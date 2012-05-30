import re
import util.CursorWrapper
import devices.Router

class RouterDSL:
	def __init__(self, e):
		self.env = e
		self.router = devices.Router.Router('dsl.router.example.com', username='user', password='password', timeout=60)
		self.actions = {'enabledsl': RouterDSL.enableDSL, 'disabledsl': RouterDSL.disableDSL, 'setfiltered': RouterDSL.setFiltered, 'setunfiltered': RouterDSL.setUnfiltered}

	def handleAction(self, e, action):
		return self.actions[action](self) + self.getReturnPage()

	def getReturnPage(self):
		if self.env.fieldStorage.has_key("returnPage"):
    			out = '<a href="%s">Return to account page</a>' % self.env.fieldStorage["returnPage"]
			return out
		else:
			return ''

	def enableDSL(self):
		interface = self.env.fieldStorage["interface"]
		dslid = self.env.fieldStorage["dslid"]
		if self.env.fieldStorage.has_key("description"): description = self.env.fieldStorage["description"]
		else: description = None

		ifConfig = self.router.enableInterface(interface, description)
		self.router.writeRunningConfiguration()

		out = []
		out.append("<pre>"+ifConfig+"</pre>")
		out.append("<ul>")
		out.append("<li>The interface %s on the DSL router has been enabled.</li>" % interface)
		sql = "UPDATE DSLAccounts SET Active = 1 WHERE DSLAccountID = ?"
		args = [dslid]
		util.CursorWrapper.CursorWrapper.execute(self.env.con.cursor(), sql, args)
		out.append("<li>The database has been updated to reflect this change.</li>")
		out.append("</ul>")
		return "\n".join(out)

	def disableDSL(self):
		interface = self.env.fieldStorage["interface"]
		dslid = self.env.fieldStorage["dslid"]

		if self.env.fieldStorage.has_key("description"): description = self.env.fieldStorage["description"]
		else: description = None

		ifConfig = self.router.disableInterface(interface, description)
		self.router.writeRunningConfiguration()

		out = []
		out.append("<pre>"+ifConfig+"</pre>")
		out.append("<ul>")
		out.append("<li>The interface %s on the DSL router has been disabled.</li>" % interface)
		sql = "UPDATE DSLAccounts SET Active = 0 WHERE DSLAccountID = ?"
		args = [dslid]
		util.CursorWrapper.CursorWrapper.execute(self.env.con.cursor(), sql, args)
		out.append("<li>The database has been updated to reflect this change.</li>")
		out.append("</ul>")
		return "\n".join(out)

	def setFiltered(self):
		interface = self.env.fieldStorage["interface"]
		dslid = self.env.fieldStorage["dslid"]

		if self.env.fieldStorage.has_key("description"): description = self.env.fieldStorage["description"]
		else: description = None

		ifConfig = self.router.setFiltered(interface, description)
		self.router.writeRunningConfiguration()

		out = []
		out.append("<pre>"+ifConfig+"</pre>")
		out.append("<ul>")
		out.append("<li>The interface %s on the DSL router has been changed to filtered.</li>" % interface)
		sql = "UPDATE DSLAccounts SET AccountTypeID = (SELECT ReverseTypeID FROM DSLAccounts JOIN AccountTypes ON DSLAccounts.AccountTypeID = AccountTypes.AccountTypeID WHERE DSLAccountID=?) WHERE DSLAccountID = ?"
		args = [dslid, dslid]
		util.CursorWrapper.CursorWrapper.execute(self.env.con.cursor(), sql, args)
		out.append("<li>The database has been updated to reflect this change.</li>")
		out.append("</ul>")
		return "\n".join(out)

	def setUnfiltered(self):
		interface = self.env.fieldStorage["interface"]
		dslid = self.env.fieldStorage["dslid"]

		if self.env.fieldStorage.has_key("description"): description = self.env.fieldStorage["description"]
		else: description = None

		ifConfig = self.router.setUnfiltered(interface, description)
		self.router.writeRunningConfiguration()

		out = []
		out.append("<pre>"+ifConfig+"</pre>")
		out.append("<ul>")
		out.append("<li>The interface %s on the DSL router has been changed to unfiltered.</li>" % interface)
		sql = "UPDATE DSLAccounts SET AccountTypeID = (SELECT ReverseTypeID FROM DSLAccounts JOIN AccountTypes ON DSLAccounts.AccountTypeID = AccountTypes.AccountTypeID WHERE DSLAccountID=?) WHERE DSLAccountID = ?"
		args = [dslid, dslid]
		util.CursorWrapper.CursorWrapper.execute(self.env.con.cursor(), sql, args)
		out.append("<li>The database has been updated to reflect this change.</li>")
		out.append("</ul>")
		return "\n".join(out)
