# ---------------------------------------------------------------
# MAC용 ODBC 드라이버 설치명령어 : https://learn.microsoft.com/ko-kr/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16
# ---------------------------------------------------------------
#
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
# brew update
# HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools

# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
# brew update
# brew install msodbcsql@13.1.9.2 mssql-tools@14.0.6.0

# 가상환경 활성화 : poetry shell을 먼저하고 실행확인한다..잊지말것..

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

# LangSmith 추적을 설정합니다. https://smith.langchain.com
# !pip install -qU langchain-teddynote
from langchain_teddynote import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("db_mokwon", set_enable=True)

from langchain.agents import create_react_agent, Tool
from langchain.prompts import PromptTemplate
#from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import pyodbc

# MS-SQL 쿼리 실행 도구 정의
def execute_sql_query(query: str) -> str:
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
        results = cursor.fetchall()

        # 결과를 읽기 쉬운 형식으로 변환
        output = "\n".join([str(row) for row in results])
        
        # 연결 종료
        cursor.close()
        conn.close()
        
        return output if output else "쿼리가 성공적으로 실행되었지만 결과가 없습니다."
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"
    
# LangChain의 @tool 데코레이터를 사용하여 도구 래핑
@tool
def query_mssql_tool(query: str) -> str:
    """
    This tool connects to an MS-SQL database and executes the provided query.
    Provide a valid SQL query as input, and the output will be the query results.
    """
    return execute_sql_query(query)


from langchain.schema.runnable import Runnable
# 사용자 정의 예외
class CustomOutputParserException(Exception):
    pass

# 사용자 정의 OutputParser
class CustomOutputParser(Runnable):
    def invoke(self, input, config=None, **kwargs):
        text = input["content"] if isinstance(input, dict) and "content" in input else input

        # 코드 블록 감지 및 SQL 쿼리 추출
        if "```sql" in text.content:
            start_idx = text.content.find("```sql") + len("```sql")
            end_idx = text.content.find("```", start_idx)
            sql_query = text.content[start_idx:end_idx].strip()
            if sql_query.startswith("SELECT"):
                # SQL 쿼리 실행
                return query_mssql_tool.invoke(sql_query)
        
        raise ValueError(f"Could not parse LLM output: {text}")

    def _call_with_config(self, input, config, **kwargs):
        return self.invoke(input, config=config, **kwargs)


# # LLM 초기화
# 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    model_name="gpt-4o",  # 모델명
)

# 도구 정의
tools = [
    Tool(
        name="Query MS-SQL",
        func=query_mssql_tool,
        description="MS-SQL 데이터베이스를 쿼리할 때 이 도구를 사용하세요. 입력은 유효한 SQL 쿼리여야 합니다."
    )
]


prompt = PromptTemplate(
    input_variables=["input", "tool_names", "tools", "agent_scratchpad", "intermediate_steps"],
    template="""You are an assistant specialized in querying MS-SQL databases.
Your job is to generate and execute SQL queries within a code block.
Use the following tools: {tool_names}
{tools}

### 테이블 및 컬럼 매핑 ###
아래 매핑 정보를 참고하여 사용자가 입력한 별칭(alias)을 실제 테이블 및 컬럼 이름으로 변환하십시오.

테이블 및 컬럼 매핑 정보:
{{
    "WIZSUJU_ITEMMARK": {{
        "alias": "관심상품",
        "columns": {{
            "CLCODE": "거래처코드",
            "ITCODE": "상품코드",
            "ITNAME": "상품명",
            "CREATE_DATE": "생성일자"
        }}
    }},
    "WIZDSALE": {{
        "alias": "주문확정(매출확정)",
        "columns": {{
            "WSD_DATE": "주문일자",
            "WSD_NUM": "주문일자번호",
            "WSD_SEQ": "주문순번",
            "CLCODE": "거래처코드",
            "CLNAME": "거래처명",
            "ITCODE": "상품코드",
            "ITNAME": "상품명",
            "WSD_BOX": "박스수량",
            "WSD_QTY": "낱개수량",
            "WSD_AMT": "주문금액"
        }}
    }}
}}

### 지침 ###
1. 테이블 별칭을 실제 이름으로 변환:
   - "관심상품"은 "WIZSUJU_ITEMMARK"로 변환하십시오.
   - "주문확정(매출확정)"은 "WIZDSALE"로 변환하십시오.

2. 컬럼 별칭을 실제 이름으로 변환:
   - 예: "거래처코드"는 "CLCODE"로 변환하십시오.
   - 예: "상품명"은 "ITNAME"으로 변환하십시오.

3. SQL 쿼리를 아래 형식으로 작성:
```sql
SELECT <컬럼명>
FROM <테이블명>
WHERE <조건>

Question: {input}

Previous steps:
{intermediate_steps}

Current thoughts:
{agent_scratchpad}"""
)

agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=prompt,
    output_parser=CustomOutputParser()
)

# response = agent.invoke({
#     "input": """
#         1.CLIENT이라는 이름을 가지는 테이블의 geonum 컬럼의 최근데이타(역순)) 10건을 조회. 출력결과는 CLCODE, CLNAME, CLPHONE 리턴해주고, 컬럼명과 값을 json형태로 만들어줘.
#     """,
#     "tool_names": "Query MS-SQL",
#     "tools": "Query MS-SQL tool can execute SQL queries.",
#     "agent_scratchpad": "",
#     "intermediate_steps": ""
# })

# print(response)

def main():
    print("에이전트를 실행합니다. 'exit'를 입력하면 종료됩니다.")
    while True:
        user_input = input("사용자 입력: ")
        if user_input.lower() in ["exit", "quit"]:
            print("에이전트를 종료합니다.")
            break
        try:
            response = agent.invoke({
                "input": user_input,
                "tool_names": "Query MS-SQL",
                "tools": "Query MS-SQL tool can execute SQL queries.",
                "agent_scratchpad": "",
                "intermediate_steps": ""
            })
            print("에이전트 응답:")
            print(response)
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
