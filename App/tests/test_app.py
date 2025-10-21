import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Staff, Shift, Report
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class AdminUnitTests(unittest.TestCase):

    def test_create_admin_user(self):
        newAdmin = Admin("Chimmy", "changapass")
        assert newAdmin.name == "Chimmy"

    def test_admin_get_json(self):
        admin = Admin("Chimmy", "changapass")
        admin_json = admin.get_json()
        self.assertDictEqual(admin_json, {"id":None, "name":"Chimmy", "createdShifts":[]})

    def test_hashed_admin_password(self):
        admin = Admin("Chimmy", "changapass")
        assert admin.password != "changapass"

    def test_check_admin_password(self):
        admin = Admin("Chimmy", "changapass")
        assert admin.check_password("changapass")

class StaffUnitTests(unittest.TestCase):

    def test_create_staff_user(self):
        newStaff = Staff("TestStaff", "staffpass")
        assert newStaff.name == "TestStaff"

    def test_staff_get_json(self):
        staff = Staff("TestStaff", "staffpass")
        staff_json = staff.get_json()
        self.assertDictEqual(staff_json, {"id":None, "name":"TestStaff", "shifts":[]})

    def test_hashed_staff_password(self):
        staff = Staff("TestStaff", "staffpass")
        assert staff.password != "staffpass"

    def test_check_staff_password(self):
        staff = Staff("TestStaff", "staffpass")
        assert staff.check_password("staffpass")

class ShiftUnitTests(unittest.TestCase):

    def test_create_shift(self):
        startTime = datetime.strptime("2025/10/19 8:00", "%Y/%m/%d %H:%M")
        endTime = datetime.strptime("2025/10/19 16:00", "%Y/%m/%d %H:%M")
        shift = Shift(1, "TestStaff", 1, "Chimmy", startTime, endTime)

        actual = {
            "staffId": shift.staffId,
            "staffName": shift.staffName,
            "adminId": shift.adminId,
            "adminName": shift.adminName,
            "startTime": shift.startTime.strftime("%Y/%m/%d %H:%M"),
            "endTime": shift.endTime.strftime("%Y/%m/%d %H:%M")
        }

        expected = {
            "staffId": 1,
            "staffName": "TestStaff",
            "adminId": 1,
            "adminName": "Chimmy",
            "startTime": "2025/10/19 08:00",
            "endTime": "2025/10/19 16:00"
        }

        self.assertDictEqual(actual, expected)

    def test_shift_get_json(self):
        startTime = datetime.strptime("2025/10/19 8:00", "%Y/%m/%d %H:%M")
        endTime = datetime.strptime("2025/10/19 16:00", "%Y/%m/%d %H:%M")
        shift = Shift(1, "TestStaff", 1, "Chimmy", startTime, endTime)

        shift_json = shift.get_json()

        expected = {
            "id": None,
            "staffId" : 1,
            "staffName": "TestStaff",
            "adminId" : 1,
            "adminName": "Chimmy",
            "startTime" : "2025/10/19 08:00",
            "endTime" : "2025/10/19 16:00",
            "timedIn" : None,
            "timedOut" : None,
            "attendance" : None
        }

        self.assertDictEqual(shift_json, expected)

    def test_get_expected_hours(self):
        startTime = datetime.strptime("2025/10/19 8:00", "%Y/%m/%d %H:%M")
        endTime = datetime.strptime("2025/10/19 16:00", "%Y/%m/%d %H:%M")
        shift = Shift(1, "TestStaff", 1, "Chimmy", startTime, endTime)
        assert shift.getExpectedHours() == 8

    def test_get_worked_hours(self):
        startTime = datetime.strptime("2025/10/19 8:00", "%Y/%m/%d %H:%M")
        endTime = datetime.strptime("2025/10/19 16:00", "%Y/%m/%d %H:%M")
        shift = Shift(1, "TestStaff", 1, "Chimmy", startTime, endTime)

        shift.timedIn = datetime.strptime("2025/10/19 8:01", "%Y/%m/%d %H:%M")
        shift.timedOut = datetime.strptime("2025/10/19 15:58", "%Y/%m/%d %H:%M")

        assert shift.getWorkedHours() == 7.95

class ReportUnitTests(unittest.TestCase):

    def test_create_report(self):
        report = Report({"John": ["2025/10/19 08:00 - 2025/10/19 16:00"]}, {"John": {"absents": 0, "earlyTimeOuts": 0, "lateTimeIns": 0, "onTime": 1, "shiftIds": [1], "totalExpectedHours": 8, "totalShifts": 1, "totalWorkedHours": 7.95}})
        report.dateGenerated = datetime.strptime("2025/10/21 20:00", "%Y/%m/%d %H:%M")

        actual = {
            "roster": report.roster,
            "data": report.data
        }

        expected = {
            "roster": {
                "John": [
                "2025/10/19 08:00 - 2025/10/19 16:00"
                ]
            },
            "data": {
                "John": {
                "absents": 0,
                "earlyTimeOuts": 0,
                "lateTimeIns": 0,
                "onTime": 1,
                "shiftIds": [1],
                "totalExpectedHours": 8,
                "totalShifts": 1,
                "totalWorkedHours": 7.95 }
            }
        }

        self.assertDictEqual(actual, expected)

    def test_report_get_json(self):
        report = Report({"John": ["2025/10/19 08:00 - 2025/10/19 16:00"]}, {"John": {"absents": 0, "earlyTimeOuts": 0, "lateTimeIns": 0, "onTime": 1, "shiftIds": [1], "totalExpectedHours": 8, "totalShifts": 1, "totalWorkedHours": 7.95}})
        report.dateGenerated = datetime.strptime("2025/10/21 20:00", "%Y/%m/%d %H:%M")
        report_json = report.get_json()

        expected = {
            "id": None,
            "dateGenerated": "2025-10-21",
            "roster": {
                "John": [
                "2025/10/19 08:00 - 2025/10/19 16:00"
                ]
            },
            "data": {
                "John": {
                "absents": 0,
                "earlyTimeOuts": 0,
                "lateTimeIns": 0,
                "onTime": 1,
                "shiftIds": [1],
                "totalExpectedHours": 8,
                "totalShifts": 1,
                "totalWorkedHours": 7.95 }
            }
        }

        self.assertDictEqual(report_json, expected)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

