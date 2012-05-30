from Structure import *
from structures.SubAccount import SubAccount

class AbuseGracePeriod(Structure):

	def __init__(self, env):
		r"""
		Initialize a AbuseGracePeriod object.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'AccountID': fp(
				type='int',
				title='Account ID',
				dbForeignTable=SubAccount,
				dbIndexed=True,
				dbName='AccountID',
				dbNulls=True,
				dbPrimaryKey=True,
			),
			'GracePeriodEnd': fp(
				type='date',
				title='Grace Period End',
				dbDefault='DATEADD(DAY, 5, GETDATE())',
				dbName='GracePeriodEnd',
			),
			'Disconnected': fp(
				type='bool',
				title='Disconnected',
				dbName='Disconnected',
			),
			'ExpireTime': fp(
				type='date',
				title='Expire Time',
				dbDefault='DATEADD(DAY, 30, GETDATE())',
				dbName='ExpireTime',
			),
		}

		self.fieldOrder = (
			'AccountID',
			'GracePeriodEnd',
			'Disconnected',
			'ExpireTime',
		)

		Structure.__init__(self,
		                   'AbuseGracePeriods',
		                   'AbuseGracePeriod',
		                   'Abuse Grace Period',
		                   'Abuse Grace Periods')

		if env != None and env.configAbuseGracePeriod:
			env.configAbuseGracePeriod(self)

		self.buildFields()
