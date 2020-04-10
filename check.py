import sqlite3
db = sqlite3.connect('local.db')
cur = db.cursor()

# cur.execute('DROP TABLE IF EXISTS Media')

# cur.execute('''CREATE TABLE IF NOT EXISTS Media(
#                 id INTEGER PRIMARY KEY, title TEXT, 
#                 type TEXT,  genre TEXT,
#                 onchapter INTEGER,  chapters INTEGER,
#                 status TEXT
#                 )''')

# passpath = r'C:\python37\projects\LogReport\EOL1'
# from CustomerReportBuilding import Report,CSV_List
# csv_list = CSV_List(passpath)
# Final_CSV_List = csv_list.get_nonrepeateCSV()
# for i,filename in enumerate(Final_CSV_List):
#   pathx = passpath + "/" + filename
#   report = Report(passpath)
#   data = report.csv_read(pathx)
#   values = report.dict_factorary(data)


# values = {'title':'jack','type':None,'genre':'Action','onchapter':None,'chapters':6,'status':'Ongoing'}

# What would I Replace x with to allow a 
# dictionary to connect to the values? 
# cur.execute('INSERT INTO Media VALUES (NULL, x)', values)
# # Added code.
# cur.execute('SELECT * FROM Media')
# colnames = cur.description
# list = [row[0] for row in cur.description]
# new_list = [values[i] for i in list if i in values.keys()]
# sql = "INSERT INTO Media VALUES ( NULL, "
# qmarks = ', '.join('?' * len(values))
# sql += qmarks + ")"
# cur.execute(sql, new_list)
# db.commit() #<-Might be important.
# cur.execute('SELECT * FROM Media')
# media = cur.fetchone()
# print (media)

