import env

def create_table(env, record):
	fields = [x for x in record.fieldOrder if record.allFields[x].present and not record.allFields[x].dbDynamicProperty]
	assert len(fields) > 0, 'No fields were present.'

	out = []

	out.append("CREATE TABLE [")
	out.append(record.dbTable)
	out.append("] (\n")
	for fieldName in fields:
		field = record.allFields[fieldName]

		out.append('[')
		out.append(field.dbName)
		out.append('] ')
		out.append(field.dbType)

		if field.dbType.endswith('char'):
			out.append('(')
			# Deal with differences between database length and HTML maxlength.
			if field.type == 'mac':
				out.append('12')
			elif field.type == 'phone':
				out.append('10')
			else:
				out.append(str(field.maxlength))

			out += ')'

		if field.dbConstraint != None:
			out.append(' CHECK(')
			out.append(field.dbConstraint.replace('?', '[' + field.dbName + ']'))
			out.append(')')

		if field.dbDefault != None:
			out.append(" DEFAULT ")
			out.append(str(field.dbDefault))
		elif field.dbIdentity:
			out.append(' IDENTITY')

		if field.dbNulls:
			out.append(' NULL')
		else:
			out.append(' NOT NULL')

		if field.dbForeignTable != None:
			tableStructure = field.dbForeignTable(env)
			out.append(' REFERENCES [')
			out.append(tableStructure.dbTable)
			out.append('] ([')
			if field.dbForeignKey != None:
				out.append(tableStructure.allFields[field.dbForeignKey].dbName)
			else:
				out.append(field.dbName)
			out.append('])')

		out.append(',\n')

	PK = [record.allFields[fieldName].dbName
	  for fieldName in fields
	  if record.allFields[fieldName].dbPrimaryKey]
	if (len(PK) > 0):
		out.append('PRIMARY KEY CLUSTERED ([')
		out.append('],['.join(PK))
		out.append(']),\n')

	for fieldName in fields:
		field = record.allFields[fieldName]
		if field.dbUnique and not field.dbPrimaryKey:
			out.append('UNIQUE ([')
			out.append(field.dbName)
			out.append(']),\n')

	if record.dbConstraints != '':
		out.append(record.dbConstraints)

	# Remove comma from last entry.
	out[-1] = out[-1][0:len(out[-1])-2]

	out.append('\n);\n\n')

	for fieldName in fields:
		field = record.allFields[fieldName]
		if not (field.dbIndexed and not field.dbPrimaryKey):
			continue
		out.append('CREATE')
		if field.dbUnique:
			out.append(' UNIQUE')
		out.append(' INDEX [idx_')
		out.append(field.dbName)
		out.append('] ON [')
		out.append(record.dbTable)
		out.append('] ([')
		out.append(field.dbName)
		out.append(']);\n')

	if hasattr(record, 'dbDynamicTable') and record.dbDynamicTable:
		out.append('\nCREATE TABLE [')
		out.append(record.dbPropertyTable)
		out.append('] (\n')

		for fieldName in fields:
			field = record.allFields[fieldName]

			if not field.dbPrimaryKey:
				continue

			out.append('[')
			out.append(field.dbName)
			out.append('] ')
			out.append(field.dbType)

			if field.dbType.endswith('char'):
				out.append('(')
				# Deal with differences between database length and HTML maxlength.
				if field.type == 'mac':
					out.append('12')
				elif field.type == 'phone':
					out.append('10')
				else:
					out.append(str(field.maxlength))

				out.append(')')

			if field.dbNulls:
				out.append(' NULL')
			else:
				out.append(' NOT NULL')

			out.append(',\n')

		out.append('[')
		out.append(record.propertyNameColumn)
		out.append('] varchar(255) NOT NULL,\n')
		out.append('[')
		out.append(record.propertyValueColumn)
		out.append('] varchar(4000) NULL,\n')
		out.append('PRIMARY KEY CLUSTERED ([')
		out.append('],['.join([record.allFields[fieldName].dbName
		  for fieldName in fields
		  if record.allFields[fieldName].dbPrimaryKey]))
		out.append('],[')
		out.append(record.propertyNameColumn)
		out.append(']),\n')
		out.append('FOREIGN KEY ([')
		out.append('],['.join([record.allFields[fieldName].dbName
		  for fieldName in fields
		  if record.allFields[fieldName].dbPrimaryKey]))
		out.append(']) REFERENCES [')
		out.append(record.dbTable)
		out.append(']\n')
		out.append(');\n')

	if record.dbMiscellaneous != '':
		out.append(record.dbMiscellaneous)

	return ''.join(out)

e = env.env(None)
tables = []

#
# NOTE:
#
# Only one instance of a dynamic table should be added here.
# This will be the top-level table with the non-dynamic properties.
#

# Round 1
if e.domain:
	import structures.Domain
	tables.append(structures.Domain.Domain)
if e.equipmentClass:
	import structures.EquipmentClass
	tables.append(structures.EquipmentClass.EquipmentClass)
if e.externalSystem:
	import structures.ExternalSystem
	tables.append(structures.ExternalSystem.ExternalSystem)
if e.group:
	import structures.Group
	tables.append(structures.Group.Group)
if e.manufacturer:
	import structures.Manufacturer
	tables.append(structures.Manufacturer.Manufacturer)
if e.projectStatus:
	import structures.ProjectStatus
	tables.append(structures.ProjectStatus.ProjectStatus)
if e.provider:
	import structures.Provider
	tables.append(structures.Provider.Provider)
if e.region:
	import structures.Region
	tables.append(structures.Region.Region)

# Round 2
if e.abuseHandler:
	import structures.AbuseHandler
	tables.append(structures.AbuseHandler.AbuseHandler)
if e.equipmentType:
	import structures.EquipmentType
	tables.append(structures.EquipmentType.EquipmentType)
if e.internalUser:
	import structures.InternalUser
	tables.append(structures.InternalUser.InternalUser)
if e.masterAccount:
	import structures.MasterAccount
	tables.append(structures.MasterAccount.MasterAccount)
if e.problemCategory:
	import structures.ProblemCategory
	tables.append(structures.ProblemCategory.ProblemCategory)
if e.project:
	import structures.Project
	tables.append(structures.Project.Project)
if e.task:
	import structures.Task
	tables.append(structures.Task.Task)
if e.terminal:
	import structures.Terminal
	tables.append(structures.Terminal.Terminal)
if e.web:
	import structures.Web
	tables.append(structures.Web.Web)

# Round 3
if e.abuseEvent:
	import structures.AbuseEvent
	tables.append(structures.AbuseEvent.AbuseEvent)
if e.abuseGracePeriod:
	import structures.AbuseGracePeriod
	tables.append(structures.AbuseGracePeriod.AbuseGracePeriod)
if e.accountType:
	import structures.AccountType
	tables.append(structures.AccountType.AccountType)
if e.blacklistEntry:
	import structures.BlacklistEntry
	tables.append(structures.BlacklistEntry.BlacklistEntry)
if e.dnsRecord:
	import structures.DNSRecord
	tables.append(structures.DNSRecord.DNSRecord)
if e.dslAccount:
	import structures.DSLAccount
	tables.append(structures.DSLAccount.DSLAccount)
if e.dslBlock:
	import structures.DSLBlock
	tables.append(structures.DSLBlock.DSLBlock)
if e.dslChannel:
	import structures.DSLChannel
	tables.append(structures.DSLChannel.DSLChannel)
if e.greylistTriplet:
	import structures.GreylistTriplet
	tables.append(structures.GreylistTriplet.GreylistTriplet)
if e.networkDevice:
	import structures.NetworkDevice
	tables.append(structures.NetworkDevice.NetworkDevice)
if e.mailEvent:
	import structures.MailEvent
	tables.append(structures.MailEvent.MailEvent)
if e.mailSenderCacheEntry:
	import structures.MailSenderCacheEntry
	tables.append(structures.MailSenderCacheEntry.MailSenderCacheEntry)
if e.msAddressBookIndividual:
	import structures.MSAddressBookIndividual
	tables.append(structures.MSAddressBookIndividual.MSAddressBookIndividual)
if e.msAddressBookGroupEntry:
	import structures.MSAddressBookGroupEntry
	tables.append(structures.MSAddressBookGroupEntry.MSAddressBookGroupEntry)
if e.msNote:
	import structures.MSNote
	tables.append(structures.MSNote.MSNote)
if e.problem:
	import structures.Problem
	tables.append(structures.Problem.Problem)
if e.projectComment:
	import structures.ProjectComment
	tables.append(structures.ProjectComment.ProjectComment)
if e.projectUser:
	import structures.ProjectUser
	tables.append(structures.ProjectUser.ProjectUser)
if e.subAccount:
	import structures.SubAccount
	tables.append(structures.SubAccount.SubAccount)
if e.subWeb:
	import structures.SubWeb
	tables.append(structures.SubWeb.SubWeb)
if e.subWebUser:
	import structures.SubWebUser
	tables.append(structures.SubWebUser.SubWebUser)
if e.taskDate:
	import structures.TaskDate
	tables.append(structures.TaskDate.TaskDate)
if e.taskException:
	import structures.TaskException
	tables.append(structures.TaskException.TaskException)
if e.taskUser:
	import structures.TaskUser
	tables.append(structures.TaskUser.TaskUser)
if e.terminalPhone:
	import structures.TerminalPhone
	tables.append(structures.TerminalPhone.TerminalPhone)
if e.troubleTicket:
	import structures.TroubleTicket
	tables.append(structures.TroubleTicket.TroubleTicket)
if e.troubleTicketComment:
	import structures.TroubleTicketComment
	tables.append(structures.TroubleTicketComment.TroubleTicketComment)
if e.wantAdCategory:
	import structures.WantAdCategory
	tables.append(structures.WantAdCategory.WantAdCategory)
if e.wantAdEntry:
	import structures.WantAdEntry
	tables.append(structures.WantAdEntry.WantAdEntry)
if e.webRedirect:
	import structures.WebRedirect
	tables.append(structures.WebRedirect.WebRedirect)
if e.webUser:
	import structures.WebUser
	tables.append(structures.WebUser.WebUser)
if e.wirelessAccount:
	import structures.WirelessAccount
	tables.append(structures.WirelessAccount.WirelessAccount)
if e.whitelistEntry:
	import structures.WhitelistEntry
	tables.append(structures.WhitelistEntry.WhitelistEntry)

# FIXME: Eventually, these SQL commands should be run on the database instead of being printed.

for table in tables:
	print create_table(e, table(e))

print "GO\n"

for table in tables:
	_instance = table(e)
	trigger = _instance.dbTriggers(e)
	if trigger:
		print _instance.dbTriggers(e)
