from Structure import *
from structures.Task import Task

class TaskDate(Structure):

	def __init__(self, env):
		r"""
		Initialize a TaskDate.
		"""
		self.allFields = {
			'TaskDateID': fp(
				type='int',
				title='Task Date ID',
				editable=False,
				dbIdentity=True,
				dbName='Task Date ID',
				dbPrimaryKey=True,
			),
			'TaskID': fp(
				type='int',
				title='Task ID',
				dbForeignTable=Task,
				dbIndexed=True,
				dbName='TaskID',
			),
			'TaskDate': fp(
				type='date',
				title='Start Date',
				dbDefault='getdate()',
				dbName='TaskDate',
			),
			'TaskMonthlyRecurrence': fp(
				type='int',
				title='Monthly Recurrence',
				dbDefault='1',
				dbName='TaskMonthlyRecurrence',
				minimum=1,
			),
			'TaskDailyRecurrence': fp(
				type='int',
				title='Daily Recurrence',
				dbDefault='1',
				dbName='TaskDailyRecurrence',
				minimum=1,
			),
			'TaskRecurrenceBeginDate': fp(
				type='date',
				title='Recurrence Begin Date',
				dbDefault='getdate()',
				dbIndexed=True,
				dbName='TaskRecurrenceBeginDate',
				dbNulls=True,
			),
			'TaskRecurrenceEndDate': fp(
				type='date',
				title='Recurrence End Date',
				dbDefault='getdate()',
				dbIndexed=True,
				dbName='TaskRecurrenceEndDate',
				dbNulls=True,
			),
			'WeekdaysOnly': fp(
				type='bool',
				title='Weekdays Only',
				dbName='WeekdaysOnly',
			),
			'RecursYearly': fp(
				type='bool',
				title='Recurs Yearly',
				dbName='RecursYearly',
			),
		}

		self.fieldOrder = (
			'TaskDateID',
			'TaskID',
			'TaskDate',
			'TaskMonthlyRecurrence',
			'TaskDailyRecurrence',
			'TaskRecurrenceBeginDate',
			'TaskRecurrenceEndDate',
			'WeekdaysOnly',
			'RecursYearly',
		)

		Structure.__init__(self,
		                   'TaskDates',
		                   'TaskDate',
		                   'Task Date',
		                   'Task Dates')

		if env != None and env.configTaskDate:
			env.configTaskDate(self)

		self.buildFields()

		if self.allFields['TaskRecurrenceBeginDate'].present and \
		   self.allFields['TaskRecurrenceEndDate'].present:

			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['TaskRecurrenceBeginDate'].dbName + \
			  '_' + self.allFields['TaskRecurrenceEndDate'].dbName

			if self.allFields['RecursYearly'].present:
				self.dbConstraints += '_' + \
				  self.allFields['RecursYearly'].dbName

			self.dbConstraints += '] CHECK ([' + \
			  self.allFields['TaskRecurrenceBeginDate'].dbName + \
			  '] <= [' + \
			  self.allFields['TaskRecurrenceEndDate'].dbName + ']'

			if self.allFields['RecursYearly'].present:
				self.dbConstraints += '''
AND (
     [RecursYearly] = 0
     OR (
         YEAR([TaskRecurrenceBeginDate]) = YEAR([TaskRecurrenceEndDate])
         AND MONTH([TaskRecurrenceBeginDate]) < MONTH([TaskRecurrenceEndDate])
         OR (
             MONTH([TaskRecurrenceBeginDate]) = MONTH([TaskRecurrenceEndDate])
             AND DAY([TaskRecurrenceBeginDate]) <= DAY([TaskRecurrenceEndDate])
         )
     )
)''' % {
	'RecursYearly': self.allFields['RecursYearly'].dbName,
	'TaskRecurrenceBeginDate': \
		self.allFields['TaskRecurrenceBeginDate'].dbName,
	'TaskRecurrenceEndDate': \
		self.allFields['TaskRecurrenceEndDate'].dbName}
			self.dbConstraints += '),\n'
