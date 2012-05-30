from Structure import *
from structures.InternalUser import InternalUser
from structures.Project import Project
from structures.ProjectStatus import ProjectStatus

import util.CursorWrapper

class Task(Structure):

	def __init__(self, env):
		r"""
		Initialize a Task.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'TaskID': fp(
				type='int',
				title='Task ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='TaskID',
				dbPrimaryKey=True,
			),
			'MasterTaskID': fp(
				type='int',
				title='Master Task ID',
				dbName='MasterTaskID',
				dbNulls=True,
			),
			'ProjectID': fp(
				type='int',
				title='Project ID',
				dbForeignTable=Project,
				dbName='ProjectID',
				dbNulls=True,
			),
			'TaskTitle': fp(
				title='Task Title',
				dbName='TaskTitle',
				maxlength=50,
			),
			'Comments': fp(
				title='Comments',
				dbName='Comments',
			),
			'CompletionDate': fp(
				type='date',
				title='Completion Date',
				dbName='CompletionDate',
				dbNulls=True,
			),
			'DueDate': fp(
				type='date',
				title='Due Date',
				dbName='DueDate',
				dbNulls=True,
			),
			'Priority': fp(
				type='int',
				display=disp(type='staticDropdown',
				             staticOptions={0: 'Critical',
				                            1: 'ASAP',
				                            2: 'Soon',
				                            3: 'Later',
				                            4: 'Some Day',
				                            5: 'Whenever'}),
				title='Priority',
				dbName='Priority',
				minimum=0,
				maximum=10,
			),
			'Status': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=ProjectStatus,
				             displayField='Description',
				             dataField='ProjectStatusID'),
				title='Status',
				dbName='Status',
				dbForeignKey='ProjectStatusID',
				dbForeignTable=ProjectStatus,
			),
			'Active': fp(
				type='bool',
				title='Active',
				dbName='Active',
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
				dbNulls=True,
			),
		}

		self.fieldOrder = (
			'TaskID',
			'ProjectID',
			'MasterTaskID',
			'TaskTitle',
			'Comments',
			'DueDate',
			'CompletionDate',
			'Priority',
			'Status',
			'Active',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'Tasks',
		                   'Task',
		                   'Task',
		                   'Tasks')

		if env != None and env.configTask:
			env.configTask(self)

		self.buildFields()

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method generates triggers to maintain data integrity with
		regard to the MasterTaskID. SQL Server doesn't allow cascading
		deletes to be activates on single-table relationships. These
		triggers perform the same actions.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.
		"""

		out = []

		if self.allFields['MasterTaskID'].present and \
		   self.allFields['TaskID'].present:
			out.append("""
CREATE TRIGGER [tri_d_%(dbTable)s_%(TaskID)s_%(MasterTaskID)s]
ON [%(dbTable)s]
FOR DELETE
 AS

 DELETE [%(dbTable)s] FROM [%(dbTable)s],[DELETED]
  WHERE [%(dbTable)s].[%(MasterTaskID)s] = [DELETED].[%(TaskID)s]
        AND [DELETED].[%(TaskID)s] IS NOT NULL

GO

CREATE TRIGGER [tri_iu_%(dbTable)s_%(TaskID)s_%(MasterTaskID)s]
ON [%(dbTable)s]
FOR INSERT, UPDATE
 AS

 IF UPDATE([%(MasterTaskID)s]) BEGIN
  DECLARE @master_task_id_value INTEGER

  SELECT TOP 1 @master_task_id_value = [%(MasterTaskID)s] FROM [INSERTED]
   WHERE [INSERTED].[%(MasterTaskID)s] IS NOT NULL AND NOT EXISTS(
    SELECT * FROM [%(dbTable)s]
     WHERE [%(TaskID)s]=[INSERTED].[%(MasterTaskID)s])

  IF @master_task_id_value IS NOT NULL BEGIN
   RAISERROR('The specified MasterTaskID does not exist.', 19, 1)
   ROLLBACK
   END
 END

GO
""" % { \
	'dbTable': self.dbTable, \
	'MasterTaskID': self.allFields['MasterTaskID'].dbName, \
	'TaskID': self.allFields['TaskID'].dbName})

		return ''.join(out)

	def dbLoadByDate(cls, env, con, date, max=None):
		"""
		Generate records from @a con based on @a date.

		This method is used to retrieve data from the database.

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param con         A DB-API connection to use to execute the
		                   SQL query.
		@param max         The maximum number of records to match. This
		                   value will only be honored if using a DB-API
		                   driver supports the @c rowcount attribute.
		                   DB-API 1.0 drivers do not support the
		                   @c rowcount attribute.

		@return Generates instances of the class on which this method
		        was called. Each instance will contain the data from
		        one row in the database.

		@pre @a max must be either @c None or an integer greater than
		     zero.

		@exception RuntimeError A @e RuntimeError will be thrown if
		                        the number of records matched is known
		                        and is greater than @a max.

		@todo Decide if @a con should be eliminated in favor of using
		      @c con from @a env. If so, implement this functionality.
		"""
		try:
			assert (max == None or int(max) > 0), \
			       'max must be greater than zero.'
		except ValueError:
			assert 0, 'max must be None or convertable to an int.'

		from structures.TaskDate import TaskDate
		taskInstance = Task(env)
		taskDateInstance = TaskDate(env)

		args = []
		args.append(date)

		#
		# I'm not even going to make an effort to wrap the SQL code at
		# 79 characters. It would get very, very ugly.
		#

		sql = """
DECLARE @requestDate DATETIME
SET @requestDate=CONVERT(DATETIME, ?)

SELECT DISTINCT """ + (('[' + taskInstance.dbTable + '].[') + ('],[' + \
                      taskInstance.dbTable + \
                      '].[').join([taskInstance.allFields[x].dbName \
		                   for x in taskInstance.fields]) + ']') + """
FROM [%(Task_dbTable)s],[%(TaskDate_dbTable)s]
WHERE
 [%(Task_dbTable)s].[%(TaskID)s] = [%(TaskDate_dbTable)s].[%(TaskID)s]
 AND (
       [%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s] IS NULL
       OR (
           [%(TaskDate_dbTable)s].[%(RecursYearly)s] = 0
           AND YEAR(@requestDate) > YEAR([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
           OR (
               YEAR(@requestDate) = YEAR([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
               AND MONTH(@requestDate) > MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
               OR (
                   MONTH(@requestDate) = MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
                   AND DAY(@requestDate) >= DAY([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
               )
           )
       )
       OR (
           [%(TaskDate_dbTable)s].[%(RecursYearly)s] = 1
           AND MONTH(@requestDate) > MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
           OR (
               MONTH(@requestDate) = MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
               AND DAY(@requestDate) >= DAY([%(TaskDate_dbTable)s].[%(TaskRecurrenceBeginDate)s])
           )
       )
 )
 AND (
       [%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s] IS NULL
       OR (
           [%(TaskDate_dbTable)s].[%(RecursYearly)s] = 0
           AND YEAR(@requestDate) < YEAR([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
           OR (
               YEAR(@requestDate) = YEAR([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
               AND MONTH(@requestDate) < MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
               OR (
                   MONTH(@requestDate) = MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
                   AND DAY(@requestDate) <= DAY([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
               )
           )
       )
       OR (
           [%(TaskDate_dbTable)s].[%(RecursYearly)s] = 1
           AND MONTH(@requestDate) < MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
           OR (
               MONTH(@requestDate) = MONTH([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
               AND DAY(@requestDate) <= DAY([%(TaskDate_dbTable)s].[%(TaskRecurrenceEndDate)s])
           )
       )
 )
 AND DATEDIFF(MONTH, @requestDate, [%(TaskDate_dbTable)s].[TaskDate]) %% [%(TaskDate_dbTable)s].[TaskMonthlyRecurrence] = 0
 AND DATEDIFF(DAY, @requestDate, [%(TaskDate_dbTable)s].[TaskDate]) %% [%(TaskDate_dbTable)s].[TaskDailyRecurrence] = 0
 AND NOT (
          [%(TaskDate_dbTable)s].[%(WeekdaysOnly)s] = 1
          AND (
               DATEPART(dw, @requestDate) = 1
               OR DATEPART(dw, @requestDate) = 7
          )
 )
 """ % {
	'Task_dbTable': taskInstance.dbTable,
	'TaskDate_dbTable': taskDateInstance.dbTable,
	'TaskID': taskInstance.allFields['TaskID'].dbName,
	'TaskRecurrenceBeginDate': \
	  taskDateInstance.allFields['TaskRecurrenceBeginDate'].dbName,
	'TaskRecurrenceEndDate': \
	  taskDateInstance.allFields['TaskRecurrenceEndDate'].dbName,
	'RecursYearly': taskDateInstance.allFields['RecursYearly'].dbName,
	'WeekdaysOnly': taskDateInstance.allFields['WeekdaysOnly'].dbName}

		# Handle Task Exceptions
		if env.taskException:
			from structures.TaskException import TaskException
			taskExceptionInstance = TaskException(env)

			sql +=  """
AND NOT EXISTS (
                 SELECT [%(TaskExceptionID)s]
                 FROM [%(TaskException_dbTable)s]
                 WHERE
                  [%(TaskException_dbTable)s].[%(TaskID)s] = [%(Task_dbTable)s].[%(TaskID)s]
                  AND YEAR(@requestDate) = YEAR([%(TaskException_dbTable)s].[%(TaskExceptionDate)s])
                  AND MONTH(@requestDate) = MONTH([%(TaskException_dbTable)s].[%(TaskExceptionDate)s])
                  AND DAY(@requestDate) = DAY([%(TaskException_dbTable)s].[%(TaskExceptionDate)s])
                )
""" % {
	'Task_dbTable': taskInstance.dbTable,
	'TaskException_dbTable': taskExceptionInstance.dbTable,
	'TaskExceptionID': \
	  taskExceptionInstance.allFields['TaskExceptionID'].dbName,
	'TaskExceptionDate': \
	  taskExceptionInstance.allFields['TaskExceptionDate'].dbName,
	'TaskID': taskInstance.allFields['TaskID'].dbName}

		cur = con.cursor()
		util.CursorWrapper.CursorWrapper.execute(cur, ''.join(sql), \
		                                         args)
		sql = None
		args = None

		# XXX: This is a work-around for DBAPI 1.0 compatibility.
		try:
			rowcount = cur.rowcount
			if (max != None and rowcount > max):
				raise RuntimeError, "A maximum " + str(max) + \
				      " rows were requested but " + \
				      str(rowcount) + " were found."
		except AttributeError:
			pass

		while 1:
			try:
				row = cur.fetchone()
			except:
				break
			if row != None:
				rec = record(env)
				rec.dbLoadRecord(row)
				yield rec
			else:
				break

		cur.close()

	dbLoadByDate = classmethod(dbLoadByDate)
