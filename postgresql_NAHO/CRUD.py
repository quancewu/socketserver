import psycopg2
import numpy as np
import datetime

class SQL:
    def __init__(self, config, *arg):
        self.db = psycopg2.connect(**config)
        self.cur = self.db.cursor()
        self.exe = self.cur.execute
        self.fa = self.cur.fetchall

    def upload_SWS250(self,data:list,data_format:list):
        try:
            for idata in data:
                value_txt = ''
                value_txt = ','.join([f'{key} = {value}' for key, value in zip(data_format,idata[1::])])
                txt = f'UPDATE public.d11 SET {value_txt} where datetimeutc = {idata[0]};'
                # print(txt)
                self.exe(txt)
                self.db.commit()
                msg_return = dict(
                    flag = True,
                    message = f"upload postgreSQL succefully with {len(data)} row"
                    )
        except psycopg2.Error as e:
            msg_return = dict(
                flag = False,
                message = f"upload postgreSQL failed with error {e.pgerror}"
                )
            self.db.rollback()
        except Exception as e:
            msg_return = dict(
                flag = False,
                message = f"system with error {e}"
                )
        return msg_return
    
    def insert(self,data:list,data_format:list,tablename:str):
        print(len(data))
        try:
            sql_data_format = ','.join(data_format)
            for idata in data:
                value_txt = ''
                value_txt = ','.join(idata)
                txt = f'INSERT INTO {tablename}({sql_data_format}) VALUES ({value_txt});'
                # print(txt)
                self.exe(txt)
                self.db.commit()
                msg_return = dict(
                    flag = True,
                    message = f"upload postgreSQL succefully with {len(data)} row"
                    )
        except psycopg2.Error as e:
            msg_return = dict(
                flag = False,
                message = f"upload postgreSQL failed with error {e.pgerror}"
                )
            self.db.rollback()
        except Exception as e:
            msg_return = dict(
                flag = False,
                message = f"system with error {e}"
                )
        return msg_return
    def rollback(self):
        self.exe('rollback;')

    def commit(self):
        self.exe('commit;')

    def close(self):
        self.db.close()

if __name__ == "__main__":
    pass