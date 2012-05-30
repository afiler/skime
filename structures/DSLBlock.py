from Structure import *
from structures.InternalUser import InternalUser
from structures.Terminal import Terminal

class DSLBlock(Structure):

	def __init__(self, env):
		r"""
		Initialize a DSLBlock.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'DSLBlockID': fp(
				type='int',
				title='Task User ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='DSLBlockID',
				dbPrimaryKey=True,
			),
			'TerminalID': fp(
				type='int',
				title='Terminal ID',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=Terminal,
				dbIndexed=True,
				dbName='TerminalID',
			),
			'Block': fp(
				type='int',
				title='Block',
				dbName='Block',
				minimum=1,
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
			'DSLBlockID',
			'TerminalID',
			'Block',
		)

		Structure.__init__(self,
		                   'DSLBlocks',
		                   'DSLBlock',
		                   'DSL Block',
		                   'DSL Blocks')

		if env != None and env.configDSLBlock:
			env.configDSLBlock(self)

		self.buildFields()

		if (self.allFields['TerminalID'].present and \
		    self.allFields['Block'].present):
			self.dbConstraints += 'UNIQUE ([' + \
			  self.allFields['TerminalID'].dbName + '],[' + \
			  self.allFields['Block'].dbName + ']),\n'
