from Structure import *
from structures.Problem import Problem
from structures.InternalUser import InternalUser

class TroubleTicket(Structure):

	def __init__(self, env):
		r"""
		Initialize a TroubleTicket.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'TroubleTicketID': fp(
				type='int',
				title='Trouble TicketID',
				editable=False,
				dbIdentity=True,
				dbName='TroubleTicketID',
				dbPrimaryKey=True,
			),
			'AccountID': fp(
				type='int',
				title='Account ID',
				editable=False,
				dbIndexed=True,
				dbName='AccountID',
			),
			'ProviderID': fp(
				type='int',
				title='Provider ID',
				editable=False,
				dbIndexed=True,
				dbName='ProviderID',
			),
			'ProblemID': fp(
				type='int',
				title='Problem',
				dbForeignTable=Problem,
				dbIndexed=True,
				dbName='ProblemID',
			),
			'Assignee': fp(
				type='int',
				title='Assignee',
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
				dbIndexed=True,
				dbName='Assignee',
				dbNulls=True,
			),
			'Closed': fp(
				type='bool',
				title='Closed',
				visible=False,
				dbIndexed=True,
				dbName='Closed',
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
			'TroubleTicketID',
			'AccountID',
			'ProviderID',
			'ProblemID',
			'Assignee',
			'Closed',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'TroubleTickets',
		                   'TroubleTicket',
		                   'Trouble Ticket',
		                   'Trouble Tickets')

		if env != None and env.configTroubleTicket:
			env.configTroubleTicket(self)

		self.buildFields()
