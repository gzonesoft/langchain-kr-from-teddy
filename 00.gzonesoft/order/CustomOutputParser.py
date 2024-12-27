from langchain.schema.runnable import Runnable
from utils.table_info import get_actual_table_and_columns

class CustomOutputParser(Runnable):
    def invoke(self, input, config=None, **kwargs):
        text = input["content"] if isinstance(input, dict) and "content" in input else input

        # SQL 코드 블록 감지 및 추출
        if "```sql" in text:
            start_idx = text.find("```sql") + len("```sql")
            end_idx = text.find("```", start_idx)
            sql_query = text[start_idx:end_idx].strip()

            # 테이블 및 열 별칭 변환
            table_alias = self.extract_table_alias(sql_query)
            column_aliases = self.extract_column_aliases(sql_query)

            actual_table, actual_columns = get_actual_table_and_columns(table_alias, column_aliases)

            # SQL 쿼리 변환
            sql_query = sql_query.replace(table_alias, actual_table)
            for alias, actual in zip(column_aliases, actual_columns):
                sql_query = sql_query.replace(alias, actual)

            print(f"변환된 SQL 쿼리: {sql_query}")

            # 결과 반환
            return {
                "transformed_query": sql_query,
                "table": actual_table,
                "columns": actual_columns,
            }

        raise ValueError(f"Could not parse LLM output: {text}")

    def extract_table_alias(self, sql_query):
        """
        SQL 쿼리에서 테이블 별칭 추출
        """
        from_clause_start = sql_query.upper().find("FROM")
        where_clause_start = sql_query.upper().find("WHERE", from_clause_start)
        table_alias = sql_query[from_clause_start + 5:where_clause_start].strip()
        return table_alias

    def extract_column_aliases(self, sql_query):
        """
        SQL 쿼리에서 열 별칭 추출
        """
        select_clause_start = sql_query.upper().find("SELECT") + len("SELECT")
        from_clause_start = sql_query.upper().find("FROM")
        column_aliases = sql_query[select_clause_start:from_clause_start].strip().split(",")
        return [col.strip() for col in column_aliases]
