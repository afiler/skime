from Structure import *

class ExternalSystem(Structure):

	def __init__(self, env):
		"""
		Initialize a ExternalSystem.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ExternalSystemID': fp(
				type='int',
				title='External System ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ExternalSystemID',
				dbPrimaryKey=True,
			),
			'Name': fp(
				title='Name',
				dbName='Name',
				maxlength='25',
			),
		}

		self.fieldOrder = (
			'ExternalSystemID',
			'Name',
		)

		Structure.__init__(self,
		                   'ExternalSystems',
		                   'ExternalSystem',
		                   'External System',
		                   'ExternalSystems')

		if env != None and env.configExternalSystem:
			env.configExternalSystem(self)

		self.buildFields()
