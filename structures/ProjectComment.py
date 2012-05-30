from Structure import *
from structures.InternalUser import InternalUser
from structures.Project import Project

class ProjectComment(Structure):

	def __init__(self, env):
		r"""
		Initialize a ProjectComment.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ProjectCommentID': fp(
				type='int',
				title='Project Comment ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ProjectCommentID',
				dbPrimaryKey=True,
			),
			'ProjectID': fp(
				title='Project ID',
				type='int',
				visible=False,
				editable=False,
				dbForeignTable=Project,
				dbName='ProjectID',
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
			'Comment': fp(
				title='Comment',
				dbName='Comment',
				maxlength=4000,
			),
		}

		self.fieldOrder = (
			'ProjectCommentID',
			'ProjectID',
			'CreateDate',
			'CreateUser',
			'Comment',
		)

		Structure.__init__(self,
		                   'ProjectComments',
		                   'ProjectComment',
		                   'Project Comment',
		                   'Project Comments')

		if env != None and env.configProjectComment:
			env.configProjectComment(self)

		self.buildFields()
