import pyodbc
import json

def execute_sql_query(query: str) -> str:
    """
    MS-SQL 데이터베이스에서 SQL 쿼리를 실행하고 결과를 JSON으로 변환하여 반환합니다.
    """
    try:
        # MS-SQL 연결 정보 설정
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=1.246.219.165;'  # 서버 이름으로 대체
            'DATABASE=WIZSALE_043_0043;'  # 데이터베이스 이름으로 대체
            'UID=sa;'  # 사용자 이름으로 대체
            'PWD=sch090526@;'  # 비밀번호로 대체
        )

        cursor = conn.cursor()
        cursor.execute(query)

        # 결과 가져오기
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        # 연결 종료
        cursor.close()
        conn.close()

        return json.dumps(results, ensure_ascii=False, indent=4)  # JSON 직렬화
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"


# import pyodbc
# import json

# def execute_sql_query(query: str) -> str:
#     """
#     MS-SQL 데이터베이스에서 SQL 쿼리를 실행하고 결과를 JSON으로 변환하여 반환합니다.
#     """
#     try:
#         # MS-SQL 연결 정보 설정
#         conn = pyodbc.connect(
#             'DRIVER={ODBC Driver 17 for SQL Server};'
#             'SERVER=1.246.219.165;'  # 서버 이름으로 대체
#             'DATABASE=WIZSALE_043_0043;'  # 데이터베이스 이름으로 대체
#             'UID=sa;'  # 사용자 이름으로 대체
#             'PWD=sch090526@;'  # 비밀번호로 대체
#         )

#         cursor = conn.cursor()
#         cursor.execute(query)

#         # 결과 가져오기
#         columns = [column[0] for column in cursor.description]  # 컬럼 이름
#         rows = cursor.fetchall()  # 결과 데이터
#         json_output = [dict(zip(columns, row)) for row in rows]  # JSON 형식으로 변환

#         # 연결 종료
#         cursor.close()
#         conn.close()

#         return json.dumps(json_output, ensure_ascii=False, indent=4)  # JSON 직렬화
#     except Exception as e:
#         return f"오류가 발생했습니다: {str(e)}"
