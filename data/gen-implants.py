#!/usr/bin/python3

import sqlite3

# You can get this file from https://www.fuzzwork.co.uk/dump/
dbFilename="sqlite-latest.sqlite" # Make sure this is the full path if this file is not in your current directory

db = sqlite3.connect(dbFilename)
curs = db.execute("select it.typeID,it.typeName,dat.attributeName,coalesce(dta.valueFloat, dta.valueInt) from invTypes as it, dgmTypeAttributes as dta, dgmAttributeTypes as dat where it.published = 1 and it.typeID = dta.typeID and dta.attributeID = dat.attributeID and coalesce(dta.valueFloat, dta.valueInt) > 0 and dat.attributeID in (175, 176, 177, 178, 179) order by it.typeID;")

print('<?xml version="1.0" encoding="utf-8"?>')
print('<implants>')

lastTypeID = 0
for rec in curs.fetchall():
	typeID = rec[0]
	name = rec[1]
	bonusText = rec[2]
	bonusValue = rec[3]
	if (lastTypeID != 0 and typeID != lastTypeID):
		print('/>') # Now that we know that this line is a new implant, finish the previous line
	elif (typeID == lastTypeID):
		print(' {}="{}"'.format(bonusText, bonusValue), end="")
		lastTypeID = typeID
		continue
	print('  <implant typeID="{}" name="{}" {}="{}"'.format(*rec), end="")
	lastTypeID = typeID

print('/>')
print('</implants>')
