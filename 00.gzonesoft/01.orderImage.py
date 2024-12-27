# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

# ------------------------------------------------------------------------------------
# 스트리밍 출력 예시..
# ------------------------------------------------------------------------------------
# from langchain_teddynote import logging
# from langchain_openai import ChatOpenAI
# from langchain_teddynote.messages import stream_response

# #추적 설정
# logging.langsmith("CH01-Basic")

# # 객체 생성
# llm = ChatOpenAI(
#     temperature=0.1,  # 창의성 (0.0 ~ 2.0)
#     model_name="gpt-4o",  # 모델명
# )

# # 질의내용
# question = "대한민국의 수도는 어디인가요?"

# # 질의
# # print(f"[답변]: {llm.invoke(question)}")
# # response = llm.invoke(question)

# answer = llm.stream("대한민국의 아름다운 관광지 3곳과 주소를 알려주세요!")
# # 스트리밍 방식으로 각 토큰을 출력합니다. (실시간 출력)
# # 방법-1
# # for token in answer:
# #     print(token.content, end="", flush=True)

# # 방법-2
# stream_response(answer)

# ------------------------------------------------------------------------------------
# 이미지 핸들링 예시..
# ------------------------------------------------------------------------------------
from langchain_teddynote import logging
from langchain_openai import ChatOpenAI
from langchain_teddynote.models import MultiModal
from langchain_teddynote.messages import stream_response

#추적 설정
logging.langsmith("AI-Gzone", set_enable=True)

import sys
# 전달받은 파라미터 출력
if len(sys.argv) > 1:
    file_path1 = sys.argv[1]
    #print(f"입력받은파라미터 : {file_path1}")
else:
    file_path1 = ""
    #print("파라미터가 없습니다.")

# 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    model_name="gpt-4o",  # 모델명
)

system_prompt = """
당신은 발주주문 문서를 해석하는 물류센터 전문가 AI 어시스턴트 입니다. 
당신의 임무는 주어진 발주 주문서를 바탕으로 주문목록을 정리하여 친절하게 답변하는 것입니다.
당신의 부가임무는 재
"""

# user_prompt = """
# 당신에게 주어진 표는 주문서 이미지 입니다. 
# 주문내용이 입력된 회사별로 주문정보를 요약하여 리스트 형태로 작성하여 요약하고, 
# 주문내용이 없는 거래처는 생략해도 무관합니다.
# 주문상품포맷을 참고하여 인식합니다.
# 결과리스트 상품명뒤에 괄호를 넣고 이 코드(문자12자리로 작성하며, 앞의 자리수에 0으로 채워서 기입)를 추가하고,
# 뒤에 주문수량을 표현해서 작성합니다.
# 마지막으로 모든 내용을 포함한 주문서양식으로 html 문서를 작성합니다.
# #주문상품포맷
# 상품코드(숫자4자리)-상품명-주문수(숫자)
# #주문서양식
# |번호|상품명|수량|비고|
# """

user_prompt = """
    당신에게 주어진 표는 주문서 이미지 입니다. 
    주문내용이 입력된 회사별로 주문정보를 요약하여 리스트 형태로 작성하여 요약하고, 
    주문내용이 없는 거래처는 생략해도 무관합니다.
    주문상품포맷을 참고하여 인식합니다.
    결과리스트 상품명뒤에 괄호를 넣고 이 코드(문자12자리로 작성하며, 앞의 자리수에 0으로 채워서 기입)를 추가하고,
    뒤에 주문수량을 표현해서 작성합니다.
    결과리스트는 json형태의 데이타로 최종구성합니다.

    #주문상품포맷
    상품코드(숫자4자리)-상품명-주문수(숫자)
    #json형태 예시:
    { "no": 1, "itcode":"0000009999", "itname":"떡갈비", "qty":1}
"""

# 멀티모달 객체 생성
multimodal_llm_with_prompt = MultiModal(
    llm, system_prompt=system_prompt, user_prompt=user_prompt
)

if (len(file_path1)>0):
    IMAGE_PATH_FROM_FILE = file_path1
    # 이미지 파일로 부터 질의(스트림 방식)
    answer = multimodal_llm_with_prompt.stream(IMAGE_PATH_FROM_FILE, display_image=False)
    # 스트리밍 방식으로 각 토큰을 출력합니다. (실시간 출력)
    stream_response(answer)
else:
    #IMAGE_PATH_FROM_FILE = "/Users/gzonesoft/Library/CloudStorage/SynologyDrive-NAS/AI_2024/OCR_주문서/수신자료_1202(민호형)/KakaoTalk_Photo_2024-12-02-16-09-31 005.jpeg"
    print("이미지 경로가 없어 종료합니다.")