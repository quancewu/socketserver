from info import info
from .util import *
import os
import time
import json
import numpy as np
from file_manager import manager

def dat_err_and_get_new_path(path):
    o_dir = os.path.dirname(path)
    o_filename = os.path.basename(path)
    new_filename = o_filename.replace('.dat','_new.dat')
    new_path = os.path.join(o_dir,new_filename)
    return new_path

def get_and_backup_json(path):
    backup_path = get_backup_path(path)
    with open(path,'r') as o_file:
        try:
            o_data = json.load(o_file)
            with open(backup_path,'w') as backup_file:
                json.dump(o_data,backup_file,indent=4)
            return o_data
        except json.decoder.JSONDecodeError:
            return None

def append_list_like_dat(path,data):
    with open(path,'a') as f:
        try:
            write_data =[]
            for key in data:
                write_data.append(data[key])
            write_data = np.array(write_data)
            write_in = ''
            if write_data.ndim > 1:
                write_data = write_data.T
                for iline in write_data:
                    write_in = write_in+','.join(iline)+'\r\n'
            else:
                write_in = ','.join(write_data)+'\r\n'
            f.write(write_in)
        except:
            new_path = dat_err_and_get_new_path(path)
            append_list_like_dat(new_path,data)

def save_dat_data(code,y,m,identity,filename,data):        
    data_dir = get_data_dir(
        info.File.save_dir,code,y,m,identity
    )
    exist_or_create_dir(data_dir)    
    file_path = os.path.join(data_dir,time.strftime("{}_%H.dat".format(filename)))
    exist_or_create_file(file_path)

    if info.File.json_format == 'list_like':
        append_list_like_dat(file_path,data)
        manager.LogWriter.log(
            'Success','Save txt_like Json Obj(len={})) Successfully.'.format(
                str(len(data))
            )
        )
