r"""
HTML Display Helper Functions

This collection of functions exists to make HTML generation easier.
It uses the XHTML 1.0 Strict standard.
http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd

@author Andy Filer \<andyf\@wiktel.com\>
@author Richard Laager \<rlaager\@wiktel.com\>
"""

import math

# HTML Escaping
def htmlEscape(text, convertNewlines=True):
	r"""
	Replaces ASCII entities with HTML entity codes, removes whitespace,
	normalizes line endings, and optionally converts newlines to \<br /\>
	tags.

	This function removes the ASCII entities @c \&, @c \<, @c \>, and @c "
	and replaces them with the HTML entities @c \&amp;, @c \&lt;, @c \&gt;,
	and @c \&quot; so they display properly on the web. It removes any
	external whitespace in @a text and converts CRs and CRLFs to LFs. If
	@a convetNewlines is true, it will replace all LFs with \<br /\> tags.

	@param text            The text to be changed.
	@param convertNewlines If true LFs will be converted to \<br /\>.
	"""

	if text == None:
		return ''

	text = str(text).strip()

	text = text.replace('&', '&amp;')
	text = text.replace('<', '&lt;')
	text = text.replace('>', '&gt;')
	text = text.replace('"', '&quot;')

	# Normalize Line-Endings
	text = text.replace('\015\n', '\n')
	text = text.replace('\015', '\n')

	if convertNewlines:
		text = text.replace('\n', '<br />')

	return text

# Start HTML Widgets
def form(text, action=None, method='post'):
	r"""
	Creates an HTML form.

	This function creates an HTML form. It uses the @c action and
	@c method attributes to set the HTML attributes of the same names.

	@param text   The text inside the form. This will be the inputs of the
	              form itself.
	@param action The file handling the output from the form.
	@param method The HTTP method to use when submitting the form.

	@pre @a text must not be @c None or the emtpy string.
	@pre @a method must be @c get or @c post.
	"""

	assert text != None, 'text must not be None.'
	text = str(text)
	assert text != "", 'text must not be the empty string.'

	assert method == 'get' or method == 'post', \
	  'method must be "get" or "post".'

	if action == None:
		action = ''
	else:
		action = str(action)

	out = '<form'

	out += ' action="' + htmlEscape(action) + '"'
	out += ' method="' + htmlEscape(method) + '"'

	out += '>\n' + text + '</form>\n'

	return out

def table(summary, text, cellspacing=0, cellpadding=0):
	r"""
	Creates an HTML table.

	This function creates an HTML table. It uses the @c summary,
	@c cellspacing, and @c cellpadding attributes to set the HTML
	attributes of the same names. The text submitted will iunclude the row
	and cell elements along with the text to display.

	@param summary     The purpose of the content of the table.
	@param text        The rows, cells, and data to be inserted into the
	                   table.
	@param cellspacing The spacing between the table's cells.
	@param cellpadding The spacing within the table's cells.

	@pre @a summary must not be @c None or the empty string.
	@pre @a text must not be @c None or the empty string.
	@pre @a cellspacing must be an integer greater than or equal to zero.
	@pre @a cellpadding must be an integer greater than or equal to zero.
	"""

	assert summary != None, 'summary must not be None.'
	summary = str(summary)
	assert summary != "", 'summary must not be the empty string.'

	assert text != None, 'text must not be None.'
	text = str(text)
	assert text != "", 'text must not be the empty string.'

	try:
		cellspacing = int(cellspacing)
		assert (cellspacing >= 0), \
		       'cellspacing must be greater than or equal to zero.'
	except ValueError:
		assert 0, 'cellspacing must be convertable to an int.'

	try:
		cellspacing = int(cellspacing)
		assert (cellspacing >= 0), \
		       'cellpadding must be greater than or equal to zero.'
	except ValueError:
		assert 0, 'cellpadding must be convertable to an int.'

	return '<table summary="' + htmlEscape(summary) + '" cellspacing="' + \
	  str(cellspacing) + '" cellpadding="' + str(cellpadding) + '">\n' + \
	  text + '</table>\n'

def row(text):
	r"""
	Creates a table row.

	This function creates a table row, sets the style of and displays the
	specified text. The submitted @a text will include the cell elements as
	well as the text to be displayed.

	@param text This is the actual text to be inserted into the table.

	@pre @a text must not be @c None or the empty string.
	"""

	assert text != None, 'text must not be None.'
	text = str(text)
	assert text != "", 'text must not be the empty string.'

	return '<tr>' + text + '</tr>\n'

def cell(text, cssClass=None, colspan=1):
	r"""
	Creates a table cell and specifies which, if any, CSS class to use.

	@param text     The text to display in the table cell.
	@param cssClass The CSS class to use to display @a text.
	@param colspan  The number of columns to span.

	@pre @a cssClass must not be the empty string.
	@pre @a colspan must be na integer greater than zero.
	"""

	if text != None:
		text = str(text)

	if cssClass != None:
		cssClass = htmlEscape(cssClass)
	assert cssClass != "", 'cssClass must not be the empty string.'

	try:
		colspan = int(colspan)
		assert (colspan >= 0), \
		       'colspan must be greater than zero.'
	except ValueError:
		assert 0, 'colspan must be convertable to an int.'


	out = '<td'
	if cssClass != None:
		out += ' class="' + cssClass + '"'
	if colspan > 1:
		out += ' colspan="' + str(colspan) + '"'
	out += '>'

	if text != None:
		out += text

	out += '</td>'
	return out

def span(text, cssClass):
	r"""
	Groups inline elements in a document.

	This function groups inline elements in a document to apply a CSS
	class.

	@param text     The text to apply the css to.
	@param cssClass The CSS class to use to display @a text.

	@pre @a text must not be @c None or the empty string.
	@pre @a cssClass must not be @c None or the empty string.
	"""

	assert text != None, 'text must not be None.'
	text = str(text)
	assert text != "", 'text must not be the empty string.'

	assert cssClass != None, 'cssClass must not be None.'
	cssClass = htmlEscape(cssClass)
	assert cssClass != "", 'cssClass must not be the empty string.'

	return '<span class="' + cssClass + '">' + text + '</span>'

def button(name, type='submit', value=None, content=None, editable=True):
	r"""
	Creates a push button.

	This function creates a generic, form submit, or form reset push
	button.

	@param name     Specifies the unique name of the button.
	@param type     Type of button: @c submit, @c button, or @c reset.
	@param value    Value of the button which is sent to the server.
	@param content  Text or images to use to display the button.
	@param editable Determines whether or not the button data is
	                submitted to the server.

	@pre @a name must not be @c None or the empty string if @a editable
	     is true.
	@pre @a type must @c button, @c submit, or @c reset.
	"""

	if editable:
		assert name != None, 'name must not be None.'
		name = str(name)
		assert name != "", 'name must not be the empty string.'

	assert (type == 'button' or type == 'submit' or type == 'reset'), \
	  'Invalid button type: ' + type

	out = '<button type="' + type + '"'
	if editable:
		out += ' name="' + htmlEscape(name) + '"'
	if value != None:
		out += ' value="' + htmlEscape(value) + '"'

	if content:
		out += '>' + content + '</button>'
	else:
		out += ' />'

	return out

def checkboxInput(name, value=0, editable=True):
	r"""
	Creates an HTML checkbox.

	@param name     The name of the checkbox element.
	@param value    The value to be sent to the server if the checkbox is
	                checked when the form is submitted.
	@param editable Determines whether or not the checkbox data is
	                submitted to the server.

	@pre @a name must not be @c None or the empty string if @a editable
	     is true.
	@pre @a value must be @c None, @c 1, or @c 0.
	"""

	if editable:
		assert name != None, 'name must not be None.'
		name = str(name)
		assert name != "", 'name must not be the empty string.'

	assert (value == None or str(value) == '1' or str(value) == '0'), \
	  'Odd value specified: ' + str(value)

	out = '<input type="checkbox"'
	if editable:
		out += ' name="' + htmlEscape(name) + '" value="1"'
	if str(value) == '1':
		out += ' checked="checked"'
	if not editable:
		out += ' disabled="disabled"'
	out += ' />'

	return out

def hiddenInput(name, value=None, editable=True):
	r"""
	@param name     The name of the hidden field.
	@param value    The value of the hidden field.
	@param editable Determines whether or not the field data is
	                submitted to the server.

	@pre @a name must not be @c None or the empty string if @a editable
	     is true.
	"""

	if editable:
		assert name != None, 'name must not be None.'
		name = str(name)
		assert name != "", 'name must not be the empty string.'

	out = '<input type="hidden"'
	if editable:
		out += ' name="' + htmlEscape(name) + '"'

	if value != None and str(value) != '':
		out += ' value="' + htmlEscape(value) + '"'

	out += ' />'
	return out

def textInput(name, value=None, width=25, maxLength=None, editable=True):
	r"""
	Creates an HTML text @c input field or @c textarea.

	This function generates text @c input field or @c textarea depending on
	the specified @c width of the box. If @c width is 100 or greater,
	@c textarea tags are generated.

	@param name      The name of the input field.
	@param value     The initial value of the input field.
	@param width     The width of the input field. (If @a width is zero,
	                 the default width will be used.)
	@param maxLength The maximum amount of characters that can be entered
	                 into the input field.
	@param editable  Determines whether or not the field will be submitted
	                 to the server.

	@pre @a name must not be @c None or the empty string if @a editable
	     is true.
	@pre @a width must be an integer greater than or equal to zero.
	@pre @a maxLength must be None or an integer greater than zero.
	"""

	if editable:
		assert name != None, 'name must not be None.'
		name = str(name)
		assert name != "", 'name must not be the empty string.'

	try:
		width = int(width)
		assert (width >= 0), \
		       'width must be greater than or equal to zero.'
	except ValueError:
		assert 0, 'width must be convertable to an int.'

	try:
		assert (maxLength == None or int(maxLength) > 0), \
		  'maxLength must be None or an integer greater than zero.'
	except ValueError:
		assert 0, 'maxLength must be convertable to an int.'

	if not editable:
		if value != None and str(value) != '':
			return htmlEscape(value)
		else:
			return ''

	if width == 0:
		width = 25

	if maxLength != None:
		maxLength = int(maxLength)
	else:
		maxLength = width

	if width < 100:
		out = '<input type="text"'
		if editable:
			out += ' name="' + htmlEscape(name) + '"'
		out += ' size="' + str(width) + '" maxlength="' + \
		       str(maxLength) + '"'

		if value != None and str(value) != '':
			out += ' value="' + htmlEscape(value) + '"'

		out += ' />'
	else:
		out = '<textarea'
		if editable:
			out += ' name="' + htmlEscape(name) + '"'
		out += ' cols="50" rows="' + \
		  str(int(math.ceil(float(width)/50))) + '">'

		if value != None and str(value) != '':
			out += htmlEscape(value, convertNewlines=False)

		out += '</textarea>'

	return out

# End HTML Widgets


# START HTML Advanced Widgets
def dropDown(name, values, titles=None, default=None):
	r"""
	Creates a selectable drop-down list.

	@param name    The name of the drop-down list.
	@param values  The value of each item in the list.
	@param titles  The viewed list to select from.
	@param default Determines which value is selected in the list as the
	               default value.

	@pre @a name must not be @c None or the empty string.
	"""

	assert name != None, 'name must not be None.'
	name = str(name)
	assert name != "", 'name must not be the empty string.'

	if titles == None:
		titles=values

	out = '<select'
	out += ' name="' + htmlEscape(name) + '"'
	out += '>\n'
	for value, title in zip(values, titles):
		out += '<option value="' + htmlEscape(value) + '"'
		if default != None and str(value) == str(default):
			out += ' selected="selected"'
		out += '>' + htmlEscape(title) + '</option>\n'
	out += '</select>'
	return out

def region(title, text, cssClass=None):
	r"""
	Defines a paragraph with the @a title and converts the specified
	text to a string.

	This function defines a paragraph, titles it using the function
	@c span(), and converts the submitted text to a string.

	@param title    The title associated with the paragraph.
	@param text     The text to display.
	@param cssClass The CSS class to use to display @a text. If @a cssClass is @c None, @c region_header will be used.

	@pre @a title must not be @c None or the empty string.
	@pre @a text must not @c None or the empty string.
	@pre @a cssClass must not be the empty string.
	"""

	assert title != None, 'title must not be None.'
	title = str(title)
	assert title != "", 'title must not be the empty string.'

	assert text != None, 'text must not be None.'
	text = str(text)
	assert text != "", 'text must not be the empty string.'

	if cssClass == None:
		cssClass = 'region_header'
	else:
		cssClass = str(cssClass)

	assert cssClass != "", 'cssClass must not be the empty string.'

	return '<p>' + span(title, cssClass) + '</p>\n' + text

# END HTML Advanced Widgets
