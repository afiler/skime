from Structure import *
from structures.InternalUser import InternalUser
from structures.Task import Task

class TaskUser(Structure):

	def __init__(self, env):
		r"""
		Initialize a TaskUser.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'TaskUserID': fp(
				type='int',
				title='Task User ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='TaskUserID',
				dbPrimaryKey=True,
			),
			'TaskID': fp(
				type='int',
				title='Task ID',
				dbForeignTable=Task,
				dbName='TaskID',
			),
			'UserID': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=InternalUser,
				             displayField='Name',
				             dataField='InternalUserID'),
				title='Internal User ID',
				dbForeignTable=InternalUser,
				dbName='InternalUserID',
			),
		}

		self.fieldOrder = (
			'TaskUserID',
			'TaskID',
			'UserID',
		)

		Structure.__init__(self,
		                   'TaskUsers',
		                   'TaskUser',
		                   'Task User',
		                   'Task Users')

		if env != None and env.configTaskUser:
			env.configTaskUser(self)

		self.buildFields()
