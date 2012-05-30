from Structure import *
from structures.InternalUser import InternalUser
from structures.ProjectStatus import ProjectStatus

class Project(Structure):

	def __init__(self, env):
		r"""
		Initialize a Project.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ProjectID': fp(
				type='int',
				title='Project ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ProjectID',
				dbPrimaryKey=True,
			),
			'ProjectTitle': fp(
				title='Project Title',
				dbName='ProjectTitle',
				maxlength=50,
			),
			'CompletionDate': fp(
				type='date',
				title='Completion Date',
				dbName='CompletionDate',
				dbNulls=True,
			),
			'Priority': fp(
				type='int',
				display=disp(type='staticDropdown',
				             staticOptions={0: 'Critical',
				                            1: 'ASAP',
				                            2: 'Soon',
				                            3: 'Later',
				                            4: 'Some Day',
				                            5: 'Whenever'}),
				title='Priority',
				dbName='Priority',
				minimum=1,
				maximum=10,
			),
			'Status': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=ProjectStatus,
				             displayField='Description',
				             dataField='ProjectStatusID'),
				title='Status',
				dbForeignTable=ProjectStatus,
				dbForeignKey='ProjectStatusID',
				dbName='Status',
			),
			'ProposedBy': fp(
				type='int',
				title='Proposed By',
				dbForeignTable=InternalUser,
				dbForeignKey='InternalUserID',
				dbName='ProposedBy',
			),
			'ApprovedBy': fp(
				type='int',
				title='Approved By',
				dbForeignTable=InternalUser,
				dbForeignKey='InternalUserID',
				dbName='ApprovedBy',
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
			'ProjectID',
			'ProjectTitle',
			'CompletionDate',
			'Priority',
			'Status',
			'ProposedBy',
			'ApprovedBy',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'Projects',
		                   'Project',
		                   'Project',
		                   'Projects')

		if env != None and env.configProject:
			env.configProject(self)

		self.buildFields()
