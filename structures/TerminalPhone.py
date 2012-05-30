from Structure import *
from structures.Terminal import Terminal

class TerminalPhone(Structure):

	def __init__(self, env):
		r"""
		Initialize a TerminalPhone.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'TerminalPhoneID': fp(
				type='int',
				title='Terminal Phone ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='TerminalPhoneID',
				dbPrimaryKey=True,
			),
			'TerminalID': fp(
				type='int',
				title='Terminal ID',
				dbName='TerminalID',
				dbForeignTable=Terminal,
			),
			'Description': fp(
				title='Description',
				dbName='Description',
			),
			'Number': fp(
				type='phone',
				title='Number',
				dbName='Number',
			),
		}

		self.fieldOrder = (
			'TerminalPhoneID',
			'TerminalID',
			'Description',
			'Number',
		)

		Structure.__init__(self,
		                   'TerminalPhones',
		                   'TerminalPhone',
		                   'Terminal Phone',
		                   'Terminal Phones')

		if env != None and env.configTerminalPhone:
			env.configTerminalPhone(self)

		self.buildFields()
