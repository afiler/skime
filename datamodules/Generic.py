from datamodules.action import action
from datamodules.DataModule import DataModule

class Generic(DataModule):

	def __init__(self, env):
		self.moduleName = 'Generic'

		structureName = env.fieldStorage['structure']
		structureFile = __import__('structures.'+structureName)
		structureCls = eval('structureFile.'+structureName+'.'+structureName)
		structureCls.defaultFieldArrangement = 'list'

		self.actions = {"edit":		action(loadFromDb=1, editable=1, nextAction="update", nextTitle="Save"),
				"view":		action(loadFromDb=1, editable=0, nextAction="edit", nextTitle="Edit"),
				"verify":	action(loadFromForm=1, editable=1, nextAction="update", nextTitle="Save"),
				"update":	action(loadFromDb=1, editable=0, preFunction=self.dbSave, chainAction="view") }

		self.structures = {structureCls: {}}
		self.rootStructure = structureCls
		self.extraVars = ['structure', 'arrangement']

		if env.fieldStorage.has_key('arrangement'): self.arrangement =  env.fieldStorage['arrangement']
		else: self.arrangement = None

		self.data = []

		self.pageTitle = ""

	def getHtml(self, env, a, moduleName=None, arrangement=None):

		if len(self.data[0]) > 1:
			self.pageTitle = self.data[0][0].groupTitle
		else:
			self.pageTitle = self.data[0][0].formTitle

		return DataModule.getHtml(self, env, a, moduleName=moduleName, arrangement=arrangement)
