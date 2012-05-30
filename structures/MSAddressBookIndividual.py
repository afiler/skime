from Structure import *
from structures.SubAccount import SubAccount

class MSAddressBookIndividual(Structure):

	def __init__(self, env):
		r"""
		Initialize a MSAddressBookIndividual.

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
			'Nickname': fp(
				title='Nickname',
				arrangements=['form', 'list', 'row'],
				dbName='Nickname',
			),
			'Email': fp(
				title='Email',
				arrangements=['form', 'list', 'row'],
				dbConstraint="? LIKE '%@%' AND ? NOT LIKE '*@%' AND ? NOT LIKE '@%'",
				dbName='Email',
				dbPrimaryKey=True,
			),
			'FullName': fp(
				title='Full Name',
				arrangements=['form', 'list', 'row'],
				dbName='FullName',
				dbNulls=True,
			),
			'Title': fp(
				title='Title',
				dbName='Title',
				dbNulls=True,
			),
			'JobTitle': fp(
				title='Job Title',
				dbName='JobTitle',
				dbNulls=True,
			),
			'HomeAddress': fp(
				title='HomeAddress',
				dbName='HomeAddress',
				dbNulls=True,
			),
			'HomeCity': fp(
				title='Home City',
				dbName='HomeCity',
				dbNulls=True,
			),
			'HomeState': fp(
				type='state',
				title='Home State',
				dbName='HomeState',
				dbNulls=True,
			),
			'HomeZip': fp(
				type='zip',
				title='Home Zip',
				dbName='HomeZip',
				dbNulls=True,
			),
			'HomeCountry': fp(
				title='Home Country',
				dbName='HomeCountry',
				dbNulls=True,
			),
			'BusinessName': fp(
				title='Business Name',
				dbName='BusinessName',
				dbNulls=True,
			),
			'BusinessDepartment': fp(
				title='Business Department',
				dbName='BusinessDepartment',
				dbNulls=True,
			),
			'BusinessAddress': fp(
				title='Business Address',
				dbName='BusinessAddress',
				dbNulls=True,
			),
			'BusinessCity': fp(
				title='Business City',
				dbName='BusinessCity',
				dbNulls=True,
			),
			'BusinessState': fp(
				type='state',
				title='Business State',
				dbName='BusinessState',
				dbNulls=True,
			),
			'BusinessZip': fp(
				type='zip',
				title='Business Zip',
				dbName='BusinessZip',
				dbNulls=True,
			),
			'BusinessCountry': fp(
				title='Business Country',
				dbName='BusinessCountry',
				dbNulls=True,
			),
			'HomePhone': fp(
				type='phone',
				title='Home Phone',
				dbName='HomePhone',
				dbNulls=True,
			),
			'WorkPhone': fp(
				type='phone',
				title='Work Phone',
				dbName='WorkPhone',
				dbNulls=True,
			),
			'Pager': fp(
				type='phone',
				title='Pager',
				dbName='Pager',
				dbNulls=True,
			),
			'CellularPhone': fp(
				type='phone',
				title='Cellular Phone',
				dbName='CellularPhone',
				dbNulls=True,
			),
			'Fax': fp(
				type='phone',
				title='Fax',
				dbName='Fax',
				dbNulls=True,
			),
			'URL': fp(
				title='URL',
				dbName='URL',
				dbNulls=True,
				maxlength=4000,
			),
			'Notes': fp(
				title='Notes',
				dbName='Notes',
				dbNulls=True,
				dbType='text',
			),
		}

		self.fieldOrder = (
			'AccountID',
			'Nickname',
			'Email',
			'FullName',
			'Title',
			'JobTitle',
			'HomeAddress',
			'HomeCity',
			'HomeState',
			'HomeZip',
			'HomeCountry',
			'BusinessName',
			'BusinessDepartment',
			'BusinessAddress',
			'BusinessCity',
			'BusinessState',
			'BusinessZip',
			'BusinessCountry',
			'HomePhone',
			'WorkPhone',
			'Pager',
			'CellularPhone',
			'Fax',
			'URL',
			'Notes',
		)

		Structure.__init__(self,
		                   'MSAddressBookIndividuals',
		                   'MSAddressBookIndividual',
		                   'MailSite Address Book Individual',
		                   'MailSite Address Book Individuals')

		if env != None and env.configMSAddressBookIndividual:
			env.configMSAddressBookIndividual(self)

		self.buildFields()

		if (self.allFields['AccountID'].present and \
		   self.allFields['Nickname'].present):
			self.dbMiscellaneous += 'CREATE UNIQUE INDEX [idx_' + \
			  self.allFields['AccountID'].dbName + '_' + \
			  self.allFields['Nickname'].dbName + '] ON [' + \
			  self.dbTable + '] ([' + \
			  self.allFields['AccountID'].dbName + '],[' + \
			  self.allFields['Nickname'].dbName + ']);\n'

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method generates triggers to maintain data integrity with
		relation to the table represented by the BlacklistEntry,
		MSAddressBookGroupEntry, and WhitelistEntry structures.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.

		@remarks This method is currently all-or-nothing. If any of the
		         related tables (and their respective fields) are not
		         present, no trigger is created.
		"""
		from structures.BlacklistEntry import BlacklistEntry
		from structures.MSAddressBookGroupEntry import MSAddressBookGroupEntry
		from structures.WhitelistEntry import WhitelistEntry

		out = []

		if self.allFields['AccountID'].present and \
		   self.allFields['Email'].present and \
		   env != None and \
		   env.blacklistEntry and \
		   env.msAddressBookGroupEntry and \
		   env.whitelistEntry:

			blacklistEntry = BlacklistEntry(env)
			msAddressBookGroupEntry = MSAddressBookGroupEntry(env)
			whitelistEntry = WhitelistEntry(env)

			if blacklistEntry.allFields['AccountID'].present and \
			   blacklistEntry.allFields['Email'].present and \
			   msAddressBookGroupEntry.allFields['AccountID'].present and \
			   msAddressBookGroupEntry.allFields['Email'].present and \
			   whitelistEntry.allFields['AccountID'].present and \
			   whitelistEntry.allFields['Email'].present:
				out.append("""
CREATE TRIGGER [tri_iu_%(dbTable)s]
ON [%(dbTable)s]
FOR INSERT, UPDATE
AS

IF (    UPDATE([%(AccountID)s])
     OR UPDATE([%(Nickname)s])
   )
 BEGIN
  IF EXISTS(SELECT [%(msAddressBookGroupEntry)s].[%(msabgeNickname)s]
              FROM [%(msAddressBookGroupEntry)s], [INSERTED]
             WHERE [%(msAddressBookGroupEntry)s].[%(msabgeAccountID)s] = [INSERTED].[%(AccountID)s]
               AND [%(msAddressBookGroupEntry)s].[%(msabgeNickname)s] = [INSERTED].[%(Nickname)s])
   BEGIN
    ROLLBACK;
    RAISERROR('The specified nickname already exists as a group entry.', 9, 1);
    RETURN;
   END
 END

IF (    UPDATE([%(AccountID)s])
     OR UPDATE([%(Email)s])
   )
 BEGIN

  DELETE [%(blacklistTable)s]
    FROM [%(blacklistTable)s], [INSERTED]
   WHERE [%(blacklistTable)s].[%(blAccountID)s] = [INSERTED].[%(AccountID)s]
     AND [%(blacklistTable)s].[%(blEmail)s] = [INSERTED].[%(Email)s]

  DELETE [%(whitelistTable)s]
    FROM [%(whitelistTable)s], [INSERTED]
   WHERE [%(whitelistTable)s].[%(wlAccountID)s] = [INSERTED].[%(AccountID)s]
     AND [%(whitelistTable)s].[%(wlEmail)s] = [INSERTED].[%(Email)s]

 END

GO
""" % { \
	'dbTable': self.dbTable, \
	'AccountID': self.allFields['AccountID'].dbName, \
	'Email': self.allFields['Email'].dbName, \
	'Nickname': self.allFields['Nickname'].dbName, \
	'blacklistTable': blacklistEntry.dbTable, \
	'blAccountID': blacklistEntry.allFields['AccountID'].dbName, \
	'blEmail': blacklistEntry.allFields['Email'].dbName, \
	'msAddressBookGroupEntry': msAddressBookGroupEntry.dbTable, \
	'msabgeAccountID': msAddressBookGroupEntry.allFields['AccountID'].dbName, \
	'msabgeNickname': msAddressBookGroupEntry.allFields['Nickname'].dbName, \
	'whitelistTable': whitelistEntry.dbTable, \
	'wlAccountID': whitelistEntry.allFields['AccountID'].dbName, \
	'wlEmail': whitelistEntry.allFields['Email'].dbName})

		return ''.join(out)
