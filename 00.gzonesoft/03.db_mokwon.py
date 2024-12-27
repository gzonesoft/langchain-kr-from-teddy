from dotenv import load_dotenv
from langchain_teddynote import logging
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, Tool
from langchain.prompts import PromptTemplate
from custom_output_parser import CustomOutputParser
from mssql_connector import execute_sql_query
from langchain.tools import tool

# API KEY 정보 로드
load_dotenv()

# 로그 설정
logging.langsmith("db_mokwon", set_enable=True)

# MS-SQL 쿼리 실행 도구 정의
@tool
def query_mssql_tool(query: str) -> str:
    """
    This tool connects to an MS-SQL database and executes the provided query.
    Provide a valid SQL query as input, and the output will be the query results.
    """
    return execute_sql_query(query)

# LLM 초기화
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 설정
    model_name="gpt-4"
)

# 도구 정의
tools = [
    Tool(
        name="Query MS-SQL",
        func=query_mssql_tool,
        description="MS-SQL 데이터베이스를 쿼리할 때 이 도구를 사용하세요. 입력은 유효한 SQL 쿼리여야 합니다."
    )
]

# 프롬프트 정의
prompt = PromptTemplate(
    input_variables=["input", "tool_names", "tools", "agent_scratchpad", "intermediate_steps"],
    template="""You are an assistant specialized in querying MS-SQL databases.
    Your job is to generate and execute SQL queries within a code block.
    Use the following tools: {tool_names}
    {tools}
    Question: {input}
    Previous steps:
    {intermediate_steps}
    Current thoughts:
    {agent_scratchpad}"""
)

# 에이전트 생성
agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=prompt,
    output_parser=CustomOutputParser()
)

def main():
    """
    사용자 입력을 받아 MS-SQL 데이터베이스 쿼리를 수행하는 에이전트를 실행합니다.
    """
    print("에이전트를 실행합니다. 'exit'를 입력하면 종료됩니다.")
    while True:
        user_input = input("사용자 입력: ")
        if user_input.lower() in ["exit", "quit"]:
            print("에이전트를 종료합니다.")
            break
        try:
            # 에이전트 호출
            response = agent.invoke({
                "input": user_input,
                "tool_names": "Query MS-SQL",
                "tools": "Query MS-SQL tool can execute SQL queries.",
                "agent_scratchpad": "",
                "intermediate_steps": ""
            })
            
            # 응답 출력
            print("에이전트 응답:")
            print(response.get("results", "결과 없음"))
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
