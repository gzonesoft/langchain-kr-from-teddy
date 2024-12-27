def execute_query(table_name: str, columns: list):
    """
    테이블에서 데이터를 조회하는 쿼리를 실행합니다.
    """
    from db.connection import connect_to_mssql

    connection = connect_to_mssql()
    try:
        cursor = connection.cursor()
        column_str = ", ".join(columns)
        query = f"SELECT {column_str} FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()

        # 결과 반환
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
    except Exception as e:
        raise ValueError(f"Query execution failed: {str(e)}")
    finally:
        connection.close()
