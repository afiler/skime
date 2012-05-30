from Structure import *
from structures.SubAccount import SubAccount

class AbuseEvent(Structure):

	def __init__(self, env):
		r"""
		Initialize a AbuseEvent object.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'AbuseEventID': fp(
				title='Abuse Event ID',
				editable=False,
				dbDefault='newid()',
				dbName='AbuseEventID',
				dbPrimaryKey=True,
				dbType='uniqueidentifier',
				visible=False,
				maxlength=36,
			),
			'EventName': fp(
				title='Event Name',
				dbConstraint="? IN ('port_scan', 'spam_complaint', 'virus')",
				dbIndexed=True,
				dbName='EventName',
			),
			'ExpireTime': fp(
				type='date',
				title='Expire Time',
				dbDefault='DATEADD(DAY, 7, GETDATE())',
				dbName='ExpireTime',
			),
			'MessageID': fp(
				title='Message ID',
				dbName='MessageID',
				dbNulls=True,
				maxlength=14,
			),
			'IPAddress': fp(
				type='ip',
				title='IP Address',
				dbName='IPAddress',
				dbNulls=True,
			),
			'EventTime': fp(
				type='date',
				title='Event Time',
				dbName='EventTime',
				dbNulls=True,
			),
			'AccountID': fp(
				type='int',
				title='Account ID',
				dbForeignTable=SubAccount,
				dbIndexed=True,
				dbName='AccountID',
				dbNulls=True,
			),
			'FromAddress': fp(
				title='Sender',
				dbName='FromAddress',
				dbNulls=True,
				maxlength=900,
			),
			'Subject': fp(
				title='Subject',
				dbName='Subject',
				dbNulls=True,
				maxlength=4000,
			),
			'Details': fp(
				title='Details',
				dbName='Details',
				dbNulls=True,
				dbType='text',
			),
		}

		self.fieldOrder = (
			'AbuseEventID',
			'EventName',
			'ExpireTime',
			'MessageID',
			'IPAddress',
			'EventTime',
			'AccountID',
			'FromAddress',
			'Subject',
			'Details',
		)

		Structure.__init__(self,
		                   'AbuseEvents',
		                   'AbuseEvent',
		                   'Abuse Event',
		                   'Abuse Events')

		if env != None and env.configAbuseEvent:
			env.configAbuseEvent(self)

		self.buildFields()

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method generates a trigger to handle abuse events. This
		trigger notifies users of an abuse complaint and the action
		required of them. If they fail to take action, later complaints
		will cause this trigger to disconnect their account.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.

		@remarks This method is currently all-or-nothing. If any of the
		         related tables (and their respective fields) are not
		         present, no trigger is created.
		@todo The HelpdeskCalls table uses a hardcoded table name and
		      hardcoded column names. It can be changed to use data
		      from a Skime structure's allFields dictionary one the
		      HelpdeskCalls table is merged into the TroubleTickets
		      table.
		"""
		from structures.AccountType import AccountType
		from structures.AbuseGracePeriod import AbuseGracePeriod
		from structures.AbuseHandler import AbuseHandler
		from structures.Domain import Domain

		out = []

		if self.allFields['AccountID'].present and \
		   self.allFields['EventName'].present and \
		   self.allFields['EventTime'].present and \
		   env != None and \
		   env.accountType and \
		   env.abuseGracePeriod and \
		   env.abuseHandler and \
		   env.domain and \
		   env.subAccount:
			accountType = AccountType(env)
			abuseGracePeriod = AbuseGracePeriod(env)
			abuseHandler = AbuseHandler(env)
			domain = Domain(env)
			subAccount = SubAccount(env)
			if accountType.allFields['AccountTypeID'].present and \
			   abuseGracePeriod.allFields['AccountID'].present and \
			   abuseGracePeriod.allFields['Disconnected'].present and \
			   abuseGracePeriod.allFields['GracePeriodEnd'].present and \
			   abuseHandler.allFields['AccountID'].present and \
			   abuseHandler.allFields['Email'].present and \
			   domain.allFields['DomainID'].present and \
			   subAccount.allFields['AccountID'].present and \
			   subAccount.allFields['Active'].present and \
			   subAccount.allFields['DomainID'].present:
				out.append("""
DROP TRIGGER [tri_iu_%(dbTable)s]
GO

CREATE TRIGGER [tri_iu_%(dbTable)s] ON [dbo].[%(dbTable)s] 
FOR INSERT, UPDATE
AS

IF (UPDATE([%(AccountID)s]))
BEGIN
	DECLARE @AccountID int
	DECLARE @EventName varchar(255)
	DECLARE @EventTime datetime

	DECLARE %(dbTable)s_AffectedRows CURSOR FOR
		SELECT [%(AccountID)s], [%(EventName)s], [%(EventTime)s]
		  FROM [INSERTED]
	OPEN %(dbTable)s_AffectedRows

	FETCH %(dbTable)s_AffectedRows INTO @AccountID, @EventName, @EventTime

	WHILE @@fetch_status = 0
	BEGIN

		IF (    @AccountID IS NOT NULL
		    AND (@EventName = 'port_scan' OR @EventName = 'spam_complaint' OR @EventName = 'virus'))
		BEGIN
			DECLARE @rc int

			DECLARE @Email varchar(8000)
			SELECT @Email = NULL

			SELECT @Email = [%(ahEmail)s]
			  FROM [%(AbuseHandlers)s]
			 WHERE [%(ahAccountID)s] = @AccountID

			IF (@Email IS NOT NULL)
			BEGIN
				ROLLBACK;
				RAISERROR('Forward abuse complaints for AccountID %%d to %%s.', 9, 1, @AccountID, @Email);
				RETURN;
			END

			SELECT @Email = Login + '@' + Domain
			  FROM [%(Domains)s], [%(SubAccounts)s]
			 WHERE [%(SubAccounts)s].[%(saAccountID)s] = @AccountID
			   AND [%(SubAccounts)s].[%(saDomainID)s] = [%(Domains)s].[%(domainsDomainID)s]

			IF (@EventTime IS NULL)
				SELECT @EventTime = GETDATE()

			DECLARE @GracePeriodEnd datetime
			DECLARE @Disconnected bit

			SELECT
			       @GracePeriodEnd = [%(agpGracePeriodEnd)s],
			       @Disconnected = [%(agpDisconnected)s]
			  FROM [%(AbuseGracePeriods)s] (UPDLOCK)
			 WHERE [%(agpAccountID)s] = @AccountID

			IF (@GracePeriodEnd IS NOT NULL)
			BEGIN
				IF (@Disconnected = 0 AND @EventTime > @GracePeriodEnd)
				BEGIN
					DECLARE @AccountType varchar(255)

					SELECT @AccountType = AccountType
					  FROM [%(AccountTypes)s], [%(SubAccounts)s]
					 WHERE [%(SubAccounts)s].[%(saAccountTypeID)s] = [%(AccountTypes)s].[%(atAccountTypeID)s]
					   AND [%(saAccountID)s] = @AccountID

					IF (   @AccountType LIKE 'Broadband %%'
					    OR @AccountType LIKE 'DSL %%'
					    OR @AccountType LIKE 'Employee DSL %%'
					    OR @AccountType LIKE 'Wireless %%')
					BEGIN
						DECLARE @messageText nvarchar(4000)
						SELECT @messageText = N'Complaints are still being received for the following user and the grace period has ended: ' + @Email
						EXECUTE @rc = master.dbo.xp_smtp_sendmail
							@server    = N'smtp.example.com',
							@FROM      = N'abuse@example.com',
							@FROM_NAME = N'Abuse Department',
							@TO        = N'abuse@example.com',
							@subject   = N'Abuse Notice',
							@type      = N'text/plain',
							@message   = @messageText

						IF (@rc <> 0)
						BEGIN
							CLOSE %(dbTable)s_AffectedRows
							DEALLOCATE %(dbTable)s_AffectedRows
							ROLLBACK;
							RAISERROR('An error occurred while sending the e-mail to the abuse account: %%d', 9, 1, @rc);
							RETURN;
						END
					END

					-- Deactivate the account.
					UPDATE [%(SubAccounts)s]
					   SET [%(saActive)s] = 0
					       [%(saLastModifyDate)s] = GETDATE()
					 WHERE [%(saAccountID)s] = @AccountID

					-- Log info on the disconnection.
					INSERT INTO HelpdeskCalls (
						CustomerID,
						ProviderID,
						OperatorID,
						[Date],
						StartTime,
						TotalTime,
						Problem,
						Resolution
					)
						SELECT
						       CustomerID,
						       1000 AS ProviderID,
						       0 AS OperatorID,
						       GETDATE() AS [Date],
						       GETDATE() AS StartTime,
						       0 AS TotalTime,
						       'Flooding Network with Spam/Viruses' AS Problem,
						       'Disconnected. Needs to get computer fixed.' AS Resolution
						  FROM SubAccounts
						 WHERE AccountID = @AccountID

					-- Record the disconnection.
					UPDATE [%(AbuseGracePeriods)s]
					   SET [%(agpDisconnected)s] = 1
					 WHERE [%(agpAccountID)s] = @AccountID
				END
			END
			ELSE
			BEGIN
				IF (@EventName = 'port_scan')
				BEGIN
					EXECUTE @rc = master.dbo.xp_smtp_sendmail
						@server    = N'smtp.example.com',
						@FROM      = N'abuse@example.com',
						@FROM_NAME = N'Abuse Department',
						@TO        = @Email,
						@subject   = N'Abuse Notice',
						@type      = N'text/plain',
						@message   = N'Dear Customer,

We have received a complaint that your computer is attempting to gain
unauthorized access to a number of systems on the internet. This activity
is usually the result of a virus or a spyware program running on your
computer. As a precaution please run an up-to-date virus and spyware scan
of your computer. The helpdesk page ( http://helpdesk.example.com )
contains links to free virus and spyware scanners you can use. You should
apply any Critical Windows Updates ( http://windowsupdate.microsoft.com )
that your computer may require.

Failure to correct this situation will result in temporary disconnection of
your service. Willfully attempting to gain unauthorized access to other
computers on the internet will result in permanent disconnection.

If you feel you''ve received this message in error, please reply to this e-mail
immediately. If you require assistance running the virus scan, feel free to
contact the helpdesk at support@example.com.

Abuse Department
abuse@example.com
'

					-- Log info on the event.
					INSERT INTO HelpdeskCalls (
						CustomerID,
						ProviderID,
						OperatorID,
						[Date],
						StartTime,
						TotalTime,
						Problem,
						Resolution
					)
						SELECT
						       CustomerID,
						       1000 AS ProviderID,
						       0 AS OperatorID,
						       GETDATE() AS [Date],
						       GETDATE() AS StartTime,
						       0 AS TotalTime,
						       'Port Scanning' AS Problem,
						       'Needs to run a virus scan.' AS Resolution
						  FROM SubAccounts
						 WHERE AccountID = @AccountID
				END

				IF (@EventName = 'spam_complaint')
				BEGIN
					EXECUTE @rc = master.dbo.xp_smtp_sendmail
						@server    = N'smtp.example.com',
						@FROM      = N'abuse@example.com',
						@FROM_NAME = N'Abuse Department',
						@TO        = @Email,
						@subject   = N'Abuse Notice',
						@type      = N'text/plain',
						@message   = N'Dear Customer,

We have received a complaint that your computer is sending junk e-mail
(spam). This activity is usually the result of a virus or a spyware program
running on your computer. As a precaution please run an up-to-date virus
scan and spyware scan of your computer. The helpdesk page
( http://helpdesk.example.com ) contains links to free virus and spyware
scanners you can use. You should also apply any Critical Windows Updates
( http://windowsupdate.microsoft.com ) that your computer may require.

Failure to correct this situation will result in temporary disconnection of
your service. Willful spamming will result in permanent disconnection.

If you feel you''ve received this message in error, please reply to this e-mail
immediately. If you require assistance running the virus scan, feel free to
contact the helpdesk at support@example.com.

Abuse Department
abuse@example.com
'

					-- Log info on the event.
					INSERT INTO HelpdeskCalls (
						CustomerID,
						ProviderID,
						OperatorID,
						[Date],
						StartTime,
						TotalTime,
						Problem,
						Resolution
					)
						SELECT
						       CustomerID,
						       1000 AS ProviderID,
						       0 AS OperatorID,
						       GETDATE() AS [Date],
						       GETDATE() AS StartTime,
						       0 AS TotalTime,
						       'Spam Complaint' AS Problem,
						       'Needs to run a virus scan.' AS Resolution
						  FROM SubAccounts
						 WHERE AccountID = @AccountID
				END

				IF (@EventName = 'virus')
				BEGIN
					EXECUTE @rc = master.dbo.xp_smtp_sendmail
						@server    = N'smtp.example.com',
						@FROM      = N'abuse@example.com',
						@FROM_NAME = N'Abuse Department',
						@TO        = @Email,
						@subject   = N'Virus Notice',
						@type      = N'text/plain',
						@message   = N'Dear Customer,

Your computer has been sending out viruses. Please run an up-to-date
virus and spyware scan of your computer. The helpdesk page
( http://helpdesk.example.com ) contains links to free virus and spyware
scanners you can use. You should apply any Critical Windows Updates
( http://windowsupdate.microsoft.com ) that your computer may require.

Failure to correct this situation will result in temporary disconnection
of your service.

If you feel you''ve received this message in error, please reply to this
e-mail immediately. If you require assistance running the virus scan, feel
free to contact the helpdesk at support@example.com.

Abuse Department
abuse@example.com
'

					-- Log info on the event.
					INSERT INTO HelpdeskCalls (
						CustomerID,
						ProviderID,
						OperatorID,
						[Date],
						StartTime,
						TotalTime,
						Problem,
						Resolution
					)
						SELECT
						       CustomerID,
						       1000 AS ProviderID,
						       0 AS OperatorID,
						       GETDATE() AS [Date],
						       GETDATE() AS StartTime,
						       0 AS TotalTime,
						       'Virus' AS Problem,
						       'Needs to run a virus scan.' AS Resolution
						  FROM SubAccounts
						 WHERE AccountID = @AccountID
				END

				IF (@rc <> 0)
				BEGIN
					CLOSE %(dbTable)s_AffectedRows
					DEALLOCATE %(dbTable)s_AffectedRows
					ROLLBACK;
					RAISERROR('An error occurred while sending the e-mail to the customer: %%d', 9, 1, @rc);
					RETURN;
				END

				INSERT INTO [%(AbuseGracePeriods)s] ([%(agpAccountID)s]) VALUES (@AccountID);
			END
		END

		FETCH %(dbTable)s_AffectedRows INTO @AccountID, @EventName, @EventTime
	END

	CLOSE %(dbTable)s_AffectedRows
	DEALLOCATE %(dbTable)s_AffectedRows
END

""" % { \
	'dbTable': self.dbTable, \
	'AccountID': self.allFields['AccountID'].dbName, \
	'EventName': self.allFields['EventName'].dbName, \
	'EventTime': self.allFields['EventTime'].dbName, \
	'Domains': domain.dbTable, \
	'SubAccounts': subAccount.dbTable, \
	'saAccountID': subAccount.allFields['AccountID'].dbName, \
	'saActive': subAccount.allFields['Active'].dbName, \
	'saDomainID': subAccount.allFields['DomainID'].dbName, \
	'saLastModifyDate' : subAccount.allFields['LastModifyDate'].dbName, \
	'domainsDomainID': domain.allFields['DomainID'].dbName, \
	'AbuseGracePeriods': abuseGracePeriod.dbTable, \
	'agpAccountID': abuseGracePeriod.allFields['AccountID'].dbName, \
	'agpGracePeriodEnd': abuseGracePeriod.allFields['GracePeriodEnd'].dbName, \
	'agpDisconnected': abuseGracePeriod.allFields['Disconnected'].dbName, \
	'AbuseHandlers': abuseHandler.dbTable, \
	'ahAccountID': abuseHandler.allFields['AccountID'].dbName, \
	'ahEmail': abuseHandler.allFields['Email'].dbName, \
	'AccountTypes': accountType.dbTable, \
	'saAccountTypeID': subAccount.allFields['AccountTypeID'].dbName, \
	'atAccountTypeID': accountType.allFields['AccountTypeID'].dbName, \
})

		return ''.join(out)
