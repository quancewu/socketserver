import queue
import threading
import os,time
import schedule
import logging
from .json_file import save_json_data
from .csv_file import save_csv_data
from .dat_file import save_dat_data
from .sqlite_db import SQLite
from .util import get_log_path,exist_or_create_dir,exist_or_create_file,get_data_dir,get_data_dir_with_time
from info import info

class DataManager(threading.Thread):
    _save_queue = queue.Queue(maxsize=600)

    @classmethod
    def _save(cls,file_type,code,y,m,identity,filename,data,data_format=None):
        cls._save_queue.put(
            (file_type,code,y,m,identity,filename,data,data_format)
        )

    @classmethod
    def save_json(cls,code,y,m,identity,filename,data):
        cls._save('json',code,y,m,identity,filename,data)

    @classmethod
    def save_csv(cls,code,y,m,identity,filename,data,data_format):
        cls._save('csv',code,y,m,identity,filename,data,data_format)
    
    @classmethod
    def save_dat(cls,code,y,m,identity,filename,data):
        cls._save('dat',code,y,m,identity,filename,data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        while 1:
            obj = DataManager._save_queue.get()
            if len(obj) == 8:
                file_type, code, y, m, identity, filename, data, data_format = obj
                if file_type == 'json':
                    save_json_data(code,y,m,identity,filename,data)
                elif file_type == 'dat':
                    save_dat_data(code,y,m,identity,filename,data)
                elif file_type == 'csv':
                    # print("succefull calling filesystem")
                    if save_csv_data(code,y,m,identity,filename,data,data_format):
                        LogWriter.log(
                            'Success',
                            'data save datatime {}'.format(data[0:2])
                        )
                    else:
                        LogWriter.log(
                            'Error',
                            'data same as last time {}'.format(data[0:2])
                        )

class LogWriter(threading.Thread):
    _wq = queue.Queue(maxsize=300)

    @classmethod
    def log(cls,status,description):
        cls._wq.put(
            (status,description)
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%dT%H:%M:%S %z')
        logger = logging.getLogger(__name__)

    def run(self):
        while 1:
            obj = LogWriter._wq.get()

            if obj == None or len(obj) != 2: 
                time.sleep(1)
                continue

            path = get_log_path(info.File.log_dir)
            exist_or_create_dir(info.File.log_dir)
            status,description = obj
            write_obj = time.strftime("%Y/%m/%d %H:%M:%S %z: {}! {}".format(
                            status,description
                        )
                    )
            with open(path,'a') as log_file:
                log_file.write(
                    write_obj+'\n'
                )
            # logging.info(f'{status}, {description}')
            print(write_obj)

class SQLiteManager(threading.Thread):
    _save_queue = queue.Queue(maxsize=600)

    @classmethod
    def _save(cls,file_type,code,y,m,identity,filename,data,data_format=None):
        cls._save_queue.put(
            (file_type,code,y,m,identity,filename,data,data_format)
        )

    @classmethod
    def _get_date(cls,file_type,code,y,m,identity,filename,date,data,data_format,flag_num):
        cls._save_queue.put(
            (file_type,code,y,m,identity,filename,date,data,data_format,flag_num)
        )

    @classmethod
    def save_SQLite_data(cls,code,y,m,identity,filename,data,data_format):
        cls._save('sqlite',code,y,m,identity,filename,data,data_format)
    
    @classmethod
    def update_data(cls,code,y,m,identity,filename,data,data_format):
        cls._save('sqlite_update',code,y,m,identity,filename,data,data_format)

    @classmethod
    def get_data(cls,code,y,m,identity,filename,date,data,data_format,flag_num):
        cls._get_date('sqlite_select',code,y,m,identity,filename,date,data,data_format,flag_num)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        while 1:
            obj = SQLiteManager._save_queue.get()
            if len(obj) == 8:
                sql_type, code, y, m, identity, filename, data, data_format = obj
                if sql_type == 'sqlite':
                    # time.sleep(1)
                    data_dir = get_data_dir(
                        info.File.save_dir,code,y,m,identity
                    )
                    exist_or_create_dir(data_dir)
                    file_path = os.path.join(data_dir,"{}.db".format(filename))
                    try:
                        local_sql = SQLite(file_path)
                        local_sql.upload_data(filename,data,data_format)
                        LogWriter.log(
                            'Success',
                            'data save to sqlite db name {}'.format(filename)
                        )
                    except Exception as e:
                        LogWriter.log(
                            'Error',
                            'data can not save to sqlite db name {} with error {}'.format(filename,e)
                        )
                elif sql_type == 'sqlite_update':
                    data_dir = get_data_dir(
                        info.File.save_dir,code,y,m,identity
                    )
                    exist_or_create_dir(data_dir)
                    try:
                        file_path = os.path.join(data_dir,"{}.db".format(filename))
                        local_sql = SQLite(file_path)
                        local_sql.update_data(filename,data,data_format)
                        LogWriter.log(
                            'Success',
                            'data update to sqlite db name {}'.format(filename)
                        )
                    except Exception as e:
                        LogWriter.log(
                            'Error',
                            'data can not update to sqlite db name {} with error {}'.format(filename,e)
                        )
                else:
                    LogWriter.log(
                        'Error',
                        'sql_type ({}) not found'.format(sql_type)
                    )
            elif len(obj) == 10:
                sql_type, code, y, m, identity, filename, date, data, data_format, flag_num = obj
                if sql_type == 'sqlite_select':
                    data_dir = get_data_dir_with_time(
                        info.File.save_dir,date,code,y,m,identity
                    )
                    exist_or_create_dir(data_dir)
                    file_path = os.path.join(data_dir,"{}.db".format(filename))
                    try:
                        local_sql = SQLite(file_path)
                        data_array = local_sql.data_select(filename,data_format,flag_num)
                        # print('manager',data_array)
                        if data_array != []:
                            data.put(data_array)
                        else:
                            data.put('no data')
                        LogWriter.log(
                            'Success',
                            'select data from sqlite db name {}'.format(filename)
                        )
                    except Exception as e:
                        LogWriter.log(
                            'Error',
                            'can not select data from sqlite db name {} with error {}'.format(filename,e)
                        )
                else:
                    LogWriter.log(
                        'Error',
                        'sql_type ({}) not found'.format(sql_type)
                    )
class LogManager(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LogWriter().start()
    