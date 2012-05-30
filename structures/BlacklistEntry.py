from Structure import *
from structures.SubAccount import SubAccount

class BlacklistEntry(Structure):

	def __init__(self, env):
		r"""
		Initialize a BlacklistEntry.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'AccountID': fp(
				type='int',
				title='Account ID',
				dbForeignTable=SubAccount,
				dbName='AccountID',
				dbPrimaryKey=True,
			),
			'Email': fp(
				title='Email',
				dbConstraint="? LIKE '%@%'",
				dbName='Email',
				dbPrimaryKey=True,
			),
			'ExpireTime': fp(
				type='date',
				title='Expire Time',
				dbDefault='dateadd(month, 6, getdate())',
				dbName='ExpireTime'
			),
		}

		self.fieldOrder = (
			'AccountID',
			'Email',
			'ExpireTime',
		)

		Structure.__init__(self,
		                   'Blacklist',
		                   'BlacklistEntry',
		                   'Blocked Sender',
		                   'Blocked Senders')

		if env != None and env.configBlacklistEntry:
			env.configBlacklistEntry(self)

		self.buildFields()

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method generates triggers to maintain data integrity with
		relation to the table represented by the
		MSAddressBookGroupEntry, MSAddressBookIndividual, and
		WhitelistEntry structures.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.

		@remarks This method is currently all-or-nothing. If any of the
		         related tables (and their respective fields) are not
		         present, no trigger is created.
		"""
		from structures.MSAddressBookGroupEntry import MSAddressBookGroupEntry
		from structures.MSAddressBookIndividual import MSAddressBookIndividual
		from structures.WhitelistEntry import WhitelistEntry

		out = []

		if self.allFields['AccountID'].present and \
		   self.allFields['Email'].present and \
		   env != None and \
		   env.msAddressBookGroupEntry and \
		   env.msAddressBookIndividual and \
		   env.whitelistEntry:
			msAddressBookGroupEntry = MSAddressBookGroupEntry(env)
			msAddressBookIndividual = MSAddressBookIndividual(env)
			whitelistEntry = WhitelistEntry(env)
			if msAddressBookGroupEntry.allFields['AccountID'].present and \
			   msAddressBookGroupEntry.allFields['Email'].present and \
			   msAddressBookIndividual.allFields['AccountID'].present and \
			   msAddressBookIndividual.allFields['Email'].present and \
			   whitelistEntry.allFields['AccountID'].present and \
			   whitelistEntry.allFields['Email'].present and \
			   whitelistEntry.allFields['ExpireTime'].present:
				out.append("""
CREATE TRIGGER [tri_iu_%(dbTable)s]
ON [%(dbTable)s]
FOR INSERT, UPDATE
AS

IF (    UPDATE([%(AccountID)s])
     OR UPDATE([%(Email)s])
   )
 BEGIN
  IF    EXISTS(SELECT [%(msAddressBookIndividual)s].[%(msabiEmail)s]
                 FROM [%(msAddressBookIndividual)s], [INSERTED]
                WHERE [%(msAddressBookIndividual)s].[%(msabiAccountID)s] = [INSERTED].[%(AccountID)s]
                  AND [%(msAddressBookIndividual)s].[%(msabiEmail)s] = [INSERTED].[%(Email)s])
     OR EXISTS(SELECT [%(msAddressBookGroupEntry)s].[%(msabgeEmail)s]
                 FROM [%(msAddressBookGroupEntry)s], [INSERTED]
                WHERE [%(msAddressBookGroupEntry)s].[%(msabgeAccountID)s] = [INSERTED].[%(AccountID)s]
                  AND [%(msAddressBookGroupEntry)s].[%(msabgeEmail)s] = [INSERTED].[%(Email)s])
   BEGIN
    ROLLBACK;
    RAISERROR('The specified e-mail address exists in the address book.', 9, 1);
    RETURN;
   END

  IF    EXISTS(SELECT [%(whitelistEntry)s].[%(wlEmail)s]
                 FROM [%(whitelistEntry)s], [INSERTED]
                WHERE [%(whitelistEntry)s].[%(wlAccountID)s] = [INSERTED].[%(AccountID)s]
                  AND [%(whitelistEntry)s].[%(wlEmail)s] = [INSERTED].[%(Email)s]
                  AND [%(whitelistEntry)s].[%(wlExpireTime)s] IS NULL)
   BEGIN
    ROLLBACK;
    RAISERROR('The specified e-mail address exists in the whitelist.', 9, 1);
    RETURN;
  END

  -- Delete auto whitelist entries.
  DELETE [%(whitelistEntry)s]
    FROM [%(whitelistEntry)s], [INSERTED]
   WHERE [%(whitelistEntry)s].[%(wlAccountID)s] = [INSERTED].[%(AccountID)s]
     AND [%(whitelistEntry)s].[%(wlEmail)s] = [INSERTED].[%(Email)s]
     AND [%(whitelistEntry)s].[%(wlExpireTime)s] IS NOT NULL
 END

GO
""" % { \
	'dbTable': self.dbTable, \
	'AccountID': self.allFields['AccountID'].dbName, \
	'Email': self.allFields['Email'].dbName, \
	'msAddressBookIndividual': msAddressBookIndividual.dbTable, \
	'msabiAccountID': msAddressBookIndividual.allFields['AccountID'].dbName, \
	'msabiEmail': msAddressBookIndividual.allFields['Email'].dbName, \
	'msAddressBookGroupEntry': msAddressBookGroupEntry.dbTable, \
	'msabgeAccountID': msAddressBookGroupEntry.allFields['AccountID'].dbName, \
	'msabgeEmail': msAddressBookGroupEntry.allFields['Email'].dbName, \
	'whitelistEntry': whitelistEntry.dbTable, \
	'wlAccountID': whitelistEntry.allFields['AccountID'].dbName, \
	'wlEmail': whitelistEntry.allFields['Email'].dbName, \
	'wlExpireTime': whitelistEntry.allFields['ExpireTime'].dbName})

		return ''.join(out)
