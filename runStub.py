r"""
Wrapper for Skime Modules

This simple script appends its first command line argument to the import path
and executes the Python script specified as its second argument. The arguments
are shifted so the script executed is none-the-wiser about this wrapper.

If an incorrect number of command line arguments is provided, the following
usage message (assuming the script is named @c runStub.py) will be printed and
the script will terminate:
@verbatim
Usage: runStub.py DIR FILE
@endverbatim

If the script is called to execute a script with the same name as itself, it
will simply exit without running anything. This keeps the script from
recursing.

@author Andy Filer \<andyf\@wiktel.com\>
@author Richard Laager \<rlaager\@wiktel.com\>
"""

import os
import sys

(path1,name1) = os.path.split(sys.argv[0])

if len(sys.argv) < 3:
	print 'Usage: ' + name1 + ' DIR FILE'
	sys.exit()

sys.path.append(sys.argv[1])

(path2,name2) = os.path.split(sys.argv[2])
if (name2 != name1):
	sys.argv = sys.argv[2:]
	execfile(os.path.join(path2, name2))
