from enum import Enum

class Department(str, Enum):
    CS = "5100"
    ENGINEERING = "2000"
    HR_PUBLIC_RELATIONS = "5131"
    PERSONNEL_OFFICE = "2200"
    PR_CENTER = "2971"
    PR_SERVICE_OFFICE = "2970"
    DOCUMENTS_GROUP = "2107"
    DAYCARE_CENTER = "4800"
    FOREIGN_LANG_COLLEGE = "2005"
    SUSTAINABILITY_OFFICE = "4700"
    BIO_RESOURCES_COLLEGE = "2006"
    BIO_RESOURCES_DEPT = "5180"
    BIOMED_DEPT = "5512"
    LIVING_SUPPORT_GROUP = "2709"
    BUSINESS_ADMIN = "5110"
    MARKETING_PLANNING = "3121"
    VEHICLE_RESEARCH_CENTER = "4200"
    MULTIMEDIA_PROGRAM = "5096"
    ADMIN_AFFAIRS = "2953"
    ADMIN_SERVICE = "3122"
    MATERIAL_SCIENCE = "5240"
    NETWORK_GROUP = "2602"
    CROSS_STRAIT_CENTER = "2955"
    OTHER = "8888"
    ADMISSION_SERVICE = "2421"
    SPACE_DESIGN = "5060"
    ARCHITECTURE_RESEARCH = "6600"
    RESEARCH_DEVELOPMENT = "2900"
    ENGLISH_DEPT = "5212"
    INDIGENOUS_STUDENT_CENTER = "2430"
    TEACHER_TRAINING_CENTER = "4210"
    CAMPUS_SECURITY = "2750"
    PRESIDENT_OFFICE = "2001"
    ADMIN_GROUP = "2601"
    QUALITY_CONTROL_GROUP = "2462"
    RESEARCH_OFFICE = "4500"
    DEVELOPMENT_GROUP = "2461"
    QUALITY_ASSURANCE = "2460"
    CAMPUS_ENVIRONMENT = "4012"
    FIRE_SAFETY_PROGRAM = "5082"
    BAKERY_PROGRAM = "5659"
    SECRETARY_OFFICE = "2100"
    FINANCE_MANAGEMENT = "2810"
    FINANCE_DEPT = "5190"
    INTL_BUSINESS = "5150"
    INTL_AFFAIRS_CENTER = "2954"
    INTL_SPEC_PROGRAM = "2958"
    INTL_CROSS_STRAIT = "2950"
    INTL_LANGUAGE_CENTER = "4007"
    EXTENSION_OFFICE = "3120"
    LIBRARY_CATALOG = "2502"
    EDU_RESEARCH_INSTITUTE = "6410"
    ACADEMIC_AFFAIRS = "2400"
    TEACHING_ADMIN = "3201"
    TEACHING_RESOURCE_CENTER = "2407"
    INDUSTRY_ACADEMIA_CENTER = "4104"
    INDUSTRY_COOP_GROUP = "2905"
    HR_FIRST_GROUP = "2202"
    DESIGN_ARTS_COLLEGE = "2004"
    PART_TIME_MASTER_DESIGN_ARTS = "7001"
    MASTER_DESIGN_ARTS = "6001"
    DESIGN_DEPT = "5032"
    GENERAL_EDU_CENTER = "9010"
    FINE_ARTS = "5070"
    CREATIVE_DESIGN = "4023"
    INNOVATION_INCUBATION = "2910"
    CHINESE_TEACHING_CENTER = "4026"
    OPTOMETRY_DEPT = "5290"
    REGISTRATION_GROUP = "2401"
    MEDIA_ARTS = "5091"
    ACCOUNTING = "2300"
    ACCOUNTING_MANAGEMENT = "5121"
    RESOURCE_MANAGEMENT = "2811"
    SPORTS_MANAGEMENT = "5172"
    IT_CENTER = "2600"
    ELECTRICAL_ENGINEERING = "5040"
    LIBRARY = "2500"

    @property
    def description(self):
        """ 取得部門的實際名稱 """
        descriptions = {
            "5100": "資訊工程學系",
            "2000": "工學院院部",
            "5131": "人力資源暨公共關係學系",
            "2200": "人事室",
            "2971": "公關事務中心",
            "2970": "公關事務暨校友服務處",
            "2107": "文書管理組",
            "4800": "日照中心籌備處",
            "2005": "外語學院院部",
            "4700": "永續發展辦公室",
            "2006": "生物科技暨資源學院院部",
            "5180": "生物資源學系",
            "5512": "生物醫學系",
            "2709": "生活與住宿輔導組",
            "5110": "企業管理學系",
            "3121": "企劃行銷組",
            "4200": "先進車輛科技研究中心",
            "5096": "多媒體數位內容學士學位學程",
            "2953": "行政事務組",
            "3122": "行政服務組",
            "5240": "材料科學與工程學系",
            "2602": "系統網路組",
            "2955": "兩岸事務中心",
            "8888": "其它",
            "2421": "招生暨就學服務中心",
            "5060": "空間設計學系",
            "6600": "建築研究所",
            "2900": "研究發展處",
            "5212": "英語學系",
            "2430": "原住民族學生資源中心",
            "4210": "師資培育中心",
            "2750": "校安中心",
            "2001": "校長室",
            "2601": "校務行政組",
            "2462": "校務品保組",
            "4500": "校務研究辦公室",
            "2461": "校務發展組",
            "2460": "校務發展暨品保處",
            "4012": "校園環境管理暨安全衛生中心",
            "5082": "消防安全學士學位學程",
            "5659": "烘焙暨飲料調製學士學位學程",
            "2100": "秘書室",
            "2810": "財物管理組",
            "5190": "財務金融學系",
            "5150": "國際企業管理學系",
            "2954": "國際事務中心",
            "2958": "國際專修部",
            "2950": "國際暨兩岸交流處",
            "4007": "國際語言中心",
            "3120": "推廣教育處",
            "2502": "採訪編目組",
            "6410": "教育專業發展研究所",
            "2400": "教務處",
            "3201": "教學行政組",
            "2407": "教學資源中心",
            "4104": "產學中心",
            "2905": "產學合作組",
            "2202": "第一組",
            "2004": "設計暨藝術學院院部",
            "7001": "設計暨藝術學院碩士在職專班",
            "6001": "設計暨藝術學院碩士班",
            "5032": "設計學系",
            "9010": "通識教育中心",
            "5070": "造形藝術學系",
            "4023": "創意設計中心",
            "2910": "創新育成中心",
            "4026": "華語教學中心",
            "5290": "視光學系",
            "2401": "註冊組",
            "5091": "傳播藝術學士學位學程",
            "2300": "會計室",
            "5121": "會計與資訊管理學系",
            "2811": "資源管理組",
            "5172": "運動健康管理學系",
            "2600": "電子計算機中心",
            "5040": "電機工程學系",
            "2500": "圖書館",
        }
        return descriptions[self.value]
