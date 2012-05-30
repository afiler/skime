from Structure import *
from structures.InternalUser import InternalUser
from structures.ProblemCategory import ProblemCategory

class Problem(Structure):

	def __init__(self, env):
		r"""
		Initialize a Problem.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ProblemID': fp(
				type='int',
				title='Problem ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ProblemID',
				dbPrimaryKey=True,
			),
			'ProblemCategoryID': fp(
				type='int',
				title='Problem Category',
				dbForeignTable=ProblemCategory,
				dbIndexed=True,
				dbName='ProblemCategoryID',
			),
			'ProblemDescription': fp(
				title='Description',
				dbName='ProblemDescription',
				maxlength='4000',
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
			'ProblemID',
			'ProblemCategoryID',
			'ProblemDescription',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'Problems',
		                   'Problem',
		                   'Problem',
		                   'Problems')

		if env != None and env.configProblem:
			env.configProblem(self)

		self.buildFields()
