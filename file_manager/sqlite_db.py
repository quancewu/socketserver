import sqlite3

class SQLite:
    def __init__(self,filepath):
        self.filepath = filepath

    def open_table_check(self,tablename,data_format):
        # print('open_check',tablename)
        self.db = sqlite3.connect(self.filepath)
        self.cur = self.db.cursor()
        self.exe = self.cur.execute
        self.fa = self.cur.fetchall
        self.tablename = tablename
        table_contants = ','.join([f'{key} {value}' for key, value in data_format.items()])
        # primary_key = data_format['primary_key']
        txt = f"create table if not exists {self.tablename} ( {table_contants});"
        # txt = f"create table if not exists {self.tablename} ( {table_contants}, primary key ({primary_key}));"
        # print(txt)
        self.exe(txt)

    def open(self,tablename):
        # print('open_not_check',tablename)
        self.db = sqlite3.connect(self.filepath)
        self.cur = self.db.cursor()
        self.exe = self.cur.execute
        self.fa = self.cur.fetchall
        self.tablename = tablename

    def insert(self,data):
        self.exe(f'insert into {self.tablename} values ({data});')

    def update(self,data,sql_id):
        # print(f'update {self.tablename} set {data} where {sql_id};')
        self.exe(f'update {self.tablename} set {data} where {sql_id};')
    def commit(self):
        self.db.commit()

    def close(self):
        # self.db.commit()
        self.db.rollback()
        self.db.close()

    def upload_data(self,tablename,data,data_format):
        self.open_table_check(tablename,data_format)
        for idata in data:
            insert_txt = ' ,'.join(['null'] + idata)
            # print(insert_txt)
            self.insert(insert_txt)
            self.commit()
        self.close()
        # for key in data.keys():
        #     if key=='Time': timeKey='Time'; continue
        #     if key=='TIMESTAMP': timeKey='TIMESTAMP'; continue
        #     i=0
        #     for time,val in zip(data[timeKey],data[key]):
        #         self.insert(f"null,'{time}','{key}',{val},null")
        #         i+=1
        #         if (i%1000)==0: self.commit(); print(i)
        #     self.commit()
        #     self.close()
    
    def update_data(self,tablename,data,data_format):
        self.open(tablename)
        for idata in data:
            update_txt = ','.join([f'{key} = {value}' for key, value in zip(data_format[1::],idata[1::])])
            sql_id = f'{data_format[0]} = {idata[0]}'
            self.update(update_txt,sql_id)
            self.commit()
        self.close()
    
    def data_select(self,tablename,data_format,flag_num):
        self.open(tablename)
        column = ','.join(data_format)
        self.exe(f'select {column} from {self.tablename} where upload_flag < {flag_num} order by ID limit 100;')
        data = self.fa()
        # print(data)
        self.close()
        return data