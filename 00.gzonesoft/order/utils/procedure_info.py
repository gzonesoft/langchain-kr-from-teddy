PROCEDURE_INFO = {
    "GET_FAV_ITEMLIST_01": {
        "alias": "관심상품조회",
        "parameters": {
            "I_CLCODE": "거래처코드",
            "I_ITSCODE": "분류코드1",
            "I_ITSCODE2": "분류코드2",
            "I_KEYWORD": "키워드",
            "I_ITCODE": "상품코드",
            "I_PAGE_SIZE": "페이지크기",
            "I_PAGE_NUM": "페이지번호",
            "I_INPUT_USER": "사용자번호"
        }
    }
}

def get_procedure_info(procedure_alias: str):
    """
    프로시저 별칭을 통해 프로시저 정보를 반환합니다.
    """
    for procedure_name, info in PROCEDURE_INFO.items():
        if info["alias"] == procedure_alias:
            return procedure_name, info
    raise ValueError(f"프로시저 별칭을 찾을 수 없습니다: {procedure_alias}")
