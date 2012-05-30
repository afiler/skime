from Structure import *
from structures.EquipmentType import EquipmentType

class NetworkDevice(Structure):

	def __init__(self, env):
		r"""
		Initialize a NetworkDevice.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'NetworkDeviceID': fp(
				type='int',
				title='Network Device ID',
				editable=False,
				dbIdentity=True,
				dbName='NetworkDeviceID',
				dbPrimaryKey=True,
			),
			'EquipmentTypeID': fp(
				type='int',
				title='Equipment Type ID',
				dbForeignTable=EquipmentType,
				dbName='EquipmentTypeID',
			),
			'Name': fp(
				title='Name',
				dbName='Name',
				dbUnique=True,
			),
			'IPAddress': fp(
				type='ip',
				title='IP Address',
				dbName='IPAddress',
				dbNulls=True,
			),
			'Description': fp(
				title='Description',
				dbName='Description',
				dbNulls=True,
			),
		}

		self.fieldOrder = (
			'NetworkDeviceID',
			'EquipmentTypeID',
			'Name',
			'IPAddress',
			'Description',
		)

		Structure.__init__(self,
		                   'NetworkDevices',
		                   'NetworkDevice',
		                   'Network Device',
		                   'Network Devices')

		if env != None and env.configNetworkDevice:
			env.configNetworkDevice(self)

		self.buildFields()
