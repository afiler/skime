from datamodules.action import action
from datamodules.DataModule import DataModule

from structures.SubWeb import SubWeb
from structures.Web import Web
from structures.WebRedirect import WebRedirect
from structures.WebUser import WebUser

class WebRecord(DataModule):

	def __init__(self, env):
		self.moduleName = 'WebRecord'

		self.actions = {"edit":		action(loadFromDb=1, editable=1, nextAction="update", nextTitle="Save"),
				"view":		action(loadFromDb=1, editable=0, nextAction="edit", nextTitle="Edit"),
				"verify":	action(loadFromForm=1, editable=1, nextAction="update", nextTitle="Save"),
				"update":	action(loadFromDb=1, editable=0, preFunction=self.dbSave, chainAction="view") }

		self.structures = {Web: {WebUser: {}, WebRedirect: {}, SubWeb: {}}}
		self.rootStructure = Web
		self.extraVars = []
		self.arrangement = 'auto'

		self.data = []

		self.pageTitle = "Web Record"
