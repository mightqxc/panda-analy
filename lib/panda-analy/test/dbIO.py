from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db import models
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()


query_dict = {
    'PandaJob':'panda_id, job_state, error_code, error_message, inputfilebyte, endtime, checksum_adler, duration_time, retry_count, timestamp'}

def build_database(db_path = 'mysql://root:@localhost:3306/panda_analy'):
    engine = create_engine(db_path)
    models.register_models(engine)

def drop_database(db_path = 'mysql://root:@localhost:3306/panda_analy'):
    engine = create_engine(db_path)
    models.unregister_models(engine)


def read_database(table = 'PandaJob',chunksize = 2, db_path = 'mysql://root:@localhost:3306/panda_analy'):
    engine = create_engine(db_path)
    select_str = "select " + query_dict.get(table) + " from " + table
    where_str = ""
    df = pd.read_sql_query(select_str + where_str, con = engine, chunksize = chunksize)
    return df

def write_database(input_file = './test/test.csv',db_path = 'mysql://root:@localhost:3306/panda_analy'):
    engine = create_engine(db_path)
    session = sessionmaker(bind=engine)()
    df = pd.read_csv(input_file)
    for row in df.T.to_dict().values():
        models.Pandajob(row).save(session=session)
    session.commit()
