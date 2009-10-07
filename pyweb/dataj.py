#!/usr/bin/python
print "Content-type: text/html"
print
print "<pre>"
import os, sys
print "<strong>Python %s</strong>" % sys.version
for (x,y) in os.environ.items():
    print "%s\t%s" % (x, y)
    print "</pre>"

