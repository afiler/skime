from Structure import *

class DNSRecord(Structure):

	def __init__(self, env):
		r"""
		Initialize a DNSRecord.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'DNSRecordID': fp(
				type='int',
				title='DNS Record ID',
				editable=False,
				dbIdentity=True,
				dbName='DNSRecordID',
				dbPrimaryKey=True,
			),
			'Name': fp(
				title='Name',
				dbName='Name',
			),
			'Type': fp(
				title='Type',
				dbName='Type',
				dbConstraint="? = UPPER(?)",
			),
			'Target': fp(
				title='Target',
				dbName='Target',
			),
		}

		self.fieldOrder = (
			'DNSRecordID',
			'Name',
			'Type',
			'Target',
		)

		Structure.__init__(self,
		                   'DNSRecords',
		                   'DNSRecord',
		                   'DNS Record',
		                   'DNS Records')

		if env != None and env.configDNSRecord:
			env.configDNSRecord(self)

		self.buildFields()
