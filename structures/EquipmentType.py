from Structure import *
from structures.EquipmentClass import EquipmentClass
from structures.Manufacturer import Manufacturer

class EquipmentType(Structure):

	def __init__(self, env):
		r"""
		Initialize a EquipmentType.
		"""
		self.allFields = {
			'EquipmentTypeID': fp(
				type='int',
				title='Equipment Type ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='EquipmentTypeID',
				dbPrimaryKey=True,
			),
			'ProductLine': fp(
				title='Product Line',
				dbName='ProductLine',
				dbNulls=True,
			),
			'ManufacturerID': fp(
				type='int',
				title='Manufacturer ID',
				dbName='ManufacturerID',
				dbForeignTable=Manufacturer,
			),
			'Model': fp(
				title='Model',
				dbName='Model',
			),
			'EquipmentClassID': fp(
				type='int',
				title='Equipment Class ID',
				dbName='EquipmentClassID',
				dbForeignTable=EquipmentClass,
			),
		}

		self.fieldOrder = (
			'EquipmentTypeID',
			'ProductLine',
			'ManufacturerID',
			'Model',
			'EquipmentClassID',
		)

		Structure.__init__(self,
		                   'EquipmentTypes',
		                   'EquipmentType',
		                   'Equipment Type',
		                   'Equipment Types')

		if env != None and env.configEquipmentType:
			env.configEquipmentType(self)

		self.buildFields()
