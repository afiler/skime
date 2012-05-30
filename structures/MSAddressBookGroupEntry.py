from Structure import *
from structures.SubAccount import SubAccount

class MSAddressBookGroupEntry(Structure):

	def __init__(self, env):
		r"""
		Initialize a MSAddressBookGroupEntry.

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
				dbPrimaryKey=True,
			),
			'Email': fp(
				title='Email',
				arrangements=['form', 'list', 'row'],
				dbConstraint="? LIKE '%@%' AND ? NOT LIKE '*@%' AND ? NOT LIKE '@%'",
				dbName='Email',
				dbPrimaryKey=True,
			),
		}

		self.fieldOrder = (
			'AccountID',
			'Nickname',
			'Email',
		)

		Structure.__init__(self,
		                   'MSAddressBookGroupEntries',
		                   'MSAddressBookGroupEntry',
		                   'MailSite Address Book Group Entry',
		                   'MailSite Address Book Group Entries')

		if env != None and env.configMSAddressBookGroupEntry:
			env.configMSAddressBookGroupEntry(self)

		self.buildFields()

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method generates triggers to maintain data integrity with
		relation to the table represented by the BlacklistEntry,
		MSAddressBookIndividual, and WhitelistEntry structures.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.

		@remarks This method is currently all-or-nothing. If any of the
		         related tables (and their respective fields) are not
		         present, no trigger is created.
		"""
		from structures.BlacklistEntry import BlacklistEntry
		from structures.MSAddressBookIndividual import MSAddressBookIndividual
		from structures.WhitelistEntry import WhitelistEntry

		out = []

		if self.allFields['AccountID'].present and \
		   self.allFields['Email'].present and \
		   env != None and \
		   env.blacklistEntry and \
		   env.msAddressBookIndividual and \
		   env.whitelistEntry:

			blacklistEntry = BlacklistEntry(env)
			msAddressBookIndividual = MSAddressBookIndividual(env)
			whitelistEntry = WhitelistEntry(env)

			if blacklistEntry.allFields['AccountID'].present and \
			   blacklistEntry.allFields['Email'].present and \
			   msAddressBookIndividual.allFields['AccountID'].present and \
			   msAddressBookIndividual.allFields['Email'].present and \
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
  IF EXISTS(SELECT [%(msAddressBookIndividual)s].[%(msabiNickname)s]
              FROM [%(msAddressBookIndividual)s], [INSERTED]
             WHERE [%(msAddressBookIndividual)s].[%(msabiAccountID)s] = [INSERTED].[%(AccountID)s]
               AND [%(msAddressBookIndividual)s].[%(msabiNickname)s] = [INSERTED].[%(Nickname)s])
   BEGIN
    ROLLBACK;
    RAISERROR('The specified nickname already exists as an individual.', 9, 1);
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
	'msAddressBookIndividual': msAddressBookIndividual.dbTable, \
	'msabiAccountID': msAddressBookIndividual.allFields['AccountID'].dbName, \
	'msabiNickname': msAddressBookIndividual.allFields['Nickname'].dbName, \
	'whitelistTable': whitelistEntry.dbTable, \
	'wlAccountID': whitelistEntry.allFields['AccountID'].dbName, \
	'wlEmail': whitelistEntry.allFields['Email'].dbName})

		return ''.join(out)
