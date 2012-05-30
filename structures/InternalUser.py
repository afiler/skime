from Structure import *
from structures.Provider import Provider

class InternalUser(Structure):

	def __init__(self, env):
		r"""
		Initialize an InternalUser.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'InternalUserID': fp(
				type='int',
				title='Internal User ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='InternalUserID',
				dbPrimaryKey=True,
			),
			'ProviderID': fp(
				type='int',
				title='Provider ID',
				editable=False,
				dbForeignTable=Provider,
				dbIndexed=True,
				dbName='ProviderID',
			),
			'Username': fp(
				title='Username',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='Username',
				dbUnique=True,
				maxlength=50,
			),
			'Password': fp(
				title='Password',
				arrangements=['form', 'list', 'row'],
				dbName='Password',
				maxlength=50,
			),
			'Active': fp(
				type='bool',
				title='Active',
				arrangements=['form', 'list', 'row'],
				dbDefault='1',
				dbIndexed=True,
				dbName='Active',
			),
			'Name': fp(
				title='Name',
				dbName='Name',
				maxlength=50,
			),
			'Truck': fp(
				type='int',
				title='Truck',
				dbName='Truck',
				dbNulls=True,
				minimum=1,
			),
			'Email': fp(
				type='email',
				title='E-Mail',
				dbName='Email',
				dbNulls=True,
			),
			'PhoneHome': fp(
				type='phone',
				title='Home Phone',
				dbIndexed=True,
				dbName='PhoneHome',
				dbNulls=True,
			),
			'PhoneHome2': fp(
				type='phone',
				title='Home Phone 2',
				dbIndexed=True,
				dbName='PhoneHome2',
				dbNulls=True,
			),
			'PhoneOffice1': fp(
				type='phone',
				title='Office Phone',
				dbIndexed=True,
				dbName='PhoneOffice1',
				dbNulls=True,
			),
			'PhoneOffice2': fp(
				type='phone',
				title='Office Phone 2',
				dbIndexed=True,
				dbName='PhoneOffice2',
				dbNulls=True,
			),
			'PhoneFax': fp(
				type='phone',
				title='Fax',
				dbIndexed=True,
				dbName='PhoneFax',
				dbNulls=True,
			),
			'PhonePager': fp(
				type='phone',
				title='Pager',
				dbIndexed=True,
				dbName='PhonePager',
				dbNulls=True,
			),
			'PhoneCell': fp(
				type='phone',
				title='Cell Phone',
				dbIndexed=True,
				dbName='PhoneCell',
				dbNulls=True,
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
				# XXX: See below for dbForeignTable=InternalUser work-around.
				dbName='CreateUser',
			),
		}

		self.fieldOrder = (
			'InternalUserID',
			'ProviderID',
			'Username',
			'Password',
			'Active',
			'Name',
			'Email',
			'PhoneHome',
			'PhoneHome2',
			'PhoneOffice1',
			'PhoneOffice2',
			'PhoneFax',
			'PhonePager',
			'PhoneCell',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'InternalUsers',
		                   'InternalUser',
		                   'Internal User',
		                   'Internal Users')

		if env != None and env.configInternalUser:
			env.configInternalUser(self)

		self.buildFields()

		# XXX: Don't try to do this like all the other objects do it...
		# XXX: That creates a circular reference issue.
		self.allFields['CreateUser'].dbForeignTable = InternalUser
