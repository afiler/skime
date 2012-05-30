class action:

	def __init__(self, editable=0, queryFromForm=0, loadFromDb=0, loadFromForm=0, nextModule=None, nextAction=None, nextTitle=None, nextLink=None, preFunction=None, chainAction=None):
		self.editable=editable
		self.queryFromForm=queryFromForm
		self.loadFromDb=loadFromDb
		self.loadFromForm=loadFromForm
		self.nextModule=nextModule
		self.nextAction=nextAction
		self.nextTitle=nextTitle
		self.nextLink=nextLink
		self.preFunction=preFunction
		self.chainAction=chainAction
