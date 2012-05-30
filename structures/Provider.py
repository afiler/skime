from Structure import *

class Provider(Structure):

	def __init__(self, env):
		r"""
		Initialize a Provider.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ProviderID': fp(
				type='int',
				title='Provider ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ProviderID',
				dbPrimaryKey=True,
			),
			'Provider': fp(
				title='Provider',
				dbIndexed=True,
				dbName='Provider',
				maxlength=50,
			),
			'NotifyEmail': fp(
				title='Notify Email',
				dbName='NotifyEmail',
				dbNulls=True,
			),
		}

		self.fieldOrder = (
			'ProviderID',
			'Provider',
			'NotifyEmail',
		)

		Structure.__init__(self,
		                   'Providers',
		                   'Provider',
		                   'Provider',
		                   'Providers')

		if env != None and env.configProvider:
			env.configProvider(self)

		self.buildFields()
