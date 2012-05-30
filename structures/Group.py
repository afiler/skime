from Structure import *
from structures.Domain import Domain

class Group(Structure):

	def __init__(self, env):
		r"""
		Initialize a Group.
		"""
		self.allFields = {
			'GroupID': fp(
				type='int',
				title='Group ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='GroupID',
				dbPrimaryKey=True,
			),
			'DomainID': fp(
				type='int',
				title='Domain ID',
				dbForeignTable=Domain,
				dbName='DomainID',
			),
			'GroupName': fp(
				title='Group Name',
				dbName='GroupName',
			),
		}

		self.fieldOrder = (
			'GroupID',
			'DomainID',
			'GroupName',
		)

		Structure.__init__(self,
		                   'Groups',
		                   'Group',
		                   'Group',
		                   'Groups')

		if env != None and env.configGroup:
			env.configGroup(self)

		self.buildFields()
