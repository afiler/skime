from datamodules.action import action
from datamodules.DataModule import DataModule

from structures.MasterAccount import MasterAccount
from structures.DSLAccount import DSLAccount
from structures.SubAccount import SubAccount
from structures.SubWeb import SubWeb
from structures.Web import Web
from structures.WebRedirect import WebRedirect
from structures.WirelessAccount import WirelessAccount

class CustomerRecord(DataModule):

	def __init__(self, env):
		self.moduleName = 'CustomerRecord'

		self.actions = {"edit":		action(loadFromDb=1, editable=1, nextAction="update", nextTitle="Save"),
				"view":		action(loadFromDb=1, editable=0, nextAction="edit", nextTitle="Edit"),
				"verify":	action(loadFromForm=1, editable=1, nextAction="update", nextTitle="Save"),
				"update":	action(loadFromDb=1, editable=0, preFunction=self.dbSave, chainAction="view") }

		self.structures = {MasterAccount: {}, SubAccount: {}, Web: {WebRedirect: {}}, SubWeb: {}}
		self.rootStructure = MasterAccount
		self.extraVars = []
		self.arrangement = 'auto'

		self.data = []

		self.pageTitle = "Customer Record"

