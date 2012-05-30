from Structure import *
from structures.AccountType import AccountType
from structures.Domain import Domain
from structures.InternalUser import InternalUser
from structures.MasterAccount import MasterAccount

class SubAccount(Structure):

	def __init__(self, env):
		r"""
		Initialize a SubAccount.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'AccountID': fp(
				type='int',
				title='Account ID',
				editable=False,
				arrangements=['form', 'list', 'row'],
				dbIdentity=True,
				dbName='AccountID',
				dbPrimaryKey=True,
				visible=False,
			),
			'CustomerID': fp(
				type='int',
				title='Customer ID',
				visible=False,
				editable=False,
				dbForeignTable=MasterAccount,
				dbIndexed=True,
				dbName='CustomerID',
			),
			'Username': fp(
				title='Username',
				length=10,
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='Username',
				maxlength=40,
			),
			'Email': fp(
				title='Email Address',
				present=False,
				dbConstraint="? LIKE '%@%'",
				dbIndexed=True,
				dbName='Email',
				dbNulls=True,
				maxlength=40,
			),
			'FirstName': fp(
				title='First Name',
				length=15,
				arrangements=['form', 'list', 'row'],
				dbName='FirstName',
				maxlength=50,
			),
			'MiddleName': fp(
				title='Middle Name',
				present=False,
				length=15,
				dbName='MiddleName',
				dbNulls=True,
				maxlength=25,
			),
			'LastName': fp(
				title='Last Name',
				length=15,
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='LastName',
				maxlength=50,
			),
			'PhoneHome': fp(
				type='phone',
				title='Home Phone',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='PhoneHome',
				dbNulls=True,
			),
			'PhoneWork': fp(
				type='phone',
				title='Work Phone',
				dbName='PhoneWork',
				dbNulls=True,
			),
			'PhoneFax': fp(
				type='phone',
				title='Fax',
				dbName='PhoneFax',
				dbNulls=True,
			),
			'DialUpNumber': fp(
				type='phone',
				title='Dial-Up Number',
				present=False,
				dbName='DailUpNumber',
				dbNulls=True,
			),
			'BillingNumber': fp(
				type='phone',
				title='Billing Number',
				dbIndexed=True,
				dbName='BillingNumber',
				dbNulls=False,
			),
			'EmailAdministrator': fp(
				type='bool',
				title='Email Admin',
				dbName='EmailAdministrator',
			),
			'DiffCost': fp(
				type='int',
				title='Differential Cost',
				present=False,
				dbDefault='0',
				dbName='DiffCost',
				dbType='smallint',
			),
			'AccountTypeID': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=AccountType,
				             displayField='AccountType',
				             dataField='AccountTypeID'),
				title='Account Type',
				arrangements=['form', 'list', 'row'],
	#			dbForeignTable='AccountTypes',
				dbName='AccountTypeID',
			),
#			'SpamFilter': fp(
#				type='int',
#				display=disp(type='staticDropdown',
#				             staticOptions={0: "Off",
#				                            1: "Extra Low",
#				                            2: "Low",
#				                            3: "Medium",
#				                            4: "High",
#				                            5: "Exclusive"}),
#				title='Spam Filter',
#				arrangements=['form', 'list', 'row'],
#				dbDefault='1',
#				dbName='SpamFilter',
#				minimum=0,
#				maximum=5,
#			),
			'PayPeriodID': fp(
				type='int',
				title='Pay Period',
				present=False,
	#			dbForeignTable='PayPeriods',
				dbName='PayPeriodID',
			),
			'Cost': fp(
				type='int',
				title='Cost',
				present=False,
				dbDefault='0',
				dbName='Cost',
				minimum=0,
			),
			'DiscountID': fp(
				type='int',
				title='Discount',
				present=False,
	#			dbForeignTable='Discounts',
				dbName='DiscountID',
			),
			'Description': fp(
				title='Description',
				present=False,
				dbNulls=True,
				dbName='Description',
				maxlength='50',
			),
			'Comments': fp(
				title='Comments',
				present=False,
				dbName='Comments',
				dbNulls=True,
			),
			'Password': fp(
				title='Password',
				length=10,
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='Password',
				maxlength=32,
			),
			'MaidenName': fp(
				title="Mother's Maiden Name",
				dbName='MaidenName',
				dbNulls=True,
				maxlength=25,
			),
			'SignDate': fp(
				type='date',
				title='Signup Date',
				present=False,
				dbDefault='getdate()',
				dbName='SignDate',
			),
			'CreateDate': fp(
				type='date',
				title='Created',
				editable=False,
				dbDefault='getdate()',
				dbName='CreateDate',
			),
			'CreateUser': fp(
				type='int',
				title='Created By',
				editable=False,
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
				dbName='CreateUser',
			),
			'StartDate': fp(
				type='date',
				title='Started',
				present=False,
				dbDefault='getdate()',
				dbName='StartDate',
			),
			'BilledThru': fp(
				type='date',
				title='Billed Thru',
				present=False,
				dbName='BilledThru',
			),
			'ExpireDate': fp(
				type='date',
				title='Expiration Date',
				present=False,
				dbIndexed=True,
				dbName='ExpireDate',
				dbNulls=True,
			),
			'Extension': fp(
				type='int',
				title='Extension',
				present=False,
				dbDefault='0',
				dbName='Extension',
			),
			'Active': fp(
				type='bool',
				title='Active',
				arrangements=['form', 'list', 'row'],
				dbDefault='1',
				dbName='Active',
			),
			'NonPay': fp(
				type='bool',
				title='NonPay',
				arrangements=['form', 'list', 'row'],
				dbName='NonPay',
			),
			'Vacation': fp(
				type='bool',
				title='Vacation',
				arrangements=['form', 'list', 'row'],
				dbName='Vacation',
			),
			'VacationDate': fp(
				type='date',
				title='Vacation Date',
				dbName='VacationDate',
				dbNulls=True,
			),
			'SystemTypeID': fp(
				type='int',
				title='System Type',
				present=False,
	#			dbForeignTable='SystemTypes',
				dbName='SystemTypeID',
			),
			'ModemSpeedID': fp(
				type='int',
				title='Modem Speed',
				present=False,
	#			dbForeignTable='ModemSpeeds',
				dbName='ModemSpeedID',
			),
			'NetSoftwareID': fp(
				type='int',
				title='Software',
	#			dbForeignTable='NetSoftwares',
				dbName='NetSoftwareID',
			),
			'SalesPersonID': fp(
				type='int',
				title='Salesperson',
	#			dbForeignTable='SalesPersons',
				dbName='SalesPersonID',
				dbNulls=True,
			),
			'Operator': fp(
				title='Operator',
				present=False,
				dbDefault='suser_name()',
				dbName='Operator',
				dbNulls=True,
				maxlength=32,
			),
			'LastModifyDate': fp(
				type='date',
				title='Last Modified',
				dbDefault='getdate()',
				dbName='LastModifyDate',
				editable=False,
			),
			'LastModifyUser': fp(
				title='Last Modified By',
				editable=False,
				dbDefault='suser_name()',
				dbName='LastModifyUser',
				maxlength=32,
			),
			'Preferred': fp(
				type='bool',
				title='Preferred Customer',
				present=False,
				dbName='Preferred',
			),
			'Status': fp(
				type='int',
				title='Status',
				present=False,
				dbDefault='1',
				dbName='Status',
				dbType='smallint',
			),
			'TimeLeft': fp(
				type='int',
				title='Time Left',
				present=False,
				dbName='TimeLeft',
				dbNulls=True,
				minimum=0,
			),
			'HomeDir': fp(
				title='Home Directory',
				present=False,
				dbName='HomeDir',
				dbNulls=True,
				maxlength=100,
			),
			'HomeDirQuota': fp(
				type='int',
				title='Home Directory Quota',
				present=False,
				dbName='HomeDirLimit',
				dbNulls=True,
				minimum=0,
			),
			'SendBill': fp(
				type='bool',
				title='Send Bill',
				present=False,
				dbDefault='1',
				dbName='SendBill',
			),
			'RemoteAccess': fp(
				type='bool',
				title='Remote Access',
				present=False,
				dbDefault='1',
				dbName='RemoteAccess',
			),
			'LoginLimit': fp(
				type='int',
				title='Login Limit',
				present=False,
				dbDefault='1',
				dbName='LoginLimit',
				dbType='smallint',
				minimum=0,
			),
			'LastUsed': fp(
				type='date',
				title='Last Used',
				present=False,
				dbIndexed=True,
				dbName='LastUsed',
				dbNulls=True,
			),
			'DomainID': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=Domain,
				             displayField='Domain',
				             dataField='DomainID'),
				title='Domain',
				arrangements=['form', 'list', 'row'],
	#			dbForeignTable='Domains',
				dbName='DomainID',
			),
			'Gender': fp(
				title='Gender',
				length=1,
				present=False,
				dbName='Gender',
				dbNulls=True,
				maxlength=1,
			),
			'Salutation': fp(
				title='Salutation',
				length=4,
				present=False,
				dbName='Salutation',
				dbNulls=True,
				maxlength=4,
			),
		}

		self.fieldOrder = (
			'AccountID',
			'CustomerID',
			'Username',
			'DomainID',
			'Email',
			'Password',
			'MaidenName',
			'AccountTypeID',
			'Salutation',
			'FirstName',
			'MiddleName',
			'LastName',
			'Gender',
			'PhoneHome',
			'PhoneWork',
			'PhoneFax',
			'DialUpNumber',
			'BillingNumber',
#			'SpamFilter',
			'EmailAdministrator',
			'Active',
			'NonPay',
			'Vacation',
			'VacationDate',
			'HomeDir',
			'HomeDirQuota',
			'Preferred',
			'Status',
			'SendBill',
			'RemoteAccess',
			'LoginLimit',
			'LastUsed',
			'TimeLeft',
			'DiffCost',
			'PayPeriodID',
			'Cost',
			'DiscountID',
			'Description',
			'SignDate',
			'CreateDate',
			'CreateUser',
			'StartDate',
			'BilledThru',
			'ExpireDate',
			'Extension',
			'SystemTypeID',
			'ModemSpeedID',
			'NetSoftwareID',
			'SalesPersonID',
			'Operator',
			'LastModifyDate',
			'LastModifyUser',
			'Comments',
		)

		Structure.__init__(self,
		                   'SubAccounts',
		                   'SubAccount',
		                   'Sub Account',
		                   'Sub Accounts',
				   'row')

		if env != None and env.configSubAccount:
			env.configSubAccount(self)

		self.buildFields()

		if (self.allFields['DomainID'].present and \
		    self.allFields['Username'].present):
			self.dbConstraints += 'UNIQUE ([' + \
			  self.allFields['DomainID'].dbName + '],[' + \
			  self.allFields['Username'].dbName + ']),\n'

		if (self.allFields['Active'].present and \
		    (self.allFields['NonPay'].present or \
		     self.allFields['Vacation'].present)):
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + self.allFields['Active'].dbName
			if (self.allFields['NonPay'].present):
				self.dbConstraints += '_' + \
				  self.allFields['NonPay'].dbName
			if (self.allFields['Vacation'].present):
				self.dbConstraints += '_' + \
				  self.allFields['Vacation'].dbName
			self.dbConstraints += '] CHECK ([' + \
			  self.allFields['Active'].dbName + '] = 0 OR ('
			if (self.allFields['NonPay'].present):
				self.dbConstraints += '[' + \
				  self.allFields['NonPay'].dbName + '] = 0'
			if (self.allFields['Vacation'].present):
				if self.allFields['NonPay'].present:
					self.dbConstraints += ' AND '
				self.dbConstraints += '[' + \
				  self.allFields['Vacation'].dbName + '] = 0'
			self.dbConstraints += ')),\n'

		if (self.allFields['Vacation'].present and \
		    self.allFields['VacationDate'].present):
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['Vacation'].dbName + '] CHECK ([' + \
			  self.allFields['Vacation'].dbName + '] = 0 OR [' + \
			  self.allFields['VacationDate'].dbName + \
			  '] IS NOT NULL),\n'

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method generates a trigger to handle the expiration of
		the user's abuse grace period when his/her account is
		reconnected.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.

		@remarks This method is currently all-or-nothing. If any of the
		         related tables (and their respective fields) are not
		         present, no trigger is created.
		@remarks This trigger makes the assumption that you will not
		         change the AccountID. If you did, the result is
		         undefined, but it shouldn't be an adverse result.
		"""
		from structures.AbuseGracePeriod import AbuseGracePeriod

		out = []

		if self.allFields['AccountID'].present and \
		   self.allFields['Active'].present and \
		   env != None and \
		   env.abuseGracePeriod:
			abuseGracePeriod = AbuseGracePeriod(env)
			if abuseGracePeriod.allFields['AccountID'].present and \
			   abuseGracePeriod.allFields['ExpireTime'].present:
				out.append("""
DROP TRIGGER [tri_iu_%(dbTable)s]
GO

CREATE TRIGGER [tri_iu_%(dbTable)s] ON [dbo].[%(dbTable)s] 
FOR UPDATE
AS

IF (UPDATE([%(Active)s]))
BEGIN
	DECLARE @AccountID int
	DECLARE @Active bit
	DECLARE @OldActive bit

	DECLARE %(dbTable)s_AffectedRows CURSOR FOR
		SELECT [%(AccountID)s], [%(Active)s]
		  FROM [INSERTED]
	OPEN %(dbTable)s_AffectedRows

	FETCH %(dbTable)s_AffectedRows INTO @AccountID, @Active

	WHILE @@fetch_status = 0
	BEGIN

		SELECT @OldActive = [%(Active)s]
		  FROM [DELETED]
		 WHERE [%(AccountID)s] = @AccountID

		IF (@Active = 1 AND @OldActive = 0)
			UPDATE [%(AbuseGracePeriods)s]
			   SET [%(agpExpireTime)s] = DATEADD(DAY, 7, GETDATE())
			 WHERE [%(agpAccountID)s] = @AccountID

		FETCH %(dbTable)s_AffectedRows INTO @AccountID, @Active
	END

	CLOSE %(dbTable)s_AffectedRows
	DEALLOCATE %(dbTable)s_AffectedRows
END

""" % { \
	'dbTable': self.dbTable, \
	'AccountID': self.allFields['AccountID'].dbName, \
	'Active': self.allFields['Active'].dbName, \
	'AbuseGracePeriods': abuseGracePeriod.dbTable, \
	'agpAccountID': abuseGracePeriod.allFields['AccountID'].dbName, \
	'agpExpireTime': abuseGracePeriod.allFields['ExpireTime'].dbName, \
})

		return ''.join(out)
