from Structure import *
from structures.WantAdCategory import WantAdCategory

class WantAdEntry(Structure):

	def __init__(self, env):
		r"""
		Initialize a WantAdEntry.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'AdID': fp(
				type='int',
				title='Ad ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='AdID',
				dbPrimaryKey=True,
			),
			'CategoryID': fp(
				type='int',
				title='Category ID',
				dbForeignTable=WantAdCategory,
				dbName='CategoryID',
			),
			'Title': fp(
				title='Title',
				dbName='Title',
				maxlength=40,
			),
			'Description': fp(
				title='Description',
				dbName='Description',
				maxlength=4000,
			),
			'Image': fp(
				title='Image',
				dbName='Image',
				dbNulls=True,
				maxlength=255,
			),
			'Price': fp(
				type='money',
				title='Price',
				dbName='Price',
			),
			'Name': fp(
				title='Name',
				dbName='Name',
				maxlength=40,
			),
			'Phone': fp(
				type='phone',
				title='Phone',
				dbName='Phone',
				dbNulls=True,
			),
			'Email': fp(
				title='Email',
				dbName='Email',
				dbNulls=True,
				maxlength=40,
			),
			'Location': fp(
				title='Location',
				dbName='Location',
				dbNulls=True,
				maxlength=100,
			),
			'ExpireDate': fp(
				type='date',
				title='Expire Date',
				dbName='ExpireDate',
				dbNulls=True,
			),
			'DeleteDate': fp(
				type='date',
				title='Delete Date',
				dbName='DeleteDate',
				dbNulls=True,
			),
		}

		self.fieldOrder = (
			'AdID',
			'CategoryID',
			'Title',
			'Description',
			'Image',
			'Price',
			'Name',
			'Phone',
			'Email',
			'Location',
			'ExpireDate',
			'DeleteDate',
		)

		Structure.__init__(self,
		                   'WantAdEntries',
		                   'WantAdEntry',
		                   'Want Ad Entry',
		                   'Want Ad Entries')

		if env != None and env.configWantAdEntry:
			env.configWantAdEntry(self)

		self.buildFields()
