'''
Here we will create the engine variable that will connect to the database
engine, the session variable to be able to perform operations on the tables,
and the variable Base which is inherited to create in the model the classes
that make references to the references to the different tables in the model.
'''
# import logging
# import logging.config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from libs.config import settings
import sys
sys.path.append('')

# Sqlalchemy
# engine is created to be called as modules from other scripts
engine = create_engine(settings.DATABASE_URL)
# session is created to be called as modules from other scripts
Session = sessionmaker(bind=engine)
session = Session()
# base is created to be called as modules from other scripts
Base = declarative_base()

# Logging
# Opening configuration file
# logging.config.fileConfig('./config_logs.conf')
# # Create logger
# logger = logging.getLogger('dbLogger')
# logger.info('probando dbLogger')


# Class to add functionality
class CommonActions:
    '''
    This class groups actions or tasks in common
    for the different scripts or classes.
    '''
    def truncate_tables(self) -> None:
        '''
        This methods performs a truncate
        to the tables
        '''
        tables = 'target_customers, transactions, current_customers,products'
        try:
            session.execute(f"TRUNCATE TABLE {tables}")
            session.commit()
            session.close()
        except Exception:
            # logger.error('Truncate Failed')
            raise ('Trancate Failed')
        else:
            print('Truncated Tables')
            # logger.info('Truncated Tables')
