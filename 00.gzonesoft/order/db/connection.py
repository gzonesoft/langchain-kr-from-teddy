import pyodbc

def connect_to_mssql(connection_info: dict):
    """
    지정된 연결 정보를 사용하여 MS-SQL 데이터베이스에 연결합니다.
    """
    try:
        # MS-SQL 연결 정보 설정
        conn_str = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=1.246.219.165;'  # 서버 이름으로 대체
            'DATABASE=WIZSALE_043_0043;'  # 데이터베이스 이름으로 대체
            'UID=sa;'  # 사용자 이름으로 대체
            'PWD=sch090526@;'  # 비밀번호로 대체
        )
        connection = pyodbc.connect(conn_str)
        return connection
    except Exception as e:
        raise ValueError(f"Database connection failed: {str(e)}")
