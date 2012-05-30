from Structure import *

class Terminal(Structure):

	def __init__(self, env):
		r"""
		Initialize a Terminal.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'TerminalID': fp(
				type='int',
				title='Terminal ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='TerminalID',
				dbPrimaryKey=True,
			),
		}

		self.fieldOrder = (
			'TerminalID',
		)

		Structure.__init__(self,
		                   'Terminals',
		                   'Terminal',
		                   'Terminal',
		                   'Terminals')

		if env != None and env.configTerminal:
			env.configTerminal(self)

		self.buildFields()
