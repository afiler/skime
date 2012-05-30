from Structure import *

class WantAdCategory(Structure):

	def __init__(self, env):
		r"""
		Initialize a WantAdCategory.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'CategoryID': fp(
				type='int',
				title='Category ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='CategoryID',
				dbPrimaryKey=True,
			),
			'ParentID': fp(
				type='int',
				title='Parent ID',
				dbForeignKey='CategoryID',
				# XXX: See below for dbForeignTable=WantAdCategory work-around.
				dbName='ParentID',
				dbNulls=True,
			),
			'Title': fp(
				title='Title',
				dbName='Title',
				maxlength=40,
			),
		}

		self.fieldOrder = (
			'CategoryID',
			'ParentID',
			'Title',
		)

		Structure.__init__(self,
		                   'WantAdCategories',
		                   'WantAdCategory',
		                   'Want Ad Category',
		                   'Want Ad Categories')

		if env != None and env.configWantAdCategory:
			env.configCategory(self)

		self.buildFields()

		# XXX: Don't try to do this like all the other objects do it...
		# XXX: That creates a circular reference issue.
		self.allFields['ParentID'].dbForeignTable = WantAdCategory
