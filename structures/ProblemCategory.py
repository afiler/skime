from Structure import *
from structures.InternalUser import InternalUser

class ProblemCategory(Structure):

	def __init__(self, env):
		r"""
		Initialize a ProblemCategory.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ProblemCategoryID': fp(
				type='int',
				title='Problem Category ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ProblemCategoryID',
				dbPrimaryKey=True,
			),
			'ProblemCategoryDescription': fp(
				title='Description',
				dbName='ProblemCategoryDescription',
			),
			'CreateDate': fp(
				type='date',
				title='Created',
				editable=False,
				dbDefault='getdate()',
				dbName='CreateDate',
			),
			'CreateUser': fp(
				type='int',
				title='Created By',
				editable=False,
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
				dbName='CreateUser',
			),
		}

		self.fieldOrder = (
			'ProblemCategoryID',
			'ProblemCategoryDescription',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'ProblemCategories',
		                   'ProblemCategory',
		                   'Problem Category',
		                   'Problem Categories')

		if env != None and env.configProblemCategory:
			env.configProblemCategory(self)

		self.buildFields()
