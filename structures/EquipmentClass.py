from Structure import *

class EquipmentClass(Structure):

	def __init__(self, env):
		r"""
		Initialize a EquipmentClass.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'EquipmentClassID': fp(
				type='int',
				title='Equipment Class ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='EquipmentClassID',
				dbPrimaryKey=True,
			),
			'EquipmentClass': fp(
				title='Equipment Class',
				dbName='EquipmentClass',
				dbUnique=True,
			),
		}

		self.fieldOrder = (
			'EquipmentClassID',
			'EquipmentClass',
		)

		Structure.__init__(self,
		                   'EquipmentClasses',
		                   'EquipmentClass',
		                   'Equipment Class',
		                   'Equipment Classes')

		if env != None and env.configEquipmentClass:
			env.configEquipmentClass(self)

		self.buildFields()
