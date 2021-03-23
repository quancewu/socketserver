import queue
import threading
from file_manager.manager import DataManager,LogManager,LogWriter,SQLiteManager
from info.info import upload_SQL_NAHO_config

class NahoApi(threading.Thread):
    _upload_queue = queue.Queue(maxsize=300)

    @classmethod
    def _sql(cls,file_type,code,y,m,identity,filename,data,data_format=None):
        if not cls._upload_queue.full():
            cls._upload_queue.put(
                (file_type,code,y,m,identity,filename,data,data_format)
            )
        else:
            LogWriter.log(
                    'Error',
                    'upload queue is full'
                )
            cls._upload_queue.put(
                (file_type,code,y,m,identity,filename,data,data_format)
            )

    @classmethod
    def upload_mysql(cls,code,y,m,identity,filename,data,data_format):
        cls._sql('mysql',code,y,m,identity,filename,data,data_format)

    @classmethod
    def upload_pgsql(cls,code,y,m,identity,filename,data,data_format):
        cls._sql('pgsql',code,y,m,identity,filename,data,data_format)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.sql_connet = SQL(upload_SQL_config.config)

    def login_init(self,sql_type):
        if sql_type == 'mysql':
            from naho.CRUD import SQL
            from info.info import upload_MySQL_config
            self.sql_connet = SQL(upload_MySQL_config.config)
        elif sql_type == 'pgsql':
            from postgresql_NAHO.CRUD import SQL
            from info.info import upload_SQL_NAHO_config
            self.sql_connet = SQL(upload_SQL_NAHO_config.config)

    def run(self):
        while 1:
            obj = NahoApi._upload_queue.get()
            if len(obj) == 8:
                sql_type, code, y, m, identity, filename, data, data_format = obj
                if sql_type == 'mysql':
                    self.login_init(sql_type)
                    mysql_data_format = [key for key in 
                                data_format.keys() if key not in ['ID','DatetimeLST','TimestampLST','upload_flag']]
                    message = self.sql_connet.update(data,mysql_data_format)
                    if message['flag']:
                        LogWriter.log(
                            'Success',
                            '{}'.format(message['message'])
                        )
                        sql_data_format = [key for key in 
                                data_format.keys() if key in ['TimestampLST','upload_flag']]
                        upload_flag_data = [[i[0],'1'] for i in data]
                        SQLiteManager.update_data(
                            code,y,m,
                            identity,
                            filename,
                            upload_flag_data,
                            sql_data_format
                            )
                    else:
                        LogWriter.log(
                            'Error',
                            '{}'.format(message['message'])
                        )
                elif sql_type == 'pgsql':
                    self.login_init(sql_type)
                    pgsql_data_format = [key for key in 
                                data_format.keys() if key not in ['id','upload_flag']]
                    message = self.sql_connet.insert(data,pgsql_data_format,'public.d11')
                    if message['flag']:
                        LogWriter.log(
                            'Success',
                            '{}'.format(message['message'])
                        )
                        sql_data_format = [key for key in 
                                data_format.keys() if key in ['datetimeutc','upload_flag']]
                        upload_flag_data = [[i[0],'200'] for i in data]
                        SQLiteManager.update_data(
                            code,y,m,
                            identity,
                            filename,
                            upload_flag_data,
                            sql_data_format
                            )
                            # [data[0]] + ['1'],
                    else:
                        LogWriter.log(
                            'Error',
                            '{}'.format(message['message'])
                        )
                        sql_data_format = [key for key in 
                                data_format.keys() if key in ['datetimeutc','upload_flag']]
                        upload_flag_data = [[i[0],'4'] for i in data]
                        SQLiteManager.update_data(
                            code,y,m,
                            identity,
                            filename,
                            upload_flag_data,
                            sql_data_format
                            )