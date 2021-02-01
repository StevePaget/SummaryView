#!/usr/bin/python

import sqlite3
from datetime import datetime

##===============================================

class DatabaseUtility: 
	def __init__(self, database):
		self.conn = sqlite3.connect(database)  #opens a database, or creates it
							#if it doesn't already exist
		
		self.cursor = self.conn.cursor()    # a Cursor is created to enable you to run commands		
		print("Connected")

	def RunCommand(self, cmd, parameters = None):
		if parameters == None:
			print ("RUNNING COMMAND: " + cmd)
			try:
				result = self.cursor.execute(cmd)
				#print("DB manager debugging") 
				#for row in result:
					#print (row)
				#print("end result")
			except:
				print ('ERROR!')
				print ('WITH ' + cmd)
				result = False
			self.conn.commit()
			return result
		else:
			print ("RUNNING COMMAND: " + cmd + " with" + str(parameters))
			try:
				result = self.cursor.execute(cmd,parameters)
			except:
				print ('ERROR!')
				print ('WITH ' + cmd,str(parameters))
				result = False
			self.conn.commit()
			return result			

	def GetTable(self, tableName):
		return self.RunCommand("SELECT * FROM %s;" % tableName)

	def GetColumns(self, tableName):
		self.RunCommand("SELECT * FROM %s;" % tableName)
		names = list(map(lambda x: x[0], self.cursor.description))
		return names

	def __del__(self):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()

##===============================================
##===============================================


if __name__ == '__main__':
	db = 'testDB.db'
	dbu = DatabaseUtility(db)
	result = dbu.RunCommand("SELECT * FROM tblPeople")
	dbu.GetColumns("tblPeople")
