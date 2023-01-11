from typing import Any, Dict, List, Tuple


def parse_choices(choices: List[Tuple]) -> List[Dict[str, Any]]:
    return [{"value": i[0], "label": i[1]} for i in choices]


# def constant_values() -> dict:
#     return {
#         "TÀI LIỆU": ["khoá 1", "THPT"],
#     }



# theem type get all docs, courses
# bỏ authen cho get all docs, courses
