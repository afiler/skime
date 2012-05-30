from Structure import *
from structures.TroubleTicket import TroubleTicket
from structures.InternalUser import InternalUser

class TroubleTicketComment(Structure):

	def __init__(self, env):
		r"""
		Initialize a TroubleTicketComment.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'TroubleTicketCommentID': fp(
				type='int',
				title='Trouble Ticket Comment ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='TroubleTicketCommentID',
				dbPrimaryKey=True,
			),
			'TroubleTicketID': fp(
				type='int',
				title='Trouble Ticket ID',
				editable=False,
				dbForeignTable=TroubleTicket,
				dbIndexed=True,
				dbName='TroubleTicketID',
			),
			'Comment': fp(
				title='Comment',
				dbName='Comment',
				maxlength=4000,
			),
			'CallTime': fp(
				type='int',
				title='Call Time',
				dbDefault='0',
				dbName='CallTime',
				minimum=0,
			),
			'CreateDate': fp(
				type='date',
				title='Created',
				editable=False,
				dbDefault='getdate()',
				dbName='CreateDate',
			),
			'CreateUser': fp(
				type='int',
				title='Created By',
				editable=False,
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
				dbName='CreateUser',
			),
		}

		self.fieldOrder = (
			'TroubleTicketCommentID',
			'TroubleTicketID',
			'CallTime',
			'Comment',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'TroubleTicketComments',
		                   'TroubleTicketComment',
		                   'Trouble Ticket Comment',
		                   'Trouble Ticket Comments')

		if env != None and env.configTroubleTicketComment:
			env.configTroubleTicketComment(self)

		self.buildFields()
