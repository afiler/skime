import sys

from devices.Router import Router
import re
import env, util
from customerRecord import CustomerRecord
from structures.MasterAccount import MasterAccount
from structures.DSLAccount import DSLAccount
from structures.SubAccount import SubAccount
from structures.SubWeb import SubWeb
from structures.Web import Web
from structures.WebRedirect import WebRedirect
from structures.WirelessAccount import WirelessAccount

def getCid(env, atmInt):
	sql = 'SELECT "CustomerID" FROM "DSLAccounts" WHERE "RouterPort" LIKE ?'
	args = ['%' + str(atmInt) + '%']

	cur = env.con.cursor()
	util.CursorWrapper.CursorWrapper.execute(cur, sql, args)

	return [x[0] for x in cur.fetchall()]

r = Router('10.0.0.1', password='password', enablePassword='password', timeout=60)

config = r.getRunningConfiguration()
r.close()

configs = config.split('!')
reAtmInt = re.compile(r'interface (ATM\S+)')
reIntPvcPart = re.compile(r'interface ATM\d+/(\S+)')
reUnnum = re.compile(r'ip unnumbered (\S+)')
reRbe = re.compile(r'atm route-bridged ip')
rePvc = re.compile(r'pvc (\S+)')
reVbr = re.compile(r'vbr-nrt (\S+) (\S+)')

founds = []
notFounds = []

for section in configs:
	if not reAtmInt.search(section):
		continue

	atmInt = reAtmInt.search(section).group(1)
	intPvcPart = reIntPvcPart.search(section).group(1)

	if reUnnum.search(section):
		unnum = reUnnum.search(section).group(1)
	else:
		unnum = 0

	if reRbe.search(section):
		rbe = reRbe.search(section).group()
	else:
		rbe = 0

	if rePvc.search(section):
		pvc = rePvc.search(section).group(1)
	else:
		pvc = 0

	if reVbr.search(section):
		vbr = (reVbr.search(section).group(1), reVbr.search(section).group(2))
	else:
		vbr = (0,0)

	e = env.env(None, 'wiktel.com')
	cids = getCid(e, intPvcPart)
	if cids:
		cr = CustomerRecord()
		cr.dbLoad(e, {'CustomerID': cids[0]})

		ma = cr.data[0][0]
		founds.append("ATM Int: " + str(atmInt) + ", Unnumbered Int: " + str(unnum) + ", RBE: " + str(rbe) + ", PVC: " + str(pvc) + ", VBR: " + str(vbr) + "\n" +
			"Name: " + ma.values['FirstName'] + " " + ma.values['LastName'] + "    Company: " + ma.values['Company'] + "   Billing Number: " + ma.values['BillingNumber'] + "\n")
	else:
		notFounds.append("ATM Int: " + str(atmInt) + ", Unnumbered Int: " + str(unnum) + ", RBE: " + str(rbe) + ", PVC: " + str(pvc) + ", VBR: " + str(vbr) + "\n" +
			'No record found for interface ' + atmInt + '\n')

f = file("dsl.txt", 'w')
f.write("-- Not Found --\n")
for x in notFounds: f.write(x)

f.write("\n")
f.write("-- Found --\n")
for x in founds: f.write(x)
