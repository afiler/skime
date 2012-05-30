from Structure import *
from structures.InternalUser import InternalUser
from structures.Web import Web

class WebRedirect(Structure):

	def __init__(self, env):
		r"""
		Initialize a WebRedirect.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'RedirectID': fp(
				type='int',
				title='Redirect ID',
				editable=False,
				dbIdentity=True,
				dbName='RedirectID',
				dbPrimaryKey=True,
			),
			'RedirectName': fp(
				title='Redirect Name',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='RedirectName',
				dbUnique=True,
			),
			'WebID': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=Web,
				             displayField='Name',
				             dataField='WebID'),
				title='Web',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=Web,
				dbIndexed=True,
				dbName='WebID',
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
			'RedirectID',
			'RedirectName',
			'WebID',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'WebRedirects',
		                   'WebRedirect',
		                   'Web Redirect',
		                   'Web Redirects',
				   'row')

		if env != None and env.configWebRedirect:
			env.configWebRedirect(self)

		self.buildFields()
