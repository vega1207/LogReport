import time
import sqlite3
import threading
from DBUtils.PooledDB import PooledDB, SharedDBConnection
import datetime
from threading import RLock
import json

LOCK = RLock()

POOL = PooledDB(
    creator=sqlite3,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    database='EOL.db'
)

class Db(object):

  def __init__(self):
    # 检测当前正在运行连接数的是否小于最大链接数，如果不小于则：等待或报raise TooManyConnections异常
    # 否则
    # 则优先去初始化时创建的链接中获取链接 SteadyDBConnection。
    # 然后将SteadyDBConnection对象封装到PooledDedicatedDBConnection中并返回。
    # 如果最开始创建的链接没有链接，则去创建一个SteadyDBConnection对象，再封装到PooledDedicatedDBConnection中并返回。
    # 一旦关闭链接后，连接就返回到连接池让后续线程继续使用。
    # print(th, '链接被拿走了', conn1._con)
    # print(th, '池子里目前有', pool._idle_cache, '\r\n')

    self.conn = POOL.connection()
    def dict_factory(cursor, row):
      d = {}
      for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
      return d
    self.conn.row_factory = dict_factory
    self.cursor = self.conn.cursor()

  def fetch_one(self,sql):
    with LOCK:
      self.cursor.execute(sql)
      result = self.cursor.fetchone()
      print(result)
      self.conn.close()
      return result

  def fetch_all(self,sql):
    with LOCK:
      self.cursor.execute(sql)
      result = self.cursor.fetchall()
      # print(result)
      self.conn.close()
      return result

  def get_measure_value(self,log_name,test_item):
    with LOCK:
      data = self.fetch_all("select * from psa where log_name='%s'"%log_name)
      get_csv_testitems = []
      get_csv_testitems_result = []
      for row in data:
          get_csv_testitems.append(row[2])
      for row in data:
          get_csv_testitems_result.append(row[3])
      data_combine = dict(zip(get_csv_testitems, get_csv_testitems_result))
      return data_combine[test_item]

  def test_add(self,passpath=''):
    with LOCK:
      from CustomerReportBuilding import Report,CSV_List
      csv_list = CSV_List(passpath)
      Final_CSV_List = csv_list.get_nonrepeateCSV()
      for i,filename in enumerate(Final_CSV_List):
        pathx = passpath + "/" + filename
        report = Report(passpath)
        data = report.csv_read(pathx)
        data_combine = report.dict_factorary(data)
        input_list  = list(data_combine)
        # print(data_combine )
        for i in input_list :
          # I recommend putting this inside a function, this way if this 
          # Evaluates to None at the end of the loop, you can exit without doing an insert
          if i :
              input_dict = i 
          else:
              input_dict = None
              continue

        keylist = list(data_combine.keys())
        vallist = list(data_combine.values())

        query = 'INSERT INTO demo (' +','.join( ['[' + i + ']' for i in keylist]) + ') VALUES (' + ','.join(['?' for i in vallist]) + ')'
        items_to_insert = list(tuple(x.get(i , '') for i in keylist) for x in input_list)
        # print(keylist)
        self.cursor.executemany(query , items_to_insert)










        # dict_xu = json.dumps(data_combine)    #将字典json序列化就可以保存在sqlite3
        # print (dict_xu)
        # now = datetime.datetime.now()
        # for key in data_combine:
        #   value = data_combine[key]
          

      # sql = "INSERT INTO psa VALUES('None','test','items','test','pass','12345678')"
      # sql = "INSERT INTO psa (id,log_name,test_item,measure_value,Result,date_time) VALUES(?,?,?,?,?,?)"
          
          # sql = "INSERT INTO psa VALUES(?,?,?,?,?,?)"
          # value2 = [(None,'log_name', key, value, 'PASS', now)]
          # self.cursor.execute(sql,value2)
  
        # self.cursor.execute('INSERT into psa values (?,?,?,?,?,?)',[None,'logname',data_combine['TestItem'], data_combine['Read FTEAEXC_UResExcAvg'], data_combine['Read MAIN_VSIRxsGridVoltW'],now])
        # self.conn.commit()
        # self.conn.close()

            






    


  

if __name__ == '__main__':  
  db = Db()
  # db.fetch_one('select * from psa')
  # db.log_name_get('lucas')
  # db.get_measure_value('sean','顶顶顶顶顶顶顶')
  # db.fetch_all('select * from psa')
  db.test_add(r'C:\python37\projects\LogReport\EOL1')
  # import json
  # sss = json.dump(ddd)
  # print (sss)
