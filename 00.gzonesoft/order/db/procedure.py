def call_procedure(procedure_name: str, params: dict):
    """
    MS-SQL 데이터베이스에서 지정된 프로시저를 호출합니다.
    """
    from db.connection import connect_to_mssql

    connection = connect_to_mssql()
    try:
        cursor = connection.cursor()

        # 프로시저 호출을 위한 파라미터 설정
        param_placeholders = ", ".join("?" for _ in params)
        sql = f"EXEC {procedure_name} {param_placeholders}"
        param_values = list(params.values())

        # 프로시저 실행
        cursor.execute(sql, param_values)
        results = cursor.fetchall()

        # 결과 반환
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
    except Exception as e:
        raise ValueError(f"Procedure call failed: {str(e)}")
    finally:
        connection.close()


# def call_procedure(connection, procedure_name: str, params: list):
#     """
#     연결된 데이터베이스에서 지정된 프로시저를 호출합니다.
#     """
#     try:
#         cursor = connection.cursor()
#         cursor.callproc(procedure_name, params)
#         results = cursor.fetchall()
#         return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
#     except Exception as e:
#         raise ValueError(f"Procedure call failed: {str(e)}")


# def call_procedure(connection, procedure_name: str, params: list):
#     """
#     연결된 데이터베이스에서 지정된 프로시저를 호출합니다.
#     """
#     try:
#         cursor = connection.cursor()
#         cursor.callproc(procedure_name, params)
#         results = cursor.fetchall()
#         return results
#     except Exception as e:
#         raise ValueError(f"Procedure call failed: {str(e)}")
