from Structure import *
from structures.SubAccount import SubAccount

class MSNote(Structure):

	def __init__(self, env):
		r"""
		Initialize a MSNote.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'NoteID': fp(
				type='int',
				title='Note ID',
				editable=False,
				dbIdentity=True,
				dbName='NoteID',
				dbPrimaryKey=True,
				visible=False
			),
			'AccountID': fp(
				type='int',
				title='Account ID',
				dbForeignTable=SubAccount,
				dbIndexed=True,
				dbName='AccountID',
			),
			'Category': fp(
				title='Category',
				arrangements=['form', 'list', 'row'],
				dbName='Category',
			),
			'Note': fp(
				title='Note',
				dbName='Note',
				dbType='text',
			),
			'LastModifyDate': fp(
				type='date',
				title='Last Modified',
				dbDefault='getdate()',
				dbName='LastModifyDate',
				editable=False,
			),
		}

		self.fieldOrder = (
			'NoteID',
			'AccountID',
			'Category',
			'Note',
			'LastModifyDate',
		)

		Structure.__init__(self,
		                   'MSNotes',
		                   'MSNote',
		                   'MailSite Note',
		                   'MailSite Notes')

		if env != None and env.configMSNote:
			env.configMSNote(self)

		self.buildFields()
