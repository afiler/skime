from display.html import *

def columnDisplay(summary, headings, data,
                  sortField=0, reverseSort=False,
                  headingClass=None, dataClass=None,
                  linkFunction=None, linkURL=None):

	assert summary != None, 'summary must not be None.'
	summary = str(summary).strip()
	assert summary != '', 'summary must not be the empty string.'

	length = len(headings)
	assert length > 0, 'headings must have at least one item.'
	for dataRow in data:
		assert len(dataRow) == length, \
		  'The items in data must be the same length as headings.'

	if headingClass != None:
		headingClass = str(headingClass).strip()
		assert headingClass != '', 'headingClass must not be the empty string.'

	if dataClass != None:
		dataClass = str(dataClass).strip()
		assert dataClass != '', 'dataClass must not be the empty string.'

	assert callable(linkFunction), 'linkFunction must be callable.'

	assert linkURL == None or linkFunction == None, \
	  'linkURL is meaningless without a linkFunction.'

	columnSort(data)

	out = []

	if not linkFunction:
		out.append(row(''.join([cell(htmlEscape(title), headingClass)
		                        for title in headings])))
	else:
		out2 = []
		index = 0
		for title in headings:
			out2.append(cell(
			  linkFunction(linkURL, htmlEscape(title), index,
			               sortField, reverseSort)))
			index += 1
		out.append(row(''.join(out2)))

	for dataRow in data:
		out.append(row(''.join([cell(htmlEscape(dataColumn), dataClass)
		                        for dataColumn in dataRow])))
	return table(summary, ''.join(out))

def columnGenericLinkFunction(linkURL, heading, index, sortField, reverseSort):

	assert heading != None, 'heading must not be None.'
	heading = str(heading).strip()

	try:
		assert (int(index) >= 0), \
		       'index must be greater than or equal to zero.'
	except ValueError:
		assert 0, 'index must be convertable to an int.'

	out = []

	out.append('<a href="')
	if linkURL != None:
		linkURL = str(linkURL).strip()
		out.append(linkURL)
		if linkURL.count('?') == 0:
			out.append('?')
	else:
		out.append('?')
	out.append('sortField=')
	out.append(str(index))
	if sortField == index:
		out.append('&amp;reverseSort=')
		out.append(str(int(not reverseSort)))
	out.append('">')
	out.append(heading)
	if sortField == index:
		out.append('&nbsp;<img src="sort')
		out.append(str(int(bool(reverseSort))))
		out.append('.png" />')
	out.append('</a>')

	return ''.join(out)

def columnSort(data, sortField=0, reverseSort=False):
	if not reverseSort:
		data.sort(lambda x, y: cmp(x[sortField], y[sortField]))
	else:
		data.sort(lambda x, y: cmp(y[sortField], x[sortField]))
