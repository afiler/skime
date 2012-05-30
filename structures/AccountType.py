from Structure import *
from structures.ExternalSystem import ExternalSystem

class AccountType(Structure):

	def __init__(self, env):
		r"""
		Initialize an AccountType.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'AccountTypeID': fp(
				type='int',
				title='Account Type ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='AccountTypeID',
				dbPrimaryKey=True,
			),
			'AccountType': fp(
				title='Account Type',
				dbName='AccountType',
				maxlength=30,
			),
			'Cost': fp(
				type='decimal',
				title='Cost',
				dbName='Cost',
				minimum=0
			),
			'ExternalSystem': fp(
				type='int',
				title='External System',
				dbForeignKey='ExternalSystemID',
				dbForeignTable=ExternalSystem,
				dbName='ExternalSystem',
			),
		}

		self.fieldOrder = (
			'AccountTypeID',
			'AccountType',
			'Cost',
			'ExternalSystem',
		)

		Structure.__init__(self,
		                   'AccountTypes',
		                   'AccountType',
		                   'Account Type',
		                   'Account Types')

		if env != None and env.configAccountType:
			env.configAccountType(self)

		self.buildFields()
