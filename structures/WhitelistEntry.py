from Structure import *
from structures.SubAccount import SubAccount

class WhitelistEntry(Structure):

	def __init__(self, env):
		r"""
		Initialize a WhitelistEntry.

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
				dbName='ExpireTime',
				dbNulls=True,
			),
		}

		self.fieldOrder = (
			'AccountID',
			'Email',
			'ExpireTime',
		)

		Structure.__init__(self,
		                   'Whitelist',
		                   'WhitelistEntry',
		                   'Whitelist Entry',
		                   'Whitelist Entries')

		if env != None and env.configWhitelistEntry:
			env.configWhitelistEntry(self)

		self.buildFields()

		if (self.allFields['ExpireTime'].present and \
		    self.allFields['Email'].present):
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['ExpireTime'].dbName + '_' + \
			  self.allFields['Email'].dbName + '] CHECK ([' + \
			  self.allFields['ExpireTime'].dbName + '] IS NULL OR [' + \
			  self.allFields['Email'].dbName + \
			  '] NOT LIKE \'*@%\'),\n'

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method generates triggers to maintain data integrity with
		relation to the table represented by the BlacklistEntry,
		MSAddressBookGroupEntry, and MSAddressBookIndividual
		structures.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.

		@remarks This method is currently all-or-nothing. If any of the
		         related tables (and their respective fields) are not
		         present, no trigger is created.
		"""
		from structures.BlacklistEntry import BlacklistEntry
		from structures.MSAddressBookGroupEntry import MSAddressBookGroupEntry
		from structures.MSAddressBookIndividual import MSAddressBookIndividual

		out = []

		if self.allFields['AccountID'].present and \
		   self.allFields['Email'].present and \
		   env != None and \
		   env.blacklistEntry and \
		   env.msAddressBookGroupEntry and \
		   env.msAddressBookIndividual:
			blacklistEntry = BlacklistEntry(env)
			msAddressBookGroupEntry = MSAddressBookGroupEntry(env)
			msAddressBookIndividual = MSAddressBookIndividual(env)
			if blacklistEntry.allFields['AccountID'].present and \
			   blacklistEntry.allFields['Email'].present and \
			   msAddressBookGroupEntry.allFields['AccountID'].present and \
			   msAddressBookGroupEntry.allFields['Email'].present and \
			   msAddressBookIndividual.allFields['AccountID'].present and \
			   msAddressBookIndividual.allFields['Email'].present:
				out.append("""
CREATE TRIGGER [tri_iu_%(dbTable)s]
ON [%(dbTable)s]
FOR INSERT, UPDATE
AS

IF (    UPDATE([%(AccountID)s])
     OR  UPDATE([%(Email)s])
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

  IF EXISTS(SELECT [%(blacklistTable)s].[%(blAccountID)s]
              FROM [%(blacklistTable)s], [INSERTED]
             WHERE [%(blacklistTable)s].[%(blAccountID)s] = [INSERTED].[%(AccountID)s]
               AND [%(blacklistTable)s].[%(blEmail)s] = [INSERTED].[%(Email)s])
   BEGIN
    ROLLBACK;
    RAISERROR('The specified e-mail address exists in the blacklist.', 9, 1);
    RETURN;
   END

 END

GO
""" % { \
	'dbTable': self.dbTable, \
	'AccountID': self.allFields['AccountID'].dbName, \
	'Email': self.allFields['Email'].dbName, \
	'blacklistTable': blacklistEntry.dbTable, \
	'blAccountID': blacklistEntry.allFields['AccountID'].dbName, \
	'blEmail': blacklistEntry.allFields['Email'].dbName, \
	'msAddressBookIndividual': msAddressBookIndividual.dbTable, \
	'msabiAccountID': msAddressBookIndividual.allFields['AccountID'].dbName, \
	'msabiEmail': msAddressBookIndividual.allFields['Email'].dbName, \
	'msAddressBookGroupEntry': msAddressBookGroupEntry.dbTable, \
	'msabgeAccountID': msAddressBookGroupEntry.allFields['AccountID'].dbName, \
	'msabgeEmail': msAddressBookGroupEntry.allFields['Email'].dbName})

		return ''.join(out)
