# processing/training_data.py

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_tables( user, password, host, port, database,create_view,insert_into_table,get_engine,execute_engine,):
    logging.info("Setting Engine Connection")
    engine = get_engine(user, password, host, port, database)
    logging.info("Creating View")
    execute_engine(engine,create_view)
    logging.info("Inserting View")
    execute_engine(engine,insert_into_table)



    