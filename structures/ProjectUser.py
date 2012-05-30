from Structure import *
from structures.InternalUser import InternalUser
from structures.Project import Project

class ProjectUser(Structure):

	def __init__(self, env):
		r"""
		Initialize a ProjectUser.
		"""
		self.allFields = {
			'ProjectUserID': fp(
				type='int',
				title='Project User ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ProjectUserID',
				dbPrimaryKey=True,
			),
			'UserID': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=InternalUser,
				             displayField='Name',
				             dataField='InternalUserID'),
				title='User ID',
				dbName='UserID',
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
			),
			'ProjectID': fp(
				type='int',
				title='Project ID',
				dbName='ProjectID',
				dbForeignKey='ProjectID',
				dbForeignTable=Project,
			),
			'Leader': fp(
				type='bool',
				title='Leader',
				dbName='Leader',
			),
		}

		self.fieldOrder = (
			'ProjectUserID',
			'UserID',
			'ProjectID',
			'Leader',
		)

		Structure.__init__(self,
		                   'ProjectUsers',
		                   'ProjectUser',
		                   'Project User',
		                   'Project Users')

		if env != None and env.configProjectUser:
			env.configProjectUser(self)

		self.buildFields()
