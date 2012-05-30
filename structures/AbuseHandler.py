from Structure import *
from structures.SubAccount import SubAccount

class AbuseHandler(Structure):

	def __init__(self, env):
		r"""
		Initialize a AbuseHandler object.

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
				dbName='Email',
				maxlength=255,
			),
		}

		self.fieldOrder = (
			'AccountID',
			'Email',
		)

		Structure.__init__(self,
		                   'AbuseHandlers',
		                   'AbuseHandler',
		                   'Abuse Handler',
		                   'Abuse Handlers')

		if env != None and env.configAbuseHandler:
			env.configAbuseHandler(self)

		self.buildFields()
