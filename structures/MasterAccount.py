from Structure import *
from structures.Group import Group
from structures.InternalUser import InternalUser
from structures.Region import Region

class MasterAccount(Structure):

	def __init__(self, env):
		r"""
		Initialize a MasterAccount.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'CustomerID': fp(
				type='int',
				title='Customer ID',
				editable=False,
				dbIdentity=True,
				dbName='CustomerID',
				dbPrimaryKey=True,
				visible=False
			),
			'LastStatementID': fp(
				type='int',
				title='Last Statement',
				present=False,
				arrangements=['list'],
				editable=False,
				dbForeignKey='StatementID',
	#			dbForeignTable='Statements',
				dbName='LastStatementID',
			),
			'FirstName': fp(
				title='First Name',
				length=15,
				arrangements=['form', 'list', 'row'],
				dbName='FirstName',
				maxlength=50,
			),
			'MiddleName': fp(
				title='Middle Name',
				length=15,
				present=False,
				dbName='MiddleName',
				dbNulls=True,
				maxlength=25,
			),
			'LastName': fp(
				title='Last Name',
				length=15,
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='LastName',
				maxlength=50,
			),
			'Company': fp(
				title='Company',
				length=50,
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='Company',
				dbNulls=True,
				maxlength=60,
			),
			'Address1': fp(
				title='Address',
				dbName='Address1',
				dbNulls=True,
				maxlength=50,
			),
			'Address2': fp(
				dbName='Address2',
				dbNulls=True,
				maxlength=50,
			),
			'City': fp(
				title='City',
				dbName='City',
				dbNulls=True,
				maxlength=40,
			),
			'State': fp(
				type='state',
				title='State',
				dbName='State',
				dbNulls=True,
				maxlength=2,
			),
			'Zip': fp(
				type='zip',
				title='Zip',
				dbName='Zip',
				dbNulls=True,
			),
			'Province': fp(
				title='Province',
				length=2,
				present=False,
				dbName='Province',
				dbNulls=True,
				maxlength=2,
			),
			'Country': fp(
				title='Country',
				present=False,
				dbName='Country',
				dbNulls=True,
				maxlength=40,
			),
			'PhoneHome': fp(
				type='phone',
				title='Home Phone',
				dbIndexed=True,
				dbName='PhoneHome',
				dbNulls=True,
			),
			'PhoneWork': fp(
				type='phone',
				title='Work Phone',
				dbName='PhoneWork',
				dbNulls=True,
			),
			'PhoneFax': fp(
				type='phone',
				title='Fax',
				dbName='PhoneFax',
				dbNulls=True,
			),
			'DialUpNumber': fp(
				type='phone',
				title='Dial-Up Number',
				present=False,
				arrangements=['list'],
				dbName='DialUpNumber',
				dbNulls=True,
			),
			'BillingNumber': fp(
				type='phone',
				title='Billing Number',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='BillingNumber',
				dbNulls=False,
			),
			'Gender': fp(
				display=disp(type='staticDropdown',
				             staticOptions={'': '',
				                            'F': 'F',
				                            'M': 'M'}),
				title='Gender',
				length=1,
				present=False,
				arrangements=['list'],
				dbConstraint="? = 'F' OR ? = 'M'",
				dbName='Gender',
				dbNulls=True,
				maxlength=1,
			),
			'Salutation': fp(
				display=disp(type='staticDropdown', \
				             staticOptions={'': '',
				                            'Dr.': 'Dr.',
				                            'Hon.': 'Hon.',
				                            'Miss': 'Miss',
				                            'Mr.': 'Mr.',
				                            'Mrs.': 'Mrs.',
				                            'Ms.': 'Ms.',
				                            'Rev.': 'Rev.',
				                            'Sir': 'Sir'}),
				title='Salutation',
				length=4,
				present=False,
				dbName='Salutation',
				dbNulls=True,
				maxlength=4,
			),
			'RegionID': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=Region,
				             displayField='Region',
				             dataField='RegionID'),
				title='Region ',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=Region,
				dbName='RegionID',
			),
			'ReferredBy': fp(
				title='Referred By',
				present=False,
				arrangements=['list'],
				dbName='ReferredBy',
				dbNulls=True,
				maxlength=25,
			),
			'SalesPersonID': fp(
				type='int',
				title='Salesperson',
				arrangements=['list'],
	#			dbForeignTable='SalesPersons',
				dbName='SalesPersonID',
				dbNulls=True,
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
				display=disp(type='dbDropdown',
				             table=InternalUser,
				             displayField='Name',
				             dataField='InternalUserID'),
				title='Created By',
				editable=False,
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
				dbName='CreateUser',
			),
			'StartDate': fp(
				type='date',
				title='Started',
				present=False,
				editable=False,
				dbDefault='getdate()',
				dbName='StartDate',
			),
			'Active': fp(
				type='bool',
				title='Active',
				arrangements=['form', 'list', 'row'],
				dbDefault='1',
				dbName='Active',
			),
			'PayPeriodID': fp(
				type='int',
				title='Pay Period',
				present=False,
				arrangements=['list'],
				dbName='PayPeriodID',
			),
			'PayMethodID': fp(
				type='int',
				title='Payment Method',
				present=False,
				arrangements=['list'],
	#			dbForeignTable='PayMethods',
				dbName='PayMethodID',
			),
			'LastReceived': fp(
				type='date',
				title='Last Payment Received',
				present=False,
				arrangements=['list'],
				dbDefault='getdate()',
				dbName='LastReceived',
			),
			'Comments': fp(
				title='Comments',
				length=150,
				dbName='Comments',
				dbNulls=True,
			),
			'Status': fp(
				type='int',
				title='Status',
				present=False,
				arrangements=['list'],
				dbDefault='1',
				dbName='Status',
				dbType='smallint',
			),
			'GroupID': fp(
				type='int',
				title='Group',
				present=False,
				display=disp(type='dbDropdown',
				             table=Group,
				             displayField='GroupName',
				             dataField='GroupID'),
				arrangements=['form', 'list', 'row'],
				dbForeignTable=Group,
				dbIndexed=True,
				dbName='GroupID',
			),
			'OverDue': fp(
				type='int',
				title='Overdue',
				present=False,
				arrangements=['list'],
				dbName='OverDue',
				dbType='smallint',
			),
			'SendMethodID': fp(
				type='int',
				title='Send Method',
				present=False,
				arrangements=['list'],
	#			dbForeignTable='SendMethods',
				dbName='SendMethodID',
				dbType='smallint',
			),
			'OverLimit': fp(
				type='decimal',
				title='Over Limit',
				present=False,
				arrangements=['list'],
				dbName='OverLimit',
			),
			'Taxable': fp(
				type='int',
				title='Taxable',
				present=False,
				arrangements=['list'],
				dbDefault='1',
				dbName='Taxable',
				dbType='smallint',
			),
			'BillingCycleID': fp(
				type='int',
				title='Billing Cycle',
				present=False,
				arrangements=['list'],
	#			dbForeignTable='BillingCycles',
				dbIndexed=True,
				dbName='BillingCycleID',
				dbType='smallint',
			),
			'BillDay': fp(
				type='int',
				title='Billing Day',
				present=False,
				arrangements=['list'],
				dbDefault='1',
				dbName='BillDay',
				dbType='smallint',
			),
			'CancelDate': fp(
				type='date',
				title='Canceled',
				present=False,
				editable=False,
				dbName='CancelDate',
				dbNulls=True,
			),
			'CancelReasonID': fp(
				type='int',
				title='Reason for Canceling',
				present=False,
				arrangements=['list'],
	#			dbForeignTable='CancelReasons',
				dbName='CancelReasonID',
				dbNulls=True,
			),
			'Balance': fp(
				type='decimal',
				title='Balance',
				present=False,
				arrangements=['list'],
				dbDefault='0',
				dbName='Balance',
			),
			'Over30Count': fp(
				type='int',
				title='Over30Count',
				present=False,
				arrangements=['list'],
				dbDefault='0',
				dbName='Over30Count',
				dbType='smallint',
			),
			'Over60Count': fp(
				type='int',
				title='Over60Count',
				present=False,
				arrangements=['list'],
				dbDefault='0',
				dbName='Over60Count',
				dbType='smallint',
			),
			'Over90Count': fp(
				type='int',
				title='Over90Count',
				present=False,
				arrangements=['list'],
				dbDefault='0',
				dbName='Over90Count',
				dbType='smallint',
			),
			'Over120Count': fp(
				type='int',
				title='Over120Count',
				present=False,
				arrangements=['list'],
				dbDefault='0',
				dbName='Over120Count',
				dbType='smallint',
			),
			'AgedDate': fp(
				type='date',
				title='Aged Date',
				present=False,
				arrangements=['list'],
				dbName='AgedDate',
				dbNulls=True,
			),
			'PendingCredit': fp(
				type='decimal',
				title='Pending Credit',
				present=False,
				arrangements=['list'],
				dbDefault='0',
				dbName='PendingCredit',
			),
			'PendingDebit': fp(
				type='decimal',
				title='Pending Debit',
				present=False,
				arrangements=['list'],
				dbDefault='0',
				dbName='PendingDebit',
			),
			'NoticeDate': fp(
				type='date',
				title='Notice Date',
				present=False,
				arrangements=['list'],
				dbName='NoticeDate',
				dbNulls=True,
			),
			'PayInfo': fp(
				title='Payment Information',
				present=False,
				arrangements=['list'],
				dbName='PayInfo',
				dbNulls=True,
				maxlength=50,
			),
			'Operator': fp(
				title='Operator',
				present=False,
				arrangements=['list'],
				dbDefault='suser_name()',
				dbName='Operator',
				dbNulls=True,
				maxlength=32,
			),
			'LastModifyDate': fp(
				type='date',
				title='Last Modified',
				dbDefault='getdate()',
				dbIndexed=True,
				dbName='LastModifyDate',
				editable=False,
			),
			'LastModifyUser': fp(
				title='Last Modified By',
				editable=False,
				dbDefault='suser_name()',
				dbName='LastModifyUser',
				maxlength=32,
			),
		}

		self.fieldOrder = (
			'Salutation',
			'FirstName',
			'MiddleName',
			'LastName',
			'Gender',
			'Company',
			'Address1',
			'Address2',
			'City',
			'State',
			'Province',
			'Zip',
			'Country',
			'PhoneHome',
			'PhoneWork',
			'PhoneFax',
			'BillingNumber',
			'DialUpNumber',
			'RegionID',
			'ReferredBy',
			'SalesPersonID',
			'PayPeriodID',
			'PayMethodID',
			'LastStatementID',
			'LastReceived',
			'OverDue',
			'SendMethodID',
			'OverLimit',
			'Taxable',
			'BillingCycleID',
			'BillDay',
			'Balance',
			'Over30Count',
			'Over60Count',
			'Over90Count',
			'Over120Count',
			'AgedDate',
			'PendingCredit',
			'PendingDebit',
			'NoticeDate',
			'PayInfo',
			'GroupID',
			'CreateDate',
			'CreateUser',
			'StartDate',
			'CancelDate',
			'CancelReasonID',
			'Status',
			'Active',
			'Operator',
			'LastModifyDate',
			'LastModifyUser',
			'CustomerID',
			'Comments',
		)

		Structure.__init__(self,
		                   'MasterAccounts',
		                   'MasterAccount',
		                   'Master Account',
		                   'Master Accounts',
		                   'form')

		if env != None and env.configMasterAccount:
			env.configMasterAccount(self)

		self.buildFields()

	## protected:
	def getFormGuts(self, env, editable, arrangement, index):
		"""
		Get the "guts" of the form.

		This calls Structure::Structure::getFormGuts() if the
		@a arrangement is not @c 'form'. If the @a arrangement is
		@c 'form', a custom generated form view is built.

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param editable    A boolean indicating if the form should
		                   include elements for editing the fields or
		                   if it should just show the fields.
		@param arrangement The arrangement of form to build.
		@param index       The index of this form in relation to other
		                   forms for the same data structure.

		@return HTML form code representing the fields of the
		"""

		if arrangement != 'form':
			return Structure.getFormGuts(self, env, editable,
			                             arrangement, index)

		for field in self.fieldOrder:
			self.allFields[field].customFormView = False

		out = []

		out.append(self.getMultipleItemRow('Name',
		  ['Salutation', 'FirstName', 'MiddleName', 'LastName'],
		  env, editable, arrangement, index))

		out.append(self.getSingleItemRow('Company', env,
		                                 editable, arrangement, index))

		out.append(self.getSingleItemRow('Address1', env, editable,
		                                 arrangement, index))
		if self.isPrintingField('Address1', arrangement):
			out.append(self.getSingleItemRow('Address2', env,
			                                 editable, arrangement,
							 index))

		out.append(self.getMultipleItemRow('',
		  ['City', 'State', 'Province', 'Zip', 'Country'],
		  env, editable, arrangement, index))

		out.append(self.getMultipleLabeledItemRow('Phone(s)',
		  [('PhoneHome','Home'),
		   ('PhoneWork','Work'),
		   ('PhoneFax','Fax')],
		  env, editable, arrangement, index, labelPlacement=1))

		out.append(self.getSingleItemRow('BillingNumber', env,
		                                 editable, arrangement, index))
		out.append(self.getSingleItemRow('RegionID', env,
		                                 editable, arrangement, index))
		out.append(self.getSingleItemRow('GroupID', env,
		                                 editable, arrangement, index))
		out.append(self.getSingleItemRow('Active', env, editable,
		                                 arrangement, index))

		out.append(self.getMultipleLabeledItemRow('Timeline',
		  [('StartDate',),('CancelDate',)],
		  env, editable, arrangement, index))

		out.append(self.getDateAndUserRow('CreateDate', 'CreateUser',
		                                  env, editable,
		                                  arrangement, index))
		out.append(self.getDateAndUserRow('LastModifyDate',
		                                  'LastModifyUser',
		                                  env, editable,
		                                  arrangement, index))

		out.append(self.getSingleItemRow('CustomerID', env, editable,
		                                 arrangement, index))

		for field in self.fieldOrder:
			if self.allFields[
			     field].arrangements.count('form') > 0 \
			   and not self.allFields[field].customFormView:
				out.append(self.getSingleItemRow(field, env,
				  editable, arrangement, index,
				  autoSetCustomProperty=0))

		return ''.join(out)
	## public:
