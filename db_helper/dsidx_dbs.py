from db_helper.sqlite3_utils import SqliteHandler

def get_dsidx_apis(db_path):
    """
    ZTOKEN表中查询出 ZTOKENTYPE  func，instm,clm,intfm,intfcm   (1,4,2,6,22)  满足我们要的几个类型
    ZTOKENMETAINFORMATION 连表查询对应的信息
    api_name     ZTOKENNAME
    class_name   ZCONTAINER -- > ZCONTAINERNAME
    type         ZTOKENTYPE
    header_file  ZHEADER --> ZHEADERPATH
    source_sdk   12.1
    source_framework  ZHEADER --> ZFRAMEWORKNAME
    """
    sql = "SELECT T.Z_PK," \
          " T.ZTOKENNAME," \
          " T.ZTOKENTYPE," \
          " T.ZCONTAINER, " \
          "F.ZDECLAREDIN FROM ZTOKEN as T" \
          " INNER JOIN ZTOKENMETAINFORMATION as F ON T.Z_PK=F.ZTOKEN" \
          " WHERE ZTOKENTYPE IN (1,2,4,6,22)"
    return SqliteHandler(db_path=db_path).execute_select(sql,())


def get_container_name(db_path, pk):
    sql = "SELECT ZCONTAINERNAME FROM ZCONTAINER WHERE Z_PK =?;"
    container = SqliteHandler(db_path=db_path).execute_select_one(sql, params=(pk, ))
    if container:
        return container['ZCONTAINERNAME']
    else:
        return None

def get_framework_and_header_name(db_path, pk):
    sql = "SELECT ZFRAMEWORKNAME, ZHEADERPATH FROM ZHEADER WHERE Z_PK = ?;"
    return SqliteHandler(db_path=db_path).execute_select_one(sql, params=(pk, ))