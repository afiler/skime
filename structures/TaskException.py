from Structure import *
from structures.Task import Task

class TaskException(Structure):

	def __init__(self, env):
		r"""
		Initialize a TaskException.
		"""
		self.allFields = {
			'TaskExceptionID': fp(
				type='int',
				title='Task Exception ID',
				editable=False,
				dbIdentity=True,
				dbName='TaskExceptionID',
				dbPrimaryKey=True,
			),
			'TaskID': fp(
				type='int',
				title='Task ID',
				dbForeignTable=Task,
				dbIndexed=True,
				dbName='TaskID',
			),
			'TaskExceptionDate': fp(
				type='date',
				title='Task Exception Date',
				dbDefault='getdate()',
				dbName='TaskExceptionDate',
			),
		}

		self.fieldOrder = (
			'TaskExceptionID',
			'TaskID',
			'TaskExceptionDate',
		)

		Structure.__init__(self,
		                   'TaskExceptions',
		                   'TaskException',
		                   'Task Exception',
		                   'Task Exceptions')

		if env != None and env.configTaskException:
			env.configTaskException(self)

		self.buildFields()
