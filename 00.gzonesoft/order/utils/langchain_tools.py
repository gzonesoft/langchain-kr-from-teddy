from utils.table_info import get_actual_table_and_columns
from db.query import execute_query
from db.procedure import call_procedure
from langchain.tools import tool


@tool
def summarize_table_tool(table_name: str) -> str:
    """
    테이블의 스키마 요약 정보를 반환합니다.
    """
    table_info = get_actual_table_and_columns(table_name, [])
    if not table_info:
        return f"테이블 정보를 찾을 수 없습니다: {table_name}"
    actual_table_name = table_info[0]
    column_summaries = ", ".join(
        [f"{alias} (actual: {actual})" for alias, actual in table_info[1].items()]
    )
    return f"테이블 '{table_name}' (실제 이름: {actual_table_name})의 컬럼 정보: {column_summaries}"


@tool
def execute_query_tool(table_name: str, columns: list, filters: dict = None) -> list:
    """
    지정된 테이블에서 데이터를 조회합니다.
    - table_name: 테이블 별칭
    - columns: 조회할 컬럼 별칭 목록
    - filters: 필터 조건 (딕셔너리 형식: {별칭: 값})
    """
    # 테이블 및 컬럼 별칭 변환
    actual_table, actual_columns = get_actual_table_and_columns(table_name, columns)

    # SQL 필터 생성
    filter_clause = ""
    if filters:
        actual_filters = {
            get_actual_table_and_columns(table_name, [alias])[1][0]: value
            for alias, value in filters.items()
        }
        filter_clause = " WHERE " + " AND ".join(
            [f"{col} = '{val}'" for col, val in actual_filters.items()]
        )

    # SQL 쿼리 생성
    sql_query = f"SELECT {', '.join(actual_columns)} FROM {actual_table}{filter_clause} LIMIT 10"

    # 쿼리 실행
    print(f"실행할 SQL 쿼리: {sql_query}")
    results = execute_query(actual_table, actual_columns)
    return results


@tool
def call_procedure_tool(procedure_name: str, params: dict) -> list:
    """
    저장 프로시저를 호출합니다.
    - procedure_name: 프로시저 이름
    - params: 매개변수 딕셔너리
    """
    print(f"호출할 프로시저: {procedure_name}, 매개변수: {params}")
    results = call_procedure(procedure_name, params)
    return results
