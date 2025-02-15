import os
import unittest
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from sis.connection import Connection
from sis.course.leave.constant.leave_result import LeaveResult
from sis.course.leave.constant.leave_type import LeaveType
from sis.course.leave.modals.leave_form_data.course_leave_form_data import CourseLeaveFormData
from sis.student_information_system import StudentInformationSystem as SIS


class TestCourseLeave(unittest.TestCase):
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

    def test_001_login(self):
        """
        測試登入功能，並保存 Connection 物件
        """
        # 確保帳號和密碼正確載入
        self.assertIsNotNone(self.acc, "SIS_LOGIN_ID is not set in .env")
        self.assertIsNotNone(self.pwd, "SIS_LOGIN_PWD is not set in .env")

        # 執行登入
        TestCourseLeave.conn = self.sis.login(self.acc, self.pwd)

        # 驗證登入結果
        self.assertIsInstance(TestCourseLeave.conn, Connection, "Login did not return a Connection object.")
        self.assertEqual(TestCourseLeave.conn.student_id, self.acc, "Student ID does not match the provided account.")

    def setUp(self):
        """
        登入
        """
        if not TestCourseLeave.conn:
            self.test_001_login()

    @classmethod
    def tearDownClass(cls):
        """
        登出
        """
        if cls.conn:
            cls.sis.logout(cls.conn)

    def test_002_info(self):
        course = self.sis.course_leave.info(
            s_id=TestCourseLeave.conn.student_id,
            s_time=datetime(2025, 2, 20),
            e_time=datetime(2025, 2, 20)
        )

        self.assertIsNotNone(course, "Course leave info is None.")
        self.assertIsInstance(course, list, "Course leave info is not a list.")

        return [c for c in course if c.course_period <= 4]

    def test_003_send(self):
        result = self.sis.course_leave.send(
            TestCourseLeave.conn,
            CourseLeaveFormData(
                course=self.test_002_info(),
                leave_type=LeaveType.PERSONAL,
                reason="市價",
            )
        )

        self.assertEqual(result, LeaveResult.SUCCESS, "Course leave send failed.")

    def test_004_list(self):
        course = self.sis.course_leave.list(
            TestCourseLeave.conn,
            datetime(2025, 2, 20),
            datetime(2025, 2, 20)
        )

        self.assertIsNotNone(course, "Course leave list is None.")
        self.assertIsInstance(course, list, "Course leave list is not a list.")

        return course

    def test_005_detail(self):
        """
        還做不了，還沒開學
        """
        pass

    def test_006_submit_document(self):
        data = self.test_004_list()[0]
        with open(Path(__file__).resolve().parent.parent.parent / "test/a.jpg", "rb") as f:
            r = self.sis.course_leave.submit_document(
                TestCourseLeave.conn,
                data.id,
                f
            )

            self.assertTrue(r, "Course leave submit document failed.")

    def test_007_cancel(self):
        data = self.test_004_list()[0]
        r = self.sis.course_leave.cancel(
            TestCourseLeave.conn,
            data.id
        )

        self.assertTrue(r, "Course leave cancel failed.")
