# 테이블 및 컬럼 매핑 정보
TABLES_INFO = {
    "WIZSUJU_ITEMMARK": {
        "alias": "관심상품",
        "columns": {
            "CLCODE": "거래처코드",
            "ITCODE": "상품코드",
            "ITNAME": "상품명",
            "CREATE_DATE": "생성일시"
        }
    },
    "WIZDSALE": {
        "alias": "주문확정(매출확정)",
        "columns": {
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
        }
    }
}

def get_actual_table_and_columns(alias_table_name, alias_column_names):
    """
    별칭 기반 테이블 및 열 이름을 실제 이름으로 변환합니다.
    """
    # 테이블 별칭으로 실제 테이블 검색
    actual_table_name = None
    for table, info in TABLES_INFO.items():
        if info["alias"] == alias_table_name:
            actual_table_name = table
            table_info = info
            break
    if not actual_table_name:
        raise ValueError(f"테이블 별칭 '{alias_table_name}'를 찾을 수 없습니다.")
    
    # 열 별칭 변환
    actual_columns = [
        next(
            (actual for actual, alias in table_info["columns"].items() if alias == alias_col),
            alias_col
        )
        for alias_col in alias_column_names
    ]
    return actual_table_name, actual_columns


# # 테이블 및 컬럼 매핑 정보
# TABLES_INFO = {
#     "WIZSUJU_ITEMMARK": {
#         "alias": "관심상품",
#         "columns": {
#             "CLCODE": "거래처코드",
#             "ITCODE": "상품코드",
#             "ITNAME": "상품명",
#             "CREATE_DATE": "생성일시"
#         }
#     },
#     "WIZDSALE": {
#         "alias": "주문확정(매출확정)",
#         "columns": {
#             "WSD_DATE" : "주문일자", 
#             "WSD_NUM" : "주문일자번호", 
#             "WSD_SEQ" : "주문순번", 
#             "CLCODE" : "거래처코드", 
#             "CLNAME" : "거래처명", 
#             "ITCODE" : "상품코드",
#             "ITNAME" : "상품명",
#             "WSD_BOX" : "박스수량",
#             "WSD_QTY" : "낱개수량",
#             "WSD_AMT" : "주문금액"
#         }
#     }
# }



# def get_actual_table_and_columns(alias_table_name, alias_column_names):
#     """
#     별칭 기반 테이블 및 열 이름을 실제 이름으로 변환합니다.
#     """
#     table_info = TABLES_INFO.get(alias_table_name)
#     if not table_info:
#         raise ValueError(f"테이블 별칭 '{alias_table_name}'를 찾을 수 없습니다.")
    
#     actual_table_name = table_info["actual_name"]
#     actual_columns = [
#         table_info["columns"].get(alias, alias) for alias in alias_column_names
#     ]
#     return actual_table_name, actual_columns