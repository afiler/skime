from Structure import *

class Manufacturer(Structure):

	def __init__(self, env):
		r"""
		Initialize a Manufacturer.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'ManufacturerID': fp(
				type='int',
				title='Manufacturer Class ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='ManufacturerID',
				dbPrimaryKey=True,
			),
			'Manufacturer': fp(
				title='Manufacturer Class',
				dbName='Manufacturer',
				dbUnique=True,
			),
		}

		self.fieldOrder = (
			'ManufacturerID',
			'Manufacturer',
		)

		Structure.__init__(self,
		                   'Manufacturers',
		                   'Manufacturer',
		                   'Manufacturer',
		                   'Manufacturers')

		if env != None and env.configManufacturer:
			env.configManufacturer(self)

		self.buildFields()
