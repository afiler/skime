from Structure import *

class Domain(Structure):

	def __init__(self, env):
		r"""
		Initialize a Domain.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'DomainID': fp(
				type='int',
				title='Domain ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='DomainID',
				dbPrimaryKey=True,
			),
			'Domain': fp(
				title='Domain',
				dbIndexed=True,
				dbName='Domain',
				maxlength=40,

			),
			'MailDomain': fp(
				title='Mail Domain',
				dbName='MailDomain',
				maxlength=40,
			),
		}

		self.fieldOrder = (
			'DomainID',
			'Domain',
			'MailDomain',
		)

		Structure.__init__(self,
		                   'Domains',
		                   'Domain',
		                   'Domain',
		                   'Domains')

		if env != None and env.configDomain:
			env.configDomain(self)

		self.buildFields()
