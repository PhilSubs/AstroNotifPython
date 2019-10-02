#!/usr/bin/env python
print "Content-type: text/html\n"
try:
    fp = open("TaskerInfo.txt", "r")
    # do stuff here
    print(fp.read())
finally:
    fp.close()
