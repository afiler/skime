from Structure import *

class MailSenderCacheEntry(Structure):

	def __init__(self, env):
		r"""
		Initialize a MailSenderCacheEntry.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'Address': fp(
				title='Address',
				dbName='Address',
				dbPrimaryKey=True,
				maxlength=900,
			),
			'Valid': fp(
				type='bool',
				title='Valid',
				dbName='Valid',
			),
			'ExpireTime': fp(
				type='date',
				title='Expire Time',
				dbDefault='dateadd(hour, 1, getdate())',
				dbName='ExpireTime'
			),
		}

		self.fieldOrder = (
			'Address',
			'Valid',
			'ExpireTime',
		)

		Structure.__init__(self,
		                   'MailSenderCache',
		                   'MailSenderCacheEntry',
		                   'Cached Sender Address',
		                   'Cached Sender Addresses')

		if env != None and env.configMailSenderCacheEntry:
			env.configMailSenderCacheEntry(self)

		self.buildFields()
