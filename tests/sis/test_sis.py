import base64
import os
import unittest

from dotenv import load_dotenv

from sis.connection import Connection
from sis.personal.modals.course_warning_DTO import CourseWarningDTO
from sis.personal.modals.injury_record import InjuryRecord
from sis.student_information_system import StudentInformationSystem as SIS


class TestSIS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        初始化 SIS 實例和帳號密碼
        """
        cls.sis = SIS
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
            cls.sis.logout(cls.conn)

    def test_001_login(self):
        """
        測試登入功能，並保存 Connection 物件
        """
        # 確保帳號和密碼正確載入
        self.assertIsNotNone(self.acc, "SIS_LOGIN_ID is not set in .env")
        self.assertIsNotNone(self.pwd, "SIS_LOGIN_PWD is not set in .env")

        # 執行登入
        TestSIS.conn = self.sis.login(self.acc, self.pwd)

        # 驗證登入結果
        self.assertIsInstance(TestSIS.conn, Connection, "Login did not return a Connection object.")
        self.assertEqual(TestSIS.conn.student_id, self.acc, "Student ID does not match the provided account.")

    def test_personal_info(self):
        """
        測試個人資訊功能，使用之前保存的 Connection
        """

        info = self.sis.personal_info.privacy(TestSIS.conn)

        self.assertIsNotNone(info, "Personal info is None.")
        self.assertIsInstance(info, dict, "Personal info is not a dictionary.")

    def test_personal_image(self):
        image_encoded = self.sis.personal_info.personal_image(TestSIS.conn.student_id)

        self.assertIsNotNone(image_encoded, "Personal image is None.")
        self.assertIsInstance(image_encoded, str, "Personal image is not a string.")

        image = base64.b64decode(image_encoded)
        self.assertIsInstance(image, bytes, "Personal image is not bytes.")

        with open("personal_image.jpg", "wb") as f:
            f.write(image)

        self.assertTrue(os.path.exists("personal_image.jpg"), "Personal image file not found.")

        os.remove("personal_image.jpg")

    def test_personal_barcode(self):
        barcode = self.sis.personal_info.personal_barcode(TestSIS.conn.student_id)

        self.assertIsNotNone(barcode, "Personal barcode is None.")
        self.assertIsInstance(barcode, str, "Personal barcode is not a string.")

        barcode_image = base64.b64decode(barcode)

        self.assertIsInstance(barcode_image, bytes, "Personal barcode is not bytes.")

        with open("personal_barcode.jpg", "wb") as f:
            f.write(barcode_image)

        self.assertTrue(os.path.exists("personal_barcode.jpg"), "Personal barcode file not found.")

        os.remove("personal_barcode.jpg")

    def test_course_list_pdf(self):
        pdf_encoded = self.sis.personal_info.personal_course_list_pdf(TestSIS.conn.student_id, "113", "1")

        self.assertIsNotNone(pdf_encoded, "Personal course list pdf is None.")
        self.assertIsInstance(pdf_encoded, str, "Personal course list pdf is not a string.")

        pdf = base64.b64decode(pdf_encoded)

        self.assertIsInstance(pdf, bytes, "Personal course list pdf is not bytes.")

        with open("personal_course_list.pdf", "wb") as f:
            f.write(pdf)

        self.assertTrue(os.path.exists("personal_course_list.pdf"), "Personal course list pdf file not found.")

        os.remove("personal_course_list.pdf")

    def test_injury_record(self):
        injury_records = self.sis.personal_info.injury_record(TestSIS.conn)

        self.assertIsNotNone(injury_records, "Injury records is None.")

        for record in injury_records:
            self.assertIsInstance(record, InjuryRecord, "Injury record is not an InjuryRecord object.")

    def test_course_warning(self):
        course_warnings = self.sis.personal_info.course_warning(TestSIS.conn)

        self.assertIsNotNone(course_warnings, "Course warnings is None.")

        for warning in course_warnings:
            self.assertIsInstance(warning, CourseWarningDTO, "Course warning is not a CourseWarningDTO object.")

if __name__ == "__main__":
    unittest.main()
