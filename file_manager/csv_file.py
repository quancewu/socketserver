from .util import *
from info import info

def write_variable(path,data_format):
    with open(path,'w') as w:
        w.write(','.join(data_format)+'\r\n')
        
def check_has_variable(path,data_format):
    with open(path,'r') as test_file:
        first_line = test_file.readline()
        if len(first_line) != 0:
            var_list = first_line.replace('\n','').replace('\r','').split(',')
            if var_list == data_format:
                return True
            else:
                return False
        else:
            write_variable(path,data_format)
            return True

def check_last_data(path,data):
    with open(path,'rb') as test_file:
        test_file.seek((-len(','.join(data))-30),2)
        tester = test_file.readlines()
        if len(tester) >= 2:
            if tester[-1].decode().split(',')[1] != data[1]:
                print(tester[-1])
                return True
            else:
                print("same")
                return False
        else:
            return True

def append_csv_file_withcheck(path,data,data_format):
    if  check_has_variable(path,data_format) and check_last_data(path,data): 
        with open(path,'a') as file:
            file.write(','.join(data)+'\r\n')
        return True
    else:
        return False

def append_csv_file(path,data,data_format):
    # check_has_variable(path,data_format)
    with open(path,'a') as file:
        file.write(','.join(data)+'\r\n')
    return True

def save_csv_data(code,y,m,identity,filename,data,data_format):
    data_dir = get_data_dir(
        info.File.save_dir,code,y,m,identity
    )
    # data_dir = get_time_dir_TEOM(info.File.save_dir,data[0])
    # print(data_dir)
    exist_or_create_dir(data_dir)
    file_path = os.path.join(data_dir,"{}.csv".format(filename))
    # print(file_path)
    exist_or_create_file(file_path)
    # print(data)
    if append_csv_file(file_path,data,data_format):
        return True
    else:
        return False