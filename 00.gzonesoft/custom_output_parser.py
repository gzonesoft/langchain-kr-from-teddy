from langchain.schema.runnable import Runnable
from mssql_connector import execute_sql_query

class CustomOutputParser(Runnable):
    def invoke(self, input, config=None, **kwargs):
        """
        입력 텍스트에서 SQL 쿼리를 추출하고 실행합니다.
        """
        text = input["content"] if isinstance(input, dict) and "content" in input else input

        # SQL 코드 블록 감지 및 추출
        if "```sql" in text:
            start_idx = text.find("```sql") + len("```sql")
            end_idx = text.find("```", start_idx)
            sql_query = text[start_idx:end_idx].strip()

            # FOR JSON AUTO 제거
            if "FOR JSON AUTO" in sql_query.upper():
                sql_query = sql_query.replace("FOR JSON AUTO", "").strip()

            # SQL 쿼리 실행
            if sql_query.startswith("SELECT"):
                print(f"실행할 SQL 쿼리: {sql_query}")
                results = execute_sql_query(sql_query)
                return {"query": sql_query, "results": results}
            else:
                raise ValueError(f"지원되지 않는 SQL 쿼리 유형입니다: {sql_query}")

        raise ValueError(f"Could not parse LLM output: {text}")
