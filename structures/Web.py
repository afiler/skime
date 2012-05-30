from Structure import *
from structures.InternalUser import InternalUser
from structures.MasterAccount import MasterAccount

class Web(Structure):

	def __init__(self, env):
		r"""
		Initialize a Web.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'WebID': fp(
				type='int',
				title='Web ID',
				editable=False,
				dbIdentity=True,
				dbName='WebID',
				dbPrimaryKey=True,
			),
			'CustomerID': fp(
				type='int',
				title='Customer ID',
				visible=False,
				editable=False,
				dbForeignTable=MasterAccount,
				dbIndexed=True,
				dbName='CustomerID',
			),
			'DesignerID': fp(
				type='int',
				title='Designer',
				dbForeignTable=MasterAccount,
				dbForeignKey='CustomerID',
				dbName='DesignerID',
				dbNulls=True,
			),
			'Name': fp(
				title='Web Name',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='Name',
				dbUnique=True,
				maxlength=50,
			),
			'WWWName': fp(
				title='WWW Name',
				dbName='WWWName',
				dbNulls=True,
				maxlength=50,
			),
			'Description': fp(
				title='Description',
				length=50,
				dbName='Description',
				dbNulls=True,
			),
			'ListInDirectory': fp(
				type='bool',
				title='List in Directory',
				dbName='ListInDirectory',
			),
			'Active': fp(
				type='bool',
				title='Active',
				arrangements=['form', 'list', 'row'],
				dbDefault='1',
				dbName='Active',
			),
			'Server': fp(
				title='Server',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='Server',
				maxlength=50,
			),
			'IPAddress': fp(
				type='ip',
				title='IP Address',
				dbName='IPAddress',
				dbNulls=True,
			),
			'DomainExpirationDate': fp(
				type='date',
				title='Domain Expiration Date',
				dbName='DomainExpirationDate',
				dbNulls=True,
			),
			'RegistrarAccount': fp(
				title='Registrar Account',
				dbName='RegistrarAccount',
				dbNulls=True,
				maxlength=30,
			),
			'RegistrarPassword': fp(
				title='Registrar Password',
				dbName='RegistrarPassword',
				dbNulls=True,
				maxlength=30,
			),
			'DiskQuota': fp(
				type='int',
				title='Disk Quota',
				length=7,
				dbName='DiskQuota',
				dbNulls=True,
			),
			'BandwidthQuota': fp(
				type='int',
				title='Bandwidth Quota',
				length=7,
				dbName='BandwidthQuota',
				dbNulls=True,
			),
			'IndexPages': fp(
				title='Index Pages',
				dbName='IndexPages',
				dbNulls=True,
			),
			'ASP': fp(
				type='bool',
				title='ASP',
				dbName='ASP'
			),
			'CGI': fp(
				type='bool',
				title='CGI',
				dbName='CGI',
			),
			'FormMail': fp(
				type='bool',
				title='FormMail',
				dbName='FormMail',
			),
			'FrontPage': fp(
				type='bool',
				title='FrontPage',
				dbName='FrontPage',
			),
			'HTTPS': fp(
				type='bool',
				title='HTTPS',
				dbName='SSL',
			),
			'MySQL': fp(
				type='bool',
				title='MySQL',
				dbName='SQL',
			),
			'Perl': fp(
				type='bool',
				title='mod_perl',
				dbName='Perl',
			),
			'PHP': fp(
				type='bool',
				title='PHP',
				dbName='PHP',
			),
			'SSI': fp(
				type='bool',
				title='SSI',
				dbName='SSI',
			),
			'StatsHostname': fp(
				title='Statistics Hostname',
				dbName='StatsHostname',
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
				title='Created By',
				editable=False,
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
				dbName='CreateUser',
			),
		}

		self.fieldOrder = (
			'WebID',
			'CustomerID',
			'DesignerID',
			'Name',
			'WWWName',
			'ListInDirectory',
			'Description',
			'Server',
			'Active',
			'IPAddress',
			'DomainExpirationDate',
			'RegistrarAccount',
			'RegistrarPassword',
			'DiskQuota',
			'BandwidthQuota',
			'IndexPages',
			'ASP',
			'CGI',
			'FormMail',
			'FrontPage',
			'HTTPS',
			'MySQL',
			'Perl',
			'PHP',
			'SSI',
			'StatsHostname',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'Webs',
		                   'Web',
		                   'Web',
		                   'Webs',
		                   'row')

		if env != None and env.configWeb:
			env.configWeb(self)

		self.buildFields()

		if self.allFields['Description'].present and\
		   self.allFields['ListInDirectory'].present:
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['Description'].dbName + '_' + \
			  self.allFields['ListInDirectory'].dbName + \
			  '] CHECK ([' + \
			  self.allFields['ListInDirectory'].dbName + \
			  '] = 0 OR ([' + \
			  self.allFields['Description'].dbName + \
			  '] IS NOT NULL AND RTRIM(LTRIM([' + \
			  self.allFields['Description'].dbName + \
			  "])) <> '')),\n"

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

		@return HTML form code representing the fields of the structure.
		"""

		out = []

		if arrangement == 'row' and not editable:
			out2 = []
			criterionIndex = 0

			out2.append('<a href="?module=WebRecord&action=view')
			for fieldName in self.findPK():
				out2.append('&criterion.')
				out2.append(str(criterionIndex))
				out2.append('=')
				out2.append(htmlEscape(fieldName))
				out2.append('&value.')
				out2.append(str(criterionIndex))
				out2.append('=')
				out2.append(htmlEscape(self.values[fieldName]))
				criterionIndex += 1
			out2.append('">[Details]</a>')
			out.append(cell(''.join(out2), 'rowset_edit_link'))

		if arrangement != 'form':
			for fieldName in self.getPrintingFields(arrangement):
				out.append(self.getFormFieldGuts(env, editable, \
							     fieldName, \
							     arrangement, \
							     index))

			return ''.join(out)


		# Handle 'form' arrangement.

		for field in self.fieldOrder:
			self.allFields[field].customFormView = False

		out.append(self.getSingleItemRow('Name', env,
		                                 editable, arrangement, index))

		out.append(self.getSingleItemRow('WWWName', env,
		                                 editable, arrangement, index))

		out.append(self.getSingleItemRow('StatsHostname', env,
		                                 editable, arrangement, index))

		out.append(self.getMultipleItemRow(
		  self.allFields['ListInDirectory'].title,
		  ['ListInDirectory', 'Description'],
		  env, editable, arrangement, index))

		out.append(self.getSingleItemRow('Active', env,
		                                 editable, arrangement, index))

		out.append(self.getMultipleLabeledItemRow('Location',
		  [('Server',),
		   ('IPAddress',)],
		  env, editable, arrangement, index, multiLine=True))

		out.append(self.getMultipleLabeledItemBlock('Features',
		  [('ASP',),
		   ('CGI',),
		   ('FormMail',),
		   ('FrontPage',),
		   ('HTTPS',),
		   ('MySQL',),
		   ('Perl',),
		   ('PHP',),
		   ('SSI',)],
		  env, editable, arrangement, index, labelPlacement=1))

		out.append(self.getSingleItemRow('IndexPages', env,
		                                 editable, arrangement, index))

		out.append(self.getMultipleLabeledItemRow('Quotas',
		  [('DiskQuota','Disk'),
		   ('BandwidthQuota','Bandwidth')],
		  env, editable, arrangement, index, multiLine=True))

		out.append(self.getMultipleLabeledItemRow('Registrar Credentials',
		  [('RegistrarAccount','Account'),
		   ('RegistrarPassword','Password')],
		  env, editable, arrangement, index, multiLine=True))


		out.append(self.getSingleItemRow('DomainExpirationDate', env,
		                                 editable, arrangement, index))

		out.append(self.getSingleItemRow('DesignerID', env,
		                                 editable, arrangement, index))

		out.append(self.getDateAndUserRow('CreateDate', 'CreateUser',
		                                  env, editable,
		                                  arrangement, index))

		out.append(self.getSingleItemRow('WebID', env, editable,
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
