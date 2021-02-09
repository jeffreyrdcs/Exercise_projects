import os
import sys
import logging
from RDconfig import rdconfig
from RDutils import rdutils, rdmenu, rddb

# create the RDPass logger
#logging.basicConfig(stream=sys.stdout)
rdpass_logger = logging.getLogger('rdpass')
rdpass_logger.setLevel(logging.DEBUG)

# create console handler andset level to debug
ch = logging.StreamHandler()      #stream=sys.stdout
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(name)s/%(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
rdpass_logger.addHandler(ch)



# Start the program
if __name__ == '__main__':
    
    # Initialize parameters
    db_path = rdconfig.config_status['db_path']
    config_path = rdconfig.config_status['config_path']

    # Print the initization
    print('##############################################')
    print('')
    print('           RD Password Manager - v1.0')
    print('')
    print('##############################################')
    
    # If add new DB flag is on, add new DB here
    
    
    # Check if database exist and return an available list for login
    db_avail_list = []
    
    while len(db_avail_list) == 0:
        db_list = rdutils.scan_db_dir(db_path)
        
        ## If no DB exist, generate one
        if len(db_list) == 0:
            rdpass_logger.info(f'Found no DB. Generating a new one.')
            rddb.create_new_db(config_path, db_path, existing_db_list = db_avail_list)
        else:
            rdpass_logger.info(f'Found {len(db_list)} DB.')
        
            ### Check if config file exists for each db
            config_avail_list = rdutils.check_config_file(config_path, db_path)
            
            for db_item, config_flag in zip(db_list, config_avail_list):
                if config_flag == 1:
                    db_avail_list.append(db_item)
                    
            rdpass_logger.info(f'{len(db_avail_list)} DB are available')
            
    # Ask user to login existing DB or create new DB, and select DB from available list if login
    sel_db_name = rdmenu.load_login_menu(db_avail_list)
    
    # login the selected DB, and if successful, reveal choice of the menu
    if rddb.login_db(sel_db_name):
        rdmenu.load_menu_command()


