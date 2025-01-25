import os
import unittest

from dotenv import load_dotenv

from icloud.icloud import iCloud
from sis.connection import Connection


class TestICloud(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        初始化 iCloud 實例和帳號密碼
        """
        cls.icloud = iCloud
        load_dotenv()
        cls.acc = os.getenv('SIS_LOGIN_ID')
        cls.pwd = os.getenv('SIS_LOGIN_PWD')
        cls.conn = None  # 保存 Connection 物件

    @classmethod
    def tearDownClass(cls):
        """
        登出
        """
        if cls.conn:
            cls.icloud.logout(cls.conn)

    def test_001_login(self):
        """
        測試登入功能，並保存 Connection 物件
        """
        # 確保帳號和密碼正確載入
        self.assertIsNotNone(self.acc, "SIS_LOGIN_ID is not set in .env")
        self.assertIsNotNone(self.pwd, "SIS_LOGIN_PWD is not set in .env")

        # 執行登入
        TestICloud.conn = self.icloud.login(self.acc, self.pwd)

        # 驗證登入結果
        self.assertIsInstance(TestICloud.conn, Connection, "Login did not return a Connection object.")
        self.assertEqual(TestICloud.conn.student_id, self.acc, "Student ID does not match the provided account.")

    def test_personal_info(self):
        self.icloud.personal_information.scholarship_record(TestICloud.conn)
        self.icloud.personal_information.injury_record(TestICloud.conn)
        self.icloud.personal_information.advisors(TestICloud.conn)
        self.icloud.personal_information.dorm_record(TestICloud.conn)
        self.icloud.personal_information.military_record(TestICloud.conn)
        self.icloud.personal_information.printer_point(TestICloud.conn)
        self.icloud.personal_information.proof_of_enrollment(TestICloud.conn)
        self.icloud.personal_information.proof_of_enrollment_pdf(TestICloud.conn, "113", "1")
        self.icloud.personal_information.rewards_and_penalties_record(TestICloud.conn)

        self.icloud.course_information.timetable(TestICloud.conn, "113", "1")
        self.icloud.course_information.grade(TestICloud.conn, "113", "1")
        self.icloud.course_information.attendance(TestICloud.conn)
        self.icloud.course_information.annual_grade(TestICloud.conn)
        self.icloud.course_information.performance_grade(TestICloud.conn)
        self.icloud.course_information.timetable_pdf(TestICloud.conn, "113", "1")

        self.icloud.advisor_info(TestICloud.conn, "2000003168")
