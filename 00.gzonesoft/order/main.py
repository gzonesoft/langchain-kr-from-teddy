from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, Tool
from langchain.prompts import PromptTemplate
from utils.langchain_tools import summarize_table_tool, execute_query_tool, call_procedure_tool
from dotenv import load_dotenv
from CustomOutputParser import CustomOutputParser

# API KEY 정보 로드
load_dotenv()

def main():
    # OpenAI Chat 모델 초기화
    llm = ChatOpenAI(
        temperature=0.1,
        model_name="gpt-4"
    )

    # LangChain 도구 정의
    tools = [
        Tool(name="Summarize Table", func=summarize_table_tool, description="Summarize the table schema."),
        Tool(name="Execute Query", func=execute_query_tool, description="Run a SQL query on the database."),
        Tool(name="Call Procedure", func=call_procedure_tool, description="Call a stored procedure in the database.")
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

    # LangChain 에이전트 생성
    agent = create_react_agent(
        tools=tools,
        llm=llm,
        prompt=prompt,
        output_parser=CustomOutputParser()  # 수정된 OutputParser 추가
    )

    # 에이전트 실행
    print("에이전트를 실행합니다. 'exit'를 입력하면 종료됩니다.")
    while True:
        user_input = input("사용자 입력: ")
        if user_input.lower() in ["exit", "quit"]:
            print("에이전트를 종료합니다.")
            break
        try:
            response = agent.invoke({
                "input": user_input,
                "agent_scratchpad": "",
                "intermediate_steps": ""
            })
            print(f"에이전트 응답: {response}")
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
