from .sqlite3_utils import SqliteHandler
from config import db_names


def create_relate_tables():
    sql = ("create table %s("
           "id integer primary key AUTOINCREMENT not null, "
           "api_name varchar, "
           "class_name varchar, "
           "type varchar, "
           "header_file varchar, "
           "source_sdk varchar, "
           "source_framework varchar )")
    for db_name in db_names.keys():
        SqliteHandler().execute_sql(sql % (db_names[db_name]), ())
