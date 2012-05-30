from Structure import *

class ProjectStatus(Structure):

	def __init__(self, env):
		r"""
		Initialize a ProjectStatus.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ProjectStatusID': fp(
				type='int',
				title='Project Status ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ProjectStatusID',
				dbPrimaryKey=True,
			),
			'Description': fp(
				title='Description',
				dbName='Description',
				maxlength=20,
			),
		}

		self.fieldOrder = (
			'ProjectStatusID',
			'Description',
		)

		Structure.__init__(self,
		                   'ProjectStatuses',
		                   'ProjectStatus',
		                   'Project Status',
		                   'Project Statuses')

		if env != None and env.configProjectStatus:
			env.configProjectStatus(self)

		self.buildFields()
