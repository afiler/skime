from structures.Structure import Structure

from structures.MasterAccount import MasterAccount
from structures.DSLAccount import DSLAccount
from structures.SubAccount import SubAccount
from structures.SubWeb import SubWeb
from structures.Web import Web
from structures.WebRedirect import WebRedirect
from structures.WirelessAccount import WirelessAccount

import util

from display.html import *

class Search(Structure):

	def rowFieldHolder(self, label, guts):
		# XXX: This is crap

		if self.values.has_key('CustomerID'):
			return cell('<a href="index.py?module=CustomerRecord&amp;action=view&amp;criterion=CustomerID&amp;value=' + str(self.values['CustomerID']) +'">' + guts + '</a>')
		else:
			return cell(guts)

	# Class Method
	def buildQuery(cls, env, max=1):
		"""Returns a query set based on data filled in form"""
		instance = cls(env)

		if env.fieldStorage.has_key(instance.formPrefix+".count"):
			count = int(env.fieldStorage[instance.formPrefix+".count"])
		else:
			raise RuntimeError, 'There is no form value for ' + instance.formPrefix + '.count.'

		query = {}
		for i in range(count):
			if i > max: raise RuntimeError, 'Too many form entries were found.'

			for (table, None, field) in instance.fieldSet:
				formFieldTitle = instance.formPrefix+'.'+field+'.'+str(i)
				if env.fieldStorage.has_key(formFieldTitle) and len(env.fieldStorage[formFieldTitle].strip()) > 0:
					query[(table, field)] = env.fieldStorage[formFieldTitle]

		return query
	buildQuery = classmethod(buildQuery)

	# Static
	def dbLoad(cls, env, con, query=None, where=None, orderBy=None, reverseSort=False, max=None):
		if where == None: where = ''
		con = env.con
		args  = []
		s = cls(env)
		(fieldSet, tableNames, joins) = (s.fieldSet, s.tableNames, s.joins)

		sql =	'SELECT "' + '","'.join([table+'"."'+field.dbName for (table, field, name) in fieldSet]) \
			+ '" FROM "' + '","'.join(tableNames) + '"'

		# XXX: The rest of this could really just come from dbLoad in Structure
		instance = cls(env)
		if query != None:
			for (table, key) in query:
				if instance.allFields.has_key(key) and instance.allFields[key].present:
					if where != '':
						where += ' AND '
					where += '"' + table + '"."' + instance.allFields[key].dbName + '" LIKE ?'
					args.append(query[(table, key)])
			assert len(args) > 0, 'query != None, but no fields in query were present (or query == {})' + str(query)

		sql += ' WHERE ' + ' AND '.join(['"'+x+'"."'+z+'" = "'+y+'"."'+z+'"' for x, y, z in joins])

		if where: sql += ' AND ' + where

		if orderBy != None and len(orderBy) > 0:
			sql += ' ORDER BY "' + '","'.join([instance.allFields[x].dbName for x in orderBy]) + '"'
			if reverseSort:
				sql += ' DESC'

		cur = con.cursor()

		util.CursorWrapper.CursorWrapper.execute(cur, sql, args)
		sql = None
		args = None

		# XXX: This is a work-around for DBAPI 1.0 compatibility.
		try:
			assert max == None or max > 0, 'max is not greater than zero'
			rowcount = cur.rowcount
			if (max != None and rowcount > max):
				raise RuntimeError, "A maximum " + str(max) + " rows were requested but " + str(rowcount) + " were found."
		except AttributeError:
			pass

		while 1:
			try:
				row = cur.fetchone()
			except:
				break
			if row != None:
				rec = cls(env)
				rec.dbLoadRecord(row)
				yield rec
			else:
				break

		cur.close()
	dbLoad = classmethod(dbLoad)

	def dbLoadRecord(self, row):
		for x, y in zip([name for (table, field, name) in self.fieldSet], row):
			self.values[x] = y

	def getFieldsAndTables(self, fields, joiner=None, PKs=None):
		fieldSet = []
		tableNames = []
		joins = []

		for field in fields:
			rec = field[0](self.env)

			# If this has been joined on something, add the tables to the join list
			# Theoretically, this should handle multiple PKs
			if joiner and PKs:
				for PK in PKs:
					if joins.count((joiner, rec.dbTable, PK.dbName)) < 1:
						joins.append((joiner, rec.dbTable, PK.dbName))

			#fieldNames.append('[' + rec.dbTable + '].[' + rec.allFields[field[1]].dbName + ']')
			fieldSet.append((rec.dbTable, rec.allFields[field[1]], field[1]))

			# This avoids inserting multiple table names as long as fields is created normally (e.g. not like MasterAccount: {SubAccount: {MasterAccount: ""}}}
			if tableNames.count(rec.dbTable) < 1: tableNames.append(rec.dbTable)

			if fields[field]:
				(moreFields, moreTables, moreJoins) = self.getFieldsAndTables(fields[field], rec.dbTable, [rec.allFields[x] for x in rec.findPK()])
				fieldSet.extend(moreFields)
				tableNames.extend(moreTables)
				joins.extend(moreJoins)

		return (fieldSet, tableNames, joins)

	def getFormTitleRow(self, arrangement=None, editable=False):
		r"""
		Get a table row of titles for all columns.

		@param arrangement The arrangement to get the title row for. If
		                   no @a arrangement is provided, the
		                   @c defaultFieldArrangement will be used.
		@param editable    Will the form that this title row is for be editable?

		@remarks This fails if a field doesn't have a title because
		         the HTML widgetry really wants content.
		"""

		if not arrangement:
			arrangement = self.defaultFieldArrangement

		out = []

		for fieldName in self.getPrintingFields(arrangement):
			out.append(cell(self.allFields[fieldName].title, \
			            'rowset_header'))

		return row(''.join(out))

	## protected:
	def getFormGuts(self, env, editable, arrangement, index):
		r"""
		Get the "guts" of the form.

		Basically, this method calls getFormFieldGuts() for each
		printing field (from getPrintingFields()).

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

		for fieldName in self.getPrintingFields(arrangement):
			out.append(self.getFormFieldGuts(env, editable, \
			                             fieldName, \
			                             arrangement, \
			                             index))

		return ''.join(out)
	## public:
