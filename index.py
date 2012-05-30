import sys
#sys.path.append('/srv/www/skime/html')

from mod_python import apache
from mod_python import util

import base64
import re

import datamodules.CustomerRecord
import datamodules.GeneralSearch
import env

import structures.InternalUser

username = ""
name = ""

def formGet(env, varName):
	if env.fieldStorage.has_key(varName):
		var = env.fieldStorage[varName]
	else:
		var = None

	return var

def handler(req):
	e = env.env(req, 'provider1.example.com')
	auth = authenhandler(req)
	if auth != apache.OK: return(auth)
	
	module = formGet(e, 'module')
	action = formGet(e, 'action')
	if action: action = action.lower()

	# Redirect to SSL URL
	if e.requireSSL and req.server.port != 443:
		req.headers_out['Location'] = 'https://' + req.hostname + req.unparsed_uri
		req.status = apache.HTTP_MOVED_PERMANENTLY
		req.content_type = 'text/html'
		req.send_http_header()
		req.write("""<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<link href="styles.css" media="all" rel="stylesheet" type="text/css" />
		<title>Redirecting...</title>
	</head>
	<body>
		<h1>Redirecting...</h1>
		<p>You are being redirected to: <a href="%(dest)s">%(dest)s</a></p>
	</body>
</html>""" % {'dest': req.headers_out['Location'] })
		return apache.OK

	req.content_type = 'text/html'
	req.send_http_header()

	req.write("""<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<link href="styles.css" media="all" rel="stylesheet" type="text/css" />
		<title>Skime</title>
	</head>
	<body>
		<table class="top_header_table" summary="Top Header">
			<colgroup>
				<col width="1*" />
				<col width="*" />
			</colgroup>
			<tr class="top_header_row1">
				<td style="width: 1*;"><a href="/"><img src="images/logo.gif" alt="Skime" /></a></td>
				<td class="top_header_text">Skime</td>
			</tr>
			<tr class="top_header_row2">
				<td colspan="2">User: """ + name + ' (' + username + ')' + """</td>
			</tr>
		</table>
""")

	if not module:
		module = 'GeneralSearch'
		action = 'searchform'

	try:
		modFile = __import__('datamodules.'+module)
		modCls = eval('modFile.'+module+'.'+module)
		mod = modCls(e)
		req.write(mod.handleAction(e, action))
	except:
		req.write('Uh-oh.  Couldn\'t even load the standard module')

	req.write("</body></html>\n")

	return apache.OK

def authenhandler(req):
	global username, name
	e = env.env(req, 'provider1.example.com')
	
	password = req.get_basic_auth_pw()
	username = req.user
	
	if (username and password):
		for user in structures.InternalUser.InternalUser.dbLoad(e, e.con, query={'Username': username, 'Password': password}, orderBy=('Username',)):
			# Reverify password because of possible database case-insensitivity.
			if user.values['Username'].lower() == username.lower() and user.values['Password'] == password:
				name = user.values['Name']
				break

	if (name):
		return apache.OK
	else:
		return apache.HTTP_UNAUTHORIZED