from Structure import *
from structures.InternalUser import InternalUser
from structures.Terminal import Terminal

class DSLChannel(Structure):

	def __init__(self, env):
		r"""
		Initialize a DSLChannel.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'DSLChannelID': fp(
				type='int',
				title='Task User ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='DSLChannelID',
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
			'Shelf': fp(
				type='int',
				title='Shelf',
				dbName='Shelf',
				minimum=0,
			),
			'Slot': fp(
				type='int',
				title='Slot',
				dbName='Slot',
				minimum=1,
				maximum=26,
			),
			'Line': fp(
				type='int',
				title='Line',
				dbName='Line',
				minimum=0,
				maximum=6,
			),
			'RouterVPI': fp(
				type='int',
				title='Router VPI',
				arrangements=['form', 'list', 'row'],
				dbName='RouterVPI',
				minimum=0,
				maximum=255,
			),
			'RouterVCI': fp(
				type='int',
				title='Router VCI',
				arrangements=['form', 'list', 'row'],
				dbName='RouterVCI',
				minimum=0,
				maximum=65535,
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
			'DSLChannelID',
			'TerminalID',
			'Shelf',
			'Slot',
			'Line',
			'RouterVPI',
			'RouterVCI',
		)

		Structure.__init__(self,
		                   'DSLChannels',
		                   'DSLChannel',
		                   'DSL Channel',
		                   'DSL Channels')

		if env != None and env.configDSLChannel:
			env.configDSLChannel(self)

		self.buildFields()

		if (self.allFields['RouterVPI'].present and \
		    self.allFields['RouterVCI'].present):
			self.dbConstraints += 'UNIQUE ([' + \
			  self.allFields['RouterVPI'].dbName + '],[' + \
			  self.allFields['RouterVCI'].dbName + ']),\n'

		if (self.allFields['TerminalID'].present and \
		    self.allFields['Shelf'].present and \
		    self.allFields['Slot'].present and \
		    self.allFields['Line'].present):
			self.dbConstraints += 'UNIQUE ([' + \
			  self.allFields['TerminalID'].dbName + '],[' + \
			  self.allFields['Shelf'].dbName + '],[' + \
			  self.allFields['Slot'].dbName + '],[' + \
			  self.allFields['Line'].dbName + ']),\n'
