# This is needed for the barf function
from display.html import htmlEscape

class env:
	r"""
	Contains info about the state of Skime, like the provider and preferences
	"""

	def __del__(self):
		try:
			if self.con != None:
				self.con.close()
		except AttributeError:
			pass

	def __init__(self, req, provider=None):
		self.req = req

		if self.req != None:
			try:
				from mod_python import util
				self.fieldStorage = util.FieldStorage(self.req)
			except ImportError:
				self.fieldStorage = {}
		else:
			self.fieldStorage = {}

		self.con = None
		self.requireSSL = False

		self.abuseEvent = 1
		self.configAbuseEvent = None
		self.abuseGracePeriod = 1
		self.configAbuseGracePeriod = None
		self.abuseHandler = 1
		self.configAbuseHandler = None
		self.accountType = 1
		self.configAccountType = None
		self.blacklistEntry = 1
		self.configBlacklistEntry = None
		self.dnsRecord = 1
		self.configDNSRecord = None
		self.domain = 1
		self.configDomain = None
		self.dslAccount = 1
		self.configDSLAccount = None
		self.dslBlock = 1
		self.configDSLBlock = None
		self.dslChannel = 1
		self.configDSLChannel = None
		self.equipmentClass = 1
		self.configEquipmentClass = None
		self.equipmentType = 1
		self.configEquipmentType = None
		self.greylistTriplet = 1
		self.configGreylistTriplet = None
		self.internalUser = 1
		self.externalSystem = 1
		self.configExternalSystem = None
		self.group = 1
		self.configGroup = None
		self.configInternalUser = None
		self.mailEvent = 1
		self.configMailEvent = None
		self.mailSenderCacheEntry = 1
		self.configMailSenderCacheEntry = None
		self.manufacturer = 1
		self.configManufacturer = None
		self.masterAccount = 1
		self.configMasterAccount = None
		self.msAddressBookIndividual = 1
		self.configMSAddressBookIndividual = None
		self.msAddressBookGroupEntry = 1
		self.configMSAddressBookGroupEntry = None
		self.msNote = 1
		self.configMSNote = None
		self.networkDevice = 1
		self.configNetworkDevice = None
		self.problem = 1
		self.configProblem = None
		self.problemCategory = 1
		self.configProblemCategory = None
		self.project = 1
		self.configProject = None
		self.projectComment = 1
		self.configProjectComment = None
		self.projectStatus = 1
		self.configProjectStatus = None
		self.projectUser = 1
		self.configProjectUser = None
		self.provider = 1
		self.configProvider = None
		self.region = 1
		self.configRegion = None
		self.subAccount = 1
		self.configSubAccount = None
		self.subWeb = 1
		self.configSubWeb = None
		self.subWebUser = 1
		self.configSubWebUser = None
		self.task = 1
		self.configTask = None
		self.taskDate = 1
		self.configTaskDate = None
		self.taskException = 1
		self.configTaskException = None
		self.taskUser = 1
		self.configTaskUser = None
		self.terminal = 1
		self.configTerminal = None
		self.terminalPhone = 1
		self.configTerminalPhone = None
		self.troubleTicket = 1
		self.configTroubleTicket = None
		self.troubleTicketComment = 1
		self.configTroubleTicketComment = None
		self.wantAdCategory = 1
		self.configWantAdCategory = None
		self.wantAdEntry = 1
		self.configWantAdEntry = None
		self.wirelessAccount = 1
		self.configWirelessAccount = None
		self.web = 1
		self.configWeb = None
		self.webRedirect = 1
		self.configWebRedirect = None
		self.webUser = 1
		self.configWebUser = None
		self.whitelistEntry = 1
		self.configWhitelistEntry = None

		if self.req == None:
			if provider == None and self.req == None:
				self.providerString = None
				return
			else:
				self.providerString = str(provider)
		else:
			# FIXME: Get Provider from req somehow (probably from the fieldStorage object)
			self.providerString = 'provider1.example.com'

		if self.providerString == "provider1.example.com":
			# TEMP: Connect to the database.
			try:
				import dbi
				import odbc
				self.con = odbc.odbc('DSN/user/pass')
			except:
				try:
					import Sybase
					self.con = Sybase.connect('127.0.0.1:1433', 'username', 'password')
				except:
					self.con = None

			self.configMasterAccount = self.provider1ConfigMasterAccount
			self.configSubAccount = self.provider1ConfigSubAccount
			self.configWeb = self.provider1ConfigWeb

			# TEMP: These tables doesn't exist in the database yet.
			self.dslAccount = 0
			self.wirelessAccount = 0

		elif self.providerString == "provider2.example.com":
			self.abuseEvent = 0
			self.abuseGracePeriod = 0
			self.abuseHandler = 0
			self.blacklistEntry = 0
			self.dnsRecord = 0
			self.dslAccount = 0
			self.dslBlock = 0
			self.dslChannel = 0
			self.equipmentClass = 0
			self.equipmentType = 0
			self.greylistTriplet = 0
			self.internalUser = 0
			self.mailEvent = 0
			self.mailSenderCacheEntry = 0
			self.manufacturer = 0
			self.configMasterAccount = self.provider2ConfigMasterAccount
			self.msAddressBookIndividual = 0
			self.msAddressBookGroupEntry = 0
			self.msNote = 0
			self.networkDevice = 0
			self.problem = 0
			self.problemCategory = 0
			self.project = 0
			self.projectComment = 0
			self.projectStatus = 0
			self.projectUser = 0
			self.configSubAccount = self.provider2ConfigSubAccount
			self.subWeb = 0
			self.subWebUser = 0
			self.task = 0
			self.taskDate = 0
			self.taskException = 0
			self.taskUser = 0
			self.terminal = 0
			self.terminalPhone = 0
			self.troubleTicket = 0
			self.troubleTicketComment = 0
			self.wantAdCategory = 0
			self.wantAdEntry = 0
			self.wirelessAccount = 0
			self.web = 0
			self.webRedirect = 0
			self.webUser = 0
			self.whitelistEntry = 0

		assert ((self.web and self.webUser) or ((not self.web) and (not self.webUser))), 'webs and webUsers must stick together.'
		assert (not self.subWeb or (self.subWeb and self.web)), 'One cannot have subWebs without webs to subdivide.'
		assert (not self.webRedirect or (self.webRedirect and self.web)), 'One cannot have webRedirects without webs to redirect to.'
		assert (not self.troubleTicketComment or (self.troubleTicketComment and self.troubleTicket)), 'One cannot have troubleTicketComments without troubleTickets to comment on.'

	# provider1.example.com Provider Configuration
	def provider1ConfigMasterAccount(self, rec):
		rec.allFields['AgedDate'].present = True
		rec.allFields['Balance'].present = True
		rec.allFields['BillDay'].present = True
		rec.allFields['BillingCycleID'].present = True
		rec.allFields['CancelDate'].present = True
		rec.allFields['CancelReasonID'].present = True
		rec.allFields['Comments'].dbType = 'text'
		rec.allFields['Country'].present = True
		rec.allFields['Country'].visible = False
		rec.allFields['CreateUser'].type = 'text'
		rec.allFields['CreateUser'].display = None
		rec.allFields['CreateUser'].dbForeignKey = None
		rec.allFields['CreateUser'].dbForeignTable = None
		rec.allFields['CreateUser'].dbType = 'varchar'
		rec.allFields['CreateUser'].length = 25
		rec.allFields['CreateUser'].maxlength = 50
		rec.allFields['DialUpNumber'].present = True
		rec.allFields['FirstName'].maxlength = 35
		rec.allFields['Gender'].present = True
		rec.allFields['GroupID'].present = True
		rec.allFields['LastModifyUser'].type = 'text'
		rec.allFields['LastModifyUser'].display = None
		rec.allFields['LastModifyUser'].dbForeignKey = None
		rec.allFields['LastModifyUser'].dbForeignTable = None
		rec.allFields['LastModifyUser'].dbType = 'varchar'
		rec.allFields['LastModifyUser'].length = 25
		rec.allFields['LastModifyUser'].maxlength = 32
		rec.allFields['LastName'].maxlength = 35
		rec.allFields['LastReceived'].present = True
		rec.allFields['MiddleName'].present = True
		rec.allFields['NoticeDate'].present = True
		rec.allFields['Operator'].present = True
		rec.allFields['Over30Count'].present = True
		rec.allFields['Over60Count'].present = True
		rec.allFields['Over90Count'].present = True
		rec.allFields['Over120Count'].present = True
		rec.allFields['OverDue'].present = True
		rec.allFields['OverLimit'].present = True
		rec.allFields['PayInfo'].present = True
		rec.allFields['PayMethodID'].present = True
		rec.allFields['PayPeriodID'].present = True
		rec.allFields['PendingCredit'].present = True
		rec.allFields['PendingDebit'].present = True
		rec.allFields['Province'].present = True
		rec.allFields['Province'].visible = False
		rec.allFields['ReferredBy'].present = True
		rec.allFields['Salutation'].present = True
		rec.allFields['SendMethodID'].present = True
		rec.allFields['StartDate'].present = True
		rec.allFields['Status'].present = True
		rec.allFields['Taxable'].present = True

	def provider1ConfigSubAccount(self, rec):
		rec.allFields['BilledThru'].present = True
		rec.allFields['Comments'].present = True
		rec.allFields['Comments'].dbType = 'text'
		rec.allFields['Cost'].present = True
		rec.allFields['CreateUser'].type = 'text'
		rec.allFields['CreateUser'].display = None
		rec.allFields['CreateUser'].dbForeignKey = None
		rec.allFields['CreateUser'].dbForeignTable = None
		rec.allFields['CreateUser'].dbType = 'varchar'
		rec.allFields['CreateUser'].length = 25
		rec.allFields['CreateUser'].maxlength = 50
		rec.allFields['Description'].present = True
		rec.allFields['DialUpNumber'].dbName = 'DialUPNumber'
		rec.allFields['DialUpNumber'].present = True
		rec.allFields['DiffCost'].present = True
		rec.allFields['DiscountID'].present = True
		rec.allFields['Email'].present = True
		rec.allFields['Extension'].present = True
		rec.allFields['ExpireDate'].present = True
		rec.allFields['Gender'].present = True
		rec.allFields['HomeDir'].present = True
		rec.allFields['HomeDirQuota'].present = True
		rec.allFields['LastModifyUser'].type = 'text'
		rec.allFields['LastModifyUser'].display = None
		rec.allFields['LastModifyUser'].dbForeignKey = None
		rec.allFields['LastModifyUser'].dbForeignTable = None
		rec.allFields['LastModifyUser'].dbType = 'varchar'
		rec.allFields['LastModifyUser'].length = 25
		rec.allFields['LastModifyUser'].maxlength = 32
		rec.allFields['LastUsed'].present = True
		rec.allFields['LoginLimit'].present = True
		rec.allFields['MiddleName'].present = True
		rec.allFields['ModemSpeedID'].present = True
		rec.allFields['Operator'].present = True
		rec.allFields['PayPeriodID'].present = True
		rec.allFields['Preferred'].present = True
		rec.allFields['RemoteAccess'].present = True
		rec.allFields['Salutation'].present = True
		rec.allFields['SendBill'].present = True
		rec.allFields['SignDate'].present = True
		rec.allFields['StartDate'].present = True
		rec.allFields['Status'].present = True
		rec.allFields['SystemTypeID'].present = True
		rec.allFields['TimeLeft'].present = True
		rec.allFields['Username'].dbName = 'Login'

	def provider1ConfigWeb(self, rec):
		rec.allFields['Name'].dbName = 'WebName'
		rec.allFields['RegistrarAccount'].dbName = 'AccountNumber'

	# provider2.example.com Provider Configuration
	def provider2ConfigMasterAccount(self, rec):
		pass

	def provider2ConfigSubAccount(self, rec):
		pass

	def barf(self, string):
		self.req.write('<p>' + htmlEscape(str(string)) + '</p>')
