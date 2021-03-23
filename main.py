import threading
import argparse
from main_mixins.mixin import (
    MainBase,SocktSeverMixin,D11Logger,
    ApiForNahoMixin,LoggerMixin,SQLiteMixin
)

class D11_Logger(
    D11Logger,
    SocktSeverMixin,
    ApiForNahoMixin,
    LoggerMixin,
    SQLiteMixin,
    MainBase
): pass


main_mapping = {
    'D11': D11_Logger,
    # 'TEOM': TEOM_Logger,
    # 'Cn2':Cn_Logger,
    # 'SWS250':SWS250_Logger,
    # 'setupno':setup,
    # 'setupyes':setup,
}

def get_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dl',type=str,help='TEOM,CN2,SWS250,no,D11')
    # parser.add_argument('dpb',type=str,help='yes,no')
    args = parser.parse_args()
    arg = args.dl#+args.dpb
    main = main_mapping[arg] 
    print('Info Get {}'.format(str(main)))
    return main 

if __name__ == "__main__":
    main = get_main()
    main()
    # print(threading.enumerate())