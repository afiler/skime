from Structure import *
from structures.Provider import Provider

class Region(Structure):

	def __init__(self, env):
		r"""
		Initialize a Region.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'RegionID': fp(
				type='int',
				title='Region ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='RegionID',
				dbPrimaryKey=True,
			),
			'Region': fp(
				title='Region',
				dbName='Region',

			),
			'ProviderID': fp(
				type='int',
				title='Provider ID',
				dbName='ProviderID',
				dbForeignTable=Provider,

			),
			'DialUpNumber': fp(
				type='phone',
				title='Dial-Up Number',
				dbName='DialUpNumber',
			),
			'HelpDeskNumber': fp(
				type='phone',
				title='Help Desk Number',
				dbName='HelpDeskNumber',
			),
			'GroupID': fp(
				type='int',
				title='Group ID',
				dbName='GroupID',
				dbNulls=True,
			),
		}

		self.fieldOrder = (
			'RegionID',
			'ProviderID',
			'Region',
			'DialUpNumber',
			'HelpDeskNumber',
			'GroupID',
		)

		Structure.__init__(self,
		                   'Regions',
		                   'Region',
		                   'Region',
		                   'Regions')

		if env != None and env.configRegion:
			env.configRegion(self)

		self.buildFields()
