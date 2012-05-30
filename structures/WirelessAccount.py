from Structure import *
from structures.EquipmentType import EquipmentType
from structures.MasterAccount import MasterAccount
from structures.SubAccount import SubAccount
from structures.Terminal import Terminal

class WirelessAccount(Structure):

	def __init__(self, env):
		r"""
		Initialize a WirelessAccount.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		__pychecker__ = 'maxlines=0'
		self.allFields = {
			'AccountID': fp(
				type='int',
				title='Account ID',
				editable=False,
				dbIdentity=True,
				dbName='AccountID',
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
			'Installed': fp(
				type='bool',
				title='Installed',
				arrangements=['form', 'list', 'row'],
				dbName='Installed',
			),
			'Billed': fp(
				type='bool',
				title='Billed',
				arrangements=['form', 'list', 'row'],
				dbName='Billed',
			),
			'Active': fp(
				type='bool',
				title='Active',
				arrangements=['form', 'list', 'row'],
				dbName='Active',
			),
			'SubAccountID': fp(
				type='int',
				title='SubAccount ID',
				dbForeignKey='AccountID',
				dbForeignTable=SubAccount,
				dbName='SubAccountID',
			),
			'Bandwidth': fp(
				type='int',
				title='Bandwidth',
				dbDefault='1024',
				dbName='Bandwidth',
				minimum=64,
			),
			'ContractExpiry': fp(
				type='date',
				title='Contract Expires',
				dbName='ContractExpiry',
				dbNulls=True,
			),
			'Filtered': fp(
				type='bool',
				title='Filtered',
				arrangements=['form', 'list', 'row'],
				dbName='Filtered',
			),
			'RadioMACAddress': fp(
				type='mac',
				title='Radio MAC Address',
				dbName='RadioMACAddress',
				dbUnique=True,
			),
			'RadioStaticIP': fp(
				type='ip',
				title='Radio Static IP Address',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='RadioStaticIP',
			),
			'SignalStrength': fp(
				title='Signal Strength',
				dbName='SignalStrength',
				maxlength=50,
			),
			'TowerAU': fp(
				title='Tower AU',
				arrangements=['form', 'list', 'row'],
				dbName='TowerAU',
				maxlength=50,
			),
			'ModemType': fp(
				type='int',
				title='Modem Type',
				dbForeignKey='EquipmentTypeID',
				dbForeignTable=EquipmentType,
				dbName='ModemType',
				maxlength=50,
			),
			'NetworkCard': fp(
				type='int',
				title='Network Card',
				dbForeignKey='EquipmentTypeID',
				dbForeignTable=EquipmentType,
				dbName='NetworkCard',
				maxlength=50,
			),
			'CreateDate': fp(
				type='date',
				title='Created',
				editable=False,
				dbDefault='getdate()',
				dbName='CreateDate',
			),
			'CreateUser': fp(
				title='Created By',
				editable=False,
				dbName='CreateUser',
			),
			'InstallDate': fp(
				title='Installation Date',
				dbName='InstallDate',
				maxlength=50,
			),
			'Installer': fp(
				title='Installer',
				dbName='Installer',
				maxlength=50,
			),
			'TestedSpeed': fp(
				type='int',
				title='Tested Speed',
				dbName='TestedSpeed',
				dbNulls=True,
				minimum=1,
			),
			'TerminalID': fp(
				type='int',
				title='Terminal ID',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=Terminal,
				dbIndexed=True,
				dbName='TerminalID',
			),
			'Users': fp(
				type='int',
				title='Users',
				arrangements=['form', 'list', 'row'],
				dbName='Users',
				minimum=1,
			),
		}

		self.fieldOrder = (
			'AccountID',
			'CustomerID',
			'Installed',
			'Billed',
			'Active',
			'SubAccountID',
			'Bandwidth',
			'Users',
			'ContractExpiry',
			'Filtered',
			'RadioMACAddress',
			'RadioStaticIP',
			'SignalStrength',
			'TowerAU',
			'ModemType',
			'NetworkCard',
			'CreateDate',
			'CreateUser',
			'InstallDate',
			'Installer',
			'TestedSpeed',
		)

		Structure.__init__(self,
		                   'WirelessAccounts',
		                   'WirelessAccount',
		                   'Wireless Account',
		                   'Wireless Accounts',
		                   'row')

		if env != None and env.configWirelessAccount:
			env.configWirelessAccount(self)

		self.buildFields()

		if (self.allFields['Active'].present and \
		    self.allFields['Billed'].present):
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['Active'].dbName + '_' + \
			  self.allFields['Billed'].dbName + \
			  '] CHECK ([' + \
			  self.allFields['Billed'].dbName + '] = 0 OR [' + \
			  self.allFields['Active'].dbName + '] = 1),\n'

		if (self.allFields['Active'].present and \
		    self.allFields['Installed'].present):
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['Active'].dbName + '_' + \
			  self.allFields['Installed'].dbName + \
			  '] CHECK ([' + self.allFields['Active'].dbName + \
			  '] = 0 OR [' + self.allFields['Installed'].dbName + \
			  '] = 1),\n'

		if (self.allFields['Installed'].present and \
		    (self.allFields['InstallDate'].present or \
		     self.allFields['Installer'].present)):
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['Installed'].dbName
			if (self.allFields['InstallDate'].present):
				self.dbConstraints += '_' + \
				  self.allFields['InstallDate'].dbName
			if (self.allFields['Installer'].present):
				self.dbConstraints += '_' + \
				  self.allFields['Installer'].dbName
			self.dbConstraints += '] CHECK ([' + \
			  self.allFields['Installed'].dbName + '] = 0 OR ('
			if (self.allFields['InstallDate'].present):
				self.dbConstraints += '[' + \
				  self.allFields['InstallDate'].dbName + \
				  '] IS NOT NULL'
			if (self.allFields['Installer'].present):
				if self.allFields['InstallDate'].present:
					self.dbConstraints += ' AND '
				self.dbConstraints += '[' + \
				  self.allFields['Installer'].dbName + \
				  '] IS NOT NULL'
			self.dbConstraints += ')),\n'




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

		@pre @a editable must be a boolean value.
		"""

		#
		# This code has too many indentation levels to fit within a
		# 79 character line. It's been wrapped as much as possible.
		#

		if arrangement != 'form':
			return Structure.getFormGuts(self, env, editable,
			                             arrangement, index)

		for field in self.fieldOrder:
			self.allFields[field].customFormView = False

		out = []

		out.append(self.getMultipleLabeledItemRow('',
		  [('Bandwidth',),('Employee',),('Filtered',),('Users',)],
		  env, editable, arrangement, index))

		out.append(self.getMultipleLabeledItemRow('',
		  [('ContractExpiry',)],
		  env, editable, arrangement, index))

		fieldHolderFunction = lambda self, label, guts: guts
		out2 = []
		if self.isPrintingField('Installed', arrangement) or \
		   self.isPrintingField('InstalledDate', arrangement) or \
		   self.isPrintingField('Installer', arrangement):


		# Line wrapping this block of code makes it impossible to read.
		# START Ignore Normal Line Wrapping Rules
			if self.values['Installed'] == 1 and ( \
			    self.isPrintingField('InstalledDate', arrangement=arrangement) or \
			    self.isPrintingField('Installer', arrangement=arrangement) \
			   ):
				if self.isPrintingField('InstalledDate', arrangement=arrangement):
					out3 = self.getFormFieldGuts(env, editable, 'InstalledDate', arrangement, index, fieldHolderFunction=fieldHolderFunction)
					if out3 != None:
						out2.append(out3)
						out2.append(' ')

						if self.isPrintingField('Installer', arrangement=arrangement):
							out3 = self.getFormFieldGuts(env, editable, 'Installer', arrangement, index, fieldHolderFunction=fieldHolderFunction)
							if out3 != None:
								out3 = out3.strip()
								if out3 != '':
									out2.append(span('by ', 'field_header'))
									out2.append(out3)
									out2.append(' ')
						out.append(row(cell(span(htmlEscape(self.allFields['InstalledDate'].title) + ': ', 'field_header')) + cell((''.join(out2)).strip())))
						out2 = []
					else:
						out3 = self.getFormFieldGuts(env, editable, 'Installer', arrangement, index, fieldHolderFunction=fieldHolderFunction)
						if out3 != None:
							out.append(row(cell(span(htmlEscape(self.allFields['Installer'].title) + ': ', 'field_header')) + cell(out3.strip())))
				else:
					out3 = self.getFormFieldGuts(env, editable, 'Installer', arrangement, index, fieldHolderFunction=fieldHolderFunction)
					if out3 != None:
						out.append(row(cell(span(htmlEscape(self.allFields['Installer'].title) + ': ', 'field_header')) + cell(out3.strip())))
			else:
				out3 = self.getFormFieldGuts(env, editable, 'Installed', arrangement, index, fieldHolderFunction=fieldHolderFunction)
				if out3 != None:
					out.append(row(cell(span(htmlEscape(self.allFields['Installed'].title) + ': ', 'field_header')) + cell(out3.strip())))
		# END Ignore Normal Line Wrapping Rules

		out.append(self.getMultipleLabeledItemRow('Test Results:',
		  [('SignalStrength',),('TestedSpeed',)], \
		  env, editable, arrangement, index))
		out.append(self.getSingleItemRow('Active', env, \
		                                 editable, arrangement, index))
		out.append(self.getSingleItemRow('Billed', env, \
		                                 editable, arrangement, index))

		out.append(self.getMultipleLabeledItemRow('Facilities', \
		  [('Terminal',),('TowerAU',)], \
		  env, editable, arrangement, index))

		out.append(self.getMultipleLabeledItemRow('Radio:', \
		  [('RadioType','Type'), \
		   ('RadioStaticIP', 'Static IP'), \
		   ('RadioMACAddress', 'MAC Address')], \
		  env, editable, arrangement, index))

		out.append(self.getDateAndUserRow('CreateDate', 'CreateUser', \
		                                  env, editable, arrangement, \
						  index))

		out.append(self.getSingleItemRow('AccountID', env, editable, \
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
