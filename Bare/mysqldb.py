import pymysql
import configparser
import os.path

class MysqlDB:
    # 数据库操作
    __sql = ''
    __db = {}
    def __init__(self):
        self.__config('mysql')
    def __config(self, section):
        conf = configparser.ConfigParser()
        conf.read(os.path.split(os.path.realpath(__file__))[0] + "/../Config/db.conf")
        self.__host = conf.get(section, 'host')
        self.__port = int(conf.get(section, 'port'))
        self.__user = conf.get(section, 'user')
        self.__pwd = conf.get(section, 'pwd')
        self.__dbname = conf.get(section, 'dbname')
        self.__charset = conf.get(section, 'charset')
    # 打开数据库连接
    def _connect(self):
        self.__db = pymysql.connect(host = self.__host, port = self.__port, user = self.__user, password = self.__pwd, db = self.__dbname, charset = self.__charset)
        return self.__db
    # 切换数据库
    def selectDB(self, dbname, charset = ''):
        self.__dbname = dbname
        if charset:
            self.__charset = charset
        return self
    # 切换数据库配置
    def selectConfig(self, section):
        self.__config(section)
        return self
    # 查询数量
    def getCount(self, table, where = {}):
        if where:
            wheresql = self._parseWhere(where)
        else:
            wheresql = ['1=1']
        self.__sql = "SELECT COUNT(*) FROM `%s` WHERE %s" % (table, ' AND '.join(wheresql))
        res = self.getOne()
        if res[0]:
            return res[0]
        else:
            return 0
    # 查询 SELECT语句的快捷方式
    def find(self, table, where = {}, fields = '*', order = '', limit = ''):
        if where:
            wheresql = self._parseWhere(where)
        else:
            wheresql = ['1=1']
        if order:
            order = 'ORDER BY ' + order
        if limit:
            if isinstance(limit, list):
                limit = 'LIMIT ' + str(limit[0]) + ', ' + str(limit[1])
            else:
                limit = 'LIMIT ' + str(limit)
        self.__sql = "SELECT %s FROM `%s` WHERE %s %s %s" % (fields, table, ' AND '.join(wheresql), order, limit)
        res = self.getAll()
        # 结果重组为关系dict数组
        field = []
        if fields == '*':
            self.__sql = 'SHOW COLUMNS FROM `%s`' % (table)
            column = self._query().fetchall()
            for val in column:
                field.append(val[0])
        else:
            temp = fields.split(',')
            for val in temp:
                field.append(val.strip(' `'))
        data = []
        for val in res:
            temp_dict = {}
            for i in range(len(field)):
                temp_dict[field[i]] = val[i]
            data.append(temp_dict)
        return data
    # 新增 [{'field1':'value1','field2':'value2',...},{...}] 支持多个 注意：所有值都必须为字符串
    def insert(self, table, rows = []):
        if isinstance(data, dict):
            rows = [rows]
        fields = []
        inserts = []
        flag = True
        for row in rows:
            values = []
            if flag == False:
                values = [''] * len(row)
            for key, val in row.items():
                if flag:
                    fields.append(key)
                    values.append(val)
                else:
                    k = fields.index(key)
                    values[k] = val
            inserts.append('("' + '", "'.join(values) + '")')
            flag = False
        self.__sql = "INSERT INTO `%s` (%s) VALUES %s" % (table, '`' + '`, `'.join(fields) + '`', ', '.join(inserts))
        cursor = self._exec()
        return cursor.rowcount
    # 更新 {'field1':'value1','field2':'value2',...} 注意：所有值都必须为字符串
    def update(self, table, row = {}, where = {}):
        if not row or not where:
            return False
        fields = []
        for key, val in row.items():
            fields.append('`' + str(key) + '`="' + str(val) + '"')
        wheresql = self._parseWhere(where)
        self.__sql = "UPDATE `%s` SET %s WHERE %s" % (table, ', '.join(fields) , ' AND '.join(wheresql))
        cursor = self._exec()
        return cursor.rowcount
    # 删除
    def delete(self, table, where = {}):
        if not where:
            return False
        wheresql = self._parseWhere(where)
        self.__sql = "DELETE FROM `%s` WHERE %s" % (table, ' AND '.join(wheresql))
        cursor = self._exec()
        return cursor.rowcount
    # 原生sql语句查询
    def query(self, sql):
        self.__sql = sql
        return self.getAll()
    def getOne(self):
        cursor = self._query()
        # 使用 fetchone() 方法获取单条数据
        return cursor.fetchone()
    def getAll(self, table = ''):
        cursor = self._query()
        # 使用 fetchall() 方法获取多条数据
        return cursor.fetchall()
    def _query(self):
        if self.__sql:
            # 使用 cursor() 方法创建一个游标对象 cursor
            self._connect()
            cursor = self.__db.cursor()
            # 使用 execute()  方法执行 SQL
            cursor.execute(self.__sql)
            return cursor
        else:
            return False
    def _exec(self):
        if self.__sql:
            self._connect()
            cursor = self.__db.cursor()
            try:
               cursor.execute(self.__sql)
               # 执行sql语句
               self.__db.commit()
            except:
               # 发生错误时回滚
               self.__db.rollback()
            return cursor
        else:
            return False
    def _parseWhere(self, where):
        if not where:
            return ''
        wheresql = []
        for key, val in where.items():
            if isinstance(val, list):
                wheresql.append('`' + str(key) +'`' + str(val[0]) + '"' + str(val[1]) +'"')
            else:
                    wheresql.append('`' + str(key) + '`="' + str(val) +'"')
        return wheresql
    def __del__(self):
        if self.__db:
            self.__db.close()
        self.__sql = ''


if __name__=="__main__":
    '''
    DB = MysqlDB()
    data = DB.query("SELECT VERSION()")
    print ( data )
    DB.selectDB('mysql')
    data = DB.query("SHOW TABLES")
    print ( data )
    '''
    #res = DB.insert('user',[{'LoginName':'zjf', 'NickName':'camfee', 'Password':'123456', 'Age':'22', 'Sex':'1'}, {'LoginName':'zjf2', 'NickName':'camfee2', 'Password':'123456', 'Age':'22', 'Sex':'1'}])
    #res = DB.update('user',{'Sex':'2'},{'UserId':'9'})
    #res = DB.delete('user',{'Sex':'2'})
    #res = DB.query("SHOW TABLES")
    #res = DB.find('user',{'LoginName':['=','zjf']},'UserId,Age,Sex')
    #res = DB.find('user',{'LoginName':'zjf'},'UserId,Age,Sex')
    #res = DB.getCount('user',{'LoginName':'zjf2'})
