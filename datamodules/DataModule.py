from display.html import *

class DataModule:

	def __init__(self, env):
		self.data = []

	def handleAction(self, env, actionString):
		self.env = env
		self.hasCriterion = False

		assert self.actions.has_key(actionString), "Unrecognized action: " + actionString
		a = self.actions[actionString]

		if a.preFunction:
			a.preFunction(env)

		if a.chainAction:
			a = self.actions[a.chainAction]

		if a.loadFromForm: self.formLoad(env)
		elif a.loadFromDb:
			self.setCriterion()
			self.setQueryFromCriterion()
			self.dbLoad(env, self.query)
		elif a.queryFromForm:
			query = self.buildQueryFromForm(env)
			self.dbLoad(env, query)
		else: self.nullLoad(env)

		return self.getHtml(env, a, moduleName=self.moduleName, arrangement=self.arrangement)

	def getHtml(self, env, a, moduleName=None, arrangement=None):
		out = []

		# We don't want to show the primary key(s) on the joined structures
		# since this information is already available from the root structure.
		keys = self.rootStructure(env).findPK()
		for structures in [x for x in self.data if x]:
			for structure in structures:
				if not isinstance(structure, self.rootStructure):
					for key in keys:
						structure.allFields[key].visible = False

		# Print out title + set of accounts for each type of account
		for structure in [x for x in self.data if x]:
			accountArea = []

			if arrangement == 'row' or (not arrangement and structure[0].defaultFieldArrangement == 'row'):
				accountArea.append(structure[0].getFormTitleRow(editable=a.editable))

			if arrangement != 'auto':
				accountArea.append(structure[0].getFormSet(env, structure, a.editable, arrangement=arrangement))

			# If this is the root structure, don't stick a title on
			if self.rootStructure and isinstance(structure[0], self.rootStructure):
				if arrangement == 'auto':
					accountArea.append(structure[0].getFormSet(env, structure, a.editable, arrangement='form'))
				out.append(table(structure[0].formTitle, ''.join(accountArea), cellpadding=3))
			else:
				if arrangement == 'auto':
					accountArea.append(structure[0].getFormTitleRow(editable=a.editable, arrangement='row'))
					accountArea.append(structure[0].getFormSet(env, structure, a.editable, arrangement='row'))
				out.append(region(structure[0].groupTitle, table(structure[0].formTitle, ''.join(accountArea), cellpadding=3)))

		out.append('<p>');
		# TODO: These should probably be rolled into something javascripty to allow buttons to do different things
		if a.nextTitle:
			out.append(button("submit", value=a.nextTitle, content=a.nextTitle))

		out.append(hiddenInput("action", value=a.nextAction))
		out.append(hiddenInput("module", value=moduleName))

		if self.hasCriterion:
			count = 0
			for x, y in zip(self.criterion, self.value):
				out.append(hiddenInput('criterion.'+str(count), value=x))
				out.append(hiddenInput('value.'+str(count), value=y))
				count = count + 1

		out.append('</p>');

		out.append(''.join([hiddenInput(x, value=env.fieldStorage[x]) for x in [x for x in self.extraVars if env.fieldStorage.has_key(x)]]))

		return form('<p>' + span(self.pageTitle, 'page_header') + '</p>\n' + ''.join(out), action=env.req.uri)

	def buildQueryFromForm(self, env):
		query = {}
		for structure in self.structures:
			query.update(structure.buildQuery(env))
		return query

	def setQueryFromCriterion(self):
		self.query = {}
		for x, y in zip(self.criterion, self.value):
			self.query[x] = y

	def setCriterion(self):
		fs = self.env.fieldStorage

		if fs.has_key('criterion') and fs.has_key('value'):
			if fs.has_key('criterion.0') and fs.has_key('value.0'):
				raise RuntimeError, 'Single and multiple criterion/value sets found.'
			self.criterion = [self.env.fieldStorage['criterion']]
			self.value = [self.env.fieldStorage['value']]
			self.hasCriterion = True
		elif fs.has_key('criterion.0') and fs.has_key('value.0'):
			count = 0
			self.criterion = []
			self.value = []
			self.hasCriterion = True
			while fs.has_key('criterion.'+str(count)) and fs.has_key('value.'+str(count)):
				self.criterion.append(fs['criterion.'+str(count)])
				self.value.append(fs['value.'+str(count)])
				count = count + 1
		else:
			raise RuntimeError, 'There is no criterion/value set found.'

	def nullLoad(self, env):
		self.nullLoadCore(env, self.structures)

	def nullLoadCore(self, env, structures):
		for structure in self.structures:
			self.data.append([structure(env)])

			if structures[structure]: self.nullLoadCore(env, stuctures[structure])

	def formLoad(self, env):
		self.formLoadCore(env, self.structures)

	def formLoadCore(self, env, structures):
		for structure in structures:
			#env.req.write('<p>Structure: ' + htmlEscape(structure) + '</p>')
			#x = list(structure.formLoad(env))
			#env.req.write('<p>Record: ' + htmlEscape(str(x)) + '</p>')
			self.data.append(list(structure.formLoad(env)))

			if structures[structure]: self.formLoadCore(env, structures[structure])


	def dbLoad(self, env, query):
		self.dbLoadCore(env, self.structures, env.con, query)

	def dbLoadCore(self, env, structures, con, query):
		for structure in structures:
			structureSet = list(structure.dbLoad(env, con, query=query))
			#env.req.write('<p>Structure: ' + htmlEscape(structureSet) + '</p>')
			self.data.append(structureSet)

			if structures[structure]:
				for record in structureSet:
					PK = record.findPK()

					assert len(PK) >= 1, 'Only tables with one or more primary keys can be recursed here'

					joinQuery = {}
					for key in PK:
						joinQuery[record.allFields[key].dbName] = record.values[key]

					self.dbLoadCore(env, structures[structure], con, joinQuery)

	def TEMPdbLoadCore(self, env, structures, cur, query):
		for structure in structures:
			structureSet = structure.dbLoad(env, cur, query=query)

			for record in structureSet:
				self.data.append([record])

				if structures[structure]:
					PK = record.findPK()
					if len(PK) != 1:
						assert 0, 'Only tables with single primary keys can be recursed here'
					self.dbLoadCore(env, structures[structure], cur, {PK[0].dbName: record.values[PK[0].dbName]})

			self.data.append(structureSet)

	def dbSave(self, env):
		# FIXME: dbSave is not yet implemented.
		#raise NotImplementedError, 'This function is not yet implemented.'

		self.formLoad(env)

		for structure in self.data:
			env.req.write('<p>' + htmlEscape('Structure = ' + str(structure)) + '</p>')
			for record in structure:
				env.req.write('<p>' + htmlEscape('Record = ' + str(record)) + '</p>')
				record.dbSave(env)

