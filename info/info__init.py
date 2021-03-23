import os,sys
import platform
from file_manager.util import exist_or_create_dir

class upload_SQL_NAHO_config:
    config = dict(
            database="name",
            host = 'IP',
            user = 'username',
            password = 'userpassword',
            port = 5432,
                )
    
class D11dic:
    sql_type = 'pgsql'
    code = 'D11'
    y = 2020
    m = 10
    identity = 1
    filename = 'D11_data'
    sql_data_format = dict(
        id = 'integer primary key autoincrement',
        datetimeutc = 'char(20) UNIQUE',
        tsp = 'real',
        pm_10 = 'real',
        pm_4 = 'real',
        pm_25 = 'real',
        pm_1 = 'real',
        pm_coarse = 'real',
        inhalable = 'real',
        thoracic = 'real',
        respirable = 'real',
        pm_10_iaq = 'real',
        pm_25_iaq = 'real',
        pm_1_iaq = 'real',
        tc = 'real',
        c0 = 'integer',
        c1 = 'integer',
        c2 = 'integer',
        c3 = 'integer',
        c4 = 'integer',
        c5 = 'integer',
        c6 = 'integer',
        c7 = 'integer',
        c8 = 'integer',
        c9 = 'integer',
        c10 = 'integer',
        c11 = 'integer',
        c12 = 'integer',
        c13 = 'integer',
        c14 = 'integer',
        c15 = 'integer',
        c16 = 'integer',
        c17 = 'integer',
        c18 = 'integer',
        c19 = 'integer',
        c20 = 'integer',
        c21 = 'integer',
        c22 = 'integer',
        c23 = 'integer',
        c24 = 'integer',
        c25 = 'integer',
        c26 = 'integer',
        c27 = 'integer',
        c28 = 'integer',
        c29 = 'integer',
        c30 = 'integer',
        m0 = 'real',
        m1 = 'real',
        m2 = 'real',
        m3 = 'real',
        m4 = 'real',
        m5 = 'real',
        m6 = 'real',
        m7 = 'real',
        m8 = 'real',
        m9 = 'real',
        m10 = 'real',
        m11 = 'real',
        m12 = 'real',
        m13 = 'real',
        m14 = 'real',
        m15 = 'real',
        m16 = 'real',
        m17 = 'real',
        m18 = 'real',
        m19 = 'real',
        m20 = 'real',
        m21 = 'real',
        m22 = 'real',
        m23 = 'real',
        m24 = 'real',
        m25 = 'real',
        m26 = 'real',
        m27 = 'real',
        m28 = 'real',
        m29 = 'real',
        m30 = 'real',
        location = 'integer',
        gravimetric_factor =  'integer',
        error_code = 'integer',
        qbatt = 'integer',
        im = 'integer',
        temperature = 'real',
        relative_humidity = 'real',
        wind_speed = 'real',
        pressure = 'real',
        wind_direction = 'real',
        precipitation_amount = 'real',
        storage_interval = 'integer',
        p_weight = 'real',
        p_vol = 'real',
        rh_i = 'real',
        temp_i = 'real',
        latitude = 'real',
        longitude = 'real',
        height = 'real',
        flow = 'real',
        flow_sensor = 'real',
        dc_voltage = 'integer',
        dc_dark = 'integer',
        dc_high = 'integer',
        c0_high = 'integer',
        c0_dark = 'integer',
        laser_low = 'integer',
        laser_high = 'integer',
        receive_datetimeutc = 'char(27)',
        upload_flag = 'integer'
    )

class File:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir,'info')
    log_dir = os.path.join(base_dir,'log_file')
    save_dir = os.path.join(base_dir,'data_file')
    script_dir = os.path.join(base_dir,'script_n_file')

    exist_or_create_dir(base_dir)
    exist_or_create_dir(config_dir)
    exist_or_create_dir(log_dir)
    exist_or_create_dir(save_dir)

    json_format = 'list_like'

    if platform.system() == "Linux":
        checker_dir = "/bin/"
        job_dir = "/bin/"
        service_dir = "/lib/systemd/system/"
    else:
        checker_dir = os.path.join(base_dir,'bin')

if __name__ == "__main__":
    device = D11dic()
    print(D11dic)