from info import info
from .util import *
import os
import time
import json
from file_manager import manager

def json_err_and_get_new_path(path):
    o_dir = os.path.dirname(path)
    o_filename = os.path.basename(path)
    new_filename = o_filename.replace('.json','_new.json')
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

def append_list_like_json(path,data):
    if os.stat(path).st_size !=0 :
        o_data = get_and_backup_json(path)
        if o_data != None:
            o_data.append(data)
            with open(path,'w') as old_file:
                json.dump(o_data,old_file,indent=4)
        else:
            new_path = json_err_and_get_new_path(path)
            append_list_like_json(new_path,data)
    else:
        with open(path,'w') as new_file:
            json.dump([data],new_file,indent=4)

def save_json_data(code,y,m,identity,filename,data):        
    data_dir = get_data_dir(
        info.File.save_dir,code,y,m,identity
    )
    exist_or_create_dir(data_dir)    
    file_path = os.path.join(data_dir,time.strftime("{}_%H.json".format(filename)))
    exist_or_create_file(file_path)

    if info.File.json_format == 'list_like':
        append_list_like_json(file_path,data)
        manager.LogWriter.log(
            'Success','Save List_like Json Obj(len={})) Successfully.'.format(
                str(len(data))
            )
        )
