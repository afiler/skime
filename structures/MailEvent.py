from Structure import *
from structures.SubAccount import SubAccount

class MailEvent(Structure):

	def __init__(self, env):
		r"""
		Initialize a MailEvent object.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'MailEventID': fp(
				title='Mail Event ID',
				editable=False,
				dbDefault='newid()',
				dbName='MailEventID',
				dbPrimaryKey=True,
				dbType='uniqueidentifier',
				visible=False,
				maxlength=36,
			),
			'EventName': fp(
				title='Event Name',
				dbIndexed=True,
				dbName='EventName',
			),
			'ExpireTime': fp(
				type='date',
				title='Expire Time',
				dbDefault='DATEADD(DAY, 21, GETDATE())',
				dbName='ExpireTime',
			),
			'MessageID': fp(
				title='Message ID',
				dbName='MessageID',
				dbNulls=True,
				maxlength=14,
			),
			'IPAddress': fp(
				type='ip',
				title='IP Address',
				dbName='IPAddress',
				dbNulls=True,
			),
			'EventTime': fp(
				type='date',
				title='Event Time',
				dbName='EventTime',
				dbNulls=True,
			),
			'AccountID': fp(
				type='int',
				title='Account ID',
				dbForeignTable=SubAccount,
				dbIndexed=True,
				dbName='AccountID',
				dbNulls=True,
			),
			'FromAddress': fp(
				title='Sender',
				dbIndexed=True,
				dbName='FromAddress',
				dbNulls=True,
				maxlength=900,
			),
			'ToAddress': fp(
				title='Recipient',
				dbIndexed=True,
				dbName='ToAddress',
				dbNulls=True,
				maxlength=900,
			),
			'Subject': fp(
				title='Subject',
				dbName='Subject',
				dbNulls=True,
				maxlength=4000,
			),
			'Details': fp(
				title='Details',
				dbName='Details',
				dbNulls=True,
			),
		}

		self.fieldOrder = (
			'MailEventID',
			'EventName',
			'ExpireTime',
			'MessageID',
			'IPAddress',
			'EventTime',
			'AccountID',
			'FromAddress',
			'ToAddress',
			'Subject',
			'Details',
		)

		Structure.__init__(self,
		                   'MailEvents',
		                   'MailEvent',
		                   'Mail Event',
		                   'Mail Events')

		if env != None and env.configMailEvent:
			env.configMailEvent(self)

		self.buildFields()
