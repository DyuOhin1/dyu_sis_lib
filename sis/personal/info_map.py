import json

def convert(data) -> dict:
    """
    0: 姓名: 王大明
    1: 性別: 1
    2: 身分證字號: A123456789
    3: 生日: 85年01月05日
    4: 經濟狀況: 2
    5: 身分別: 1
    6: 聯絡電話:
    7: 戶籍地址: 台北市大安區信義路5段10號
    8: 通訊地址: 台北市中正區羅斯福路3段10號
    9: 聯絡電話: 02-12345678
    10: 行動電話: 0987654321
    11: eMail: daming.wang@example.com
    12: 宿舍狀況: 1
    13: 宿舍編號: 401-A
    14: 房東姓名: 李四
    15: 房東電話: 0912345678
    16: 現住地址: 高雄市三民區文山路100號
    17: 緊急聯絡人: 王美麗
    18: 關係: 1
    19: 聯絡電話: 02-87654321
    20: 學號: S987654321
    21: 學制: 碩士日間部
    22: 系所: 電機工程學系
    23: 組別: A
    24: 年班: 1年3班
    25: 原畢業學校: 私立光華高中
    26: 畢業日期: 110年06月
    27: 師徒導師: 林志明
    28: 班導師: 吳美華
    29: 婚姻狀況: 0
    30: 配偶姓名:
    31: 宗教: 2
    32: 其他:
    33: 生理缺陷: 0
    34: 其他:
    35: 曾患疾病: 0
    36: 其他:
    37: 殘障手冊:
    38: 介紹人: 張小華
    39: 證號: B987654321
    40: 公司名稱: 偉大科技股份有限公司
    41: 職稱: 軟體工程師
    42: 公司地址: 台北市信義區松智路100號
    43: 稱謂1: 父
    44: 姓名: 王忠誠
    45: 職業: 醫師
    46: 工作機關: 台北市立聯合醫院
    47: 手機: 0911222333
    48: 稱謂2: 母
    49: 姓名: 李美玉
    50: 職業: 教師
    51: 工作機關: 台北市建國中學
    52: 手機: 0922333444
    53: 稱謂3: 兄
    54: 姓名: 王小強
    55: 職業: 工程師
    56: 工作機關: 華碩科技
    57: 手機: 0933444555
    58: 稱謂4: 姊
    59: 姓名: 王小美
    60: 職業: 銀行員
    61: 工作機關: 台灣銀行
    62: 手機: 0933555666
    63: 稱謂5: 弟
    64: 姓名: 王小華
    65: 職業: 學生
    66: 工作機關: 國立台灣大學
    67: 手機: 0955666777
    68: 稱謂6: 妹
    69: 姓名: 王小麗
    70: 職業: 學生
    71: 工作機關: 台北市立師範附中
    72: 手機: 0966777888
    73: 自傳(中): 我是一個積極進取的人，喜歡挑戰自我並探索新領域。
    74: 備註: 無
    75: 自傳(英): I am a proactive individual who enjoys challenging myself and exploring new areas.
    76: 校務用eMail: s987654321@cloud.university.edu
    """
    economic_status_map = {
        "1": "富裕",
        "2": "小康",
        "3": "普通",
        "4": "清寒",
        "5": "貧困",
    }

    identity_type_map = {
        "0": "一般生",
        "1": "身障生",
        "2": "低收入戶子女",
        "3": "中低收入戶子女",
        "4": "原住民",
    }

    religion_map = {
        "1": "無",
        "2": "佛教",
        "3": "基督教",
        "4": "天主教",
        "5": "回教",
        "6": "道教",
    }

    disabilities_map = {
        "1": "無",
        "2": "近視",
        "3": "視覺障礙",
        "4": "聽覺障礙",
        "5": "肢體殘障",
    }

    health_history_map = {
        "1": "無",
        "2": "腦炎",
        "3": "癲癇",
        "4": "心臟病",
        "5": "小兒麻痺",
        "6": "氣喘",
        "7": "過敏症",
        "8": "肺結核",
    }

    emergency_contact_relation_map = {
        "0": "夫",
        "1": "父",
        "2": "母",
        "3": "兄",
        "4": "姐",
        "5": "親戚",
        "6": "本人",
        "7": "祖父",
        "8": "祖母",
        "9": "妻",
    }

    dormitory_status_map = {
        "1": "家裡",
        "2": "親戚家",
        "3": "學校宿舍",
        "4": "校外租屋",
    }

    personal_info_map = {
        "student_id": data[20],
        "name": data[0],
        "gender": "男" if data[1] == "1" else "女",
        "id": data[2],
        "birth_date": data[3],
        "economic_status": economic_status_map.get(data[4], "未知"),
        "identity_type": identity_type_map.get(data[5], "未知"),
        "marital_status": "未婚" if data[29] == "1" else "已婚",
        "spouse_name": data[30],
        "religion": {
            "id": religion_map.get(data[31], "未知"),
            "other": data[32],
        },
        "disabilities": {
            "id": disabilities_map.get(data[33], "未知"),
            "other": data[34],
        },
        "health_history": {
            "disease": health_history_map.get(data[35], "未知"),
            "other": data[36],
        },
        "emergency_contact": {
            "name": data[17],
            "relation": emergency_contact_relation_map.get(data[18], "未知"),
            "phone": data[19],
        },
        "disabilities_certificate": data[37],
        "introducer": {
            "id": data[38],
            "company": data[39],
            "title": data[40],
            "job": data[41],
            "company_address": data[42],
        },
        "education": {
            "program": data[21],
            "department": data[22],
            "class": {
                "id": data[24],
                "teacher": data[28],
            },
            "mentor": data[27],
            "previous_school": data[25],
            "graduation_date": data[26],
        },
        "contact_info": {
            "mailing_address": data[8],
            "permanent_address": data[7],
            "telephone": data[9],
            "mobile": data[10],
        },
        "dormitory": {
            "status": dormitory_status_map.get(data[12], "未知"),
            "room_number": data[13],
            "address": data[16],
            "landlord": {
                "name": data[14],
                "phone": data[15],
            },
        },
        "family_info": {
            "father": {
                "name": data[44],
                "phone": data[46],
                "job": data[45],
            },
            "mother": {
                "name": data[49],
                "phone": data[51],
                "job": data[50],
            },
            "other": [
                {
                    "title": data[53],
                    "name": data[54],
                    "job": data[55],
                    "company": data[56],
                },
                {
                    "title": data[58],
                    "name": data[59],
                    "job": data[60],
                    "company": data[61],
                },
                {
                    "title": data[63],
                    "name": data[64],
                    "job": data[65],
                    "company": data[66],
                },
                {
                    "title": data[69],
                    "name": data[70],
                    "job": data[71],
                    "company": data[72],
                },
            ]
        },
        "biography": {
            "chinese": data[73],
            "english": data[75],
        },
        "email": {
            "campus": data[76],
            "personal": data[11],
        },
    }

    return personal_info_map