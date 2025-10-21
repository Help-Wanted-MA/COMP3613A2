import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from flask_jwt_extended import decode_token

from App.database import db, get_migrate
from App.models import User, Staff, Admin, Shift, Report
from App.main import create_app
from App.controllers import ( 
    initialize, create_admin_user, schedule_shift, get_admin, delete_admin, login, list_admins_json,
    delete_staff, delete_shift, generate_report, get_report, list_reports_json, delete_report,
    create_staff_user, time_shift, get_staff, generate_roster, get_all_staff, get_all_admins, get_shift, get_staff_shifts
)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
'''
Helper Commands
'''
def pretty_print_report_json(report):
    str = f'''
        ReportID: {report["id"]}
        Date Generated: {report["dateGenerated"]}
    '''
    
    for staffName, data in report["data"].items():
        str += f'''
        -----------------------------------------
            Name: {staffName}
            Total Shifts: {data["totalShifts"]},
            Total Expected Hours: {data["totalExpectedHours"]},
            Total Worked Hours: {data["totalWorkedHours"]:.2f},
            On Time: {data["onTime"]},
            Late Time Ins: {data["lateTimeIns"]},
            Early Time Outs: {data["earlyTimeOuts"]},
            Absent: {data["absents"]},
            shiftIds: {data["shiftIds"]}
        -----------------------------------------
        '''
    return str

def pretty_print_shift_json(shift):
    str = f'''
        ShiftID: {shift["id"]}
        Start time: {shift["startTime"]}
        End time: {shift["endTime"]}
        Timed in: {shift["timedIn"]}
        Timed out: {shift["timedOut"]}
        Attendance: {shift["attendance"]}
    '''
    return str




'''
Staff Commands
'''
def view_staff():
    allStaff = get_all_staff()
    for staff in allStaff:
        print(f"Staff ID: {staff.id} | Staff Name: {staff.name}")
        
    staffId = click.prompt("Enter a staff id: ", type=int)
    
    try:
        staff = get_staff(staffId)
    except Exception as e:
        print(e)
        return

    data = staff.get_json()
    shifts = data["shifts"]
    str = ''
    for shift in shifts:
        str += pretty_print_shift_json(shift)
        
    print(f'''
          StaffID: {data["id"]}
          Name: {data["name"]}
          shifts: {str}''')
    return staffId
        
staff_cli = AppGroup('staff', help='Staff object commands') 

@staff_cli.command("list", help="Lists all staff users")
def list_staff_command():
    allStaff = get_all_staff()
    for staff in allStaff:
        print(f"Staff ID: {staff.id} | Staff Name: {staff.name}")
   
@staff_cli.command("view", help="View a staff user's details from a list of users")
def view_staff_command():
    view_staff()
     
@staff_cli.command("view_roster", help="View the combined staff roster for this week")
@click.option("--date", "-d", default=None, help="Reference date for the week (format: YYYY/MM/DD)")
def view_roster_command(date):
    roster = generate_roster(date)
    str = 'Shifts for each staff member this week:\n'
    for staff in roster:
        str += f'\n{staff}:\n'
        for shift in roster[staff]:
            str += f'{shift}\n'
            
    print(str)
    
@staff_cli.command("create", help="Creates a staff user")
@click.argument('name', default="tom")
@click.argument('password', default="tompass")
def create_staff_command(name, password):
    try:
        staff = create_staff_user(name, password)
        print(f'Staff user {staff.name} successfully created!')
    except Exception as e:
        print(e)
           
@staff_cli.command("time_shift", help="Time in/out of a shift")
@click.argument("type", type=click.Choice(["in", "out"], case_sensitive=False))
def time_shift_command(type):
    view_staff()
    
    shiftId = click.prompt(f'Enter a shift ID to time {type}: ', type=int)
    try:
        shift = time_shift(shiftId, type)
        if type == "in":
            print(f"Time {type} shift {shift.id} at {shift.timedIn.isoformat()}")
        elif type == "out":
            print(f"Time {type} shift {shift.id} at {shift.timedOut.isoformat()}")
    except Exception as e:
        print(e)


app.cli.add_command(staff_cli) # add the group to the cli



'''
Admin Commands
'''
def view_admin():
    allAdmins = get_all_admins()
    for admin in allAdmins:
        print (f"Admin ID: {admin.id} | Admin name: {admin.name}")
        
    adminId = click.prompt("Enter an admin number: ", type=int)
    
    try:
        admin = get_admin(adminId)
        data = admin.get_json()
        shifts = data["createdShifts"]
        str = ''
        for shift in shifts:
            str += pretty_print_shift_json(shift)
            
        print(f'''
              AdminID: {data["id"]}
              Name: {data["name"]}
              CreatedShifts: {str}''')
    except Exception as e:
        print(e)
        
        
admin_cli = AppGroup('admin', help='Admin object commands') 

@admin_cli.command("list", help="Lists all admin users")
def list_admin_command():
    allAdmins = get_all_admins()
    for admin in allAdmins:
        print (f"Admin ID: {admin.id} | Admin name: {admin.name}")
    
@admin_cli.command("view", help="View an admin user's details from a list of admins")
def list_admin_command():
    view_admin()
        
@admin_cli.command("create", help="Creates an admin user")
@click.argument('name', default="john")
@click.argument('password', default="johnpass")
def create_admin_command(name, password):
    try:
        admin = create_admin_user(name, password)
        print(f'Admin user {admin.name} successfully created!')
    except Exception as e:
        print(e)
        

@admin_cli.command("schedule_shift", help='Schedules a shift for a staff user.')
def schedule_shift_command():
    print("ADMINS:")
    allAdmins = get_all_admins()
    for admin in allAdmins:
        print (f"Admin ID: {admin.id} | Admin name: {admin.name}")
    adminId = click.prompt("Enter the ID of the admin who is creating this shift: ", type=int)
    
    print("STAFF:")
    allStaff = get_all_staff()
    for staff in allStaff:
        print(f"Staff ID: {staff.id} | Staff Name: {staff.name}")
    staffId = click.prompt("Enter the ID of the staff to create the shift for: ", type=int)
    
    startTime = click.prompt("Enter the start time of the shift(YYYY/MM/DD HH:MM): ")
    endTime = click.prompt("Enter the end time of the shift(YYYY/MM/DD HH:MM): ")
    try:
        shift = schedule_shift(staffId, adminId, startTime, endTime)
        print(f'Shift scheduled! Details:\n{pretty_print_shift_json(shift.get_json())}')
    except Exception as e:
        print(e)
        

@admin_cli.command("generate_report", help="Generates a report")
def generate_report_command():
    try:
        report = generate_report()
        print(f'Report generated!\n\n {pretty_print_report_json(report.get_json())}')
    except Exception as e:
        print(e)
        
    
@admin_cli.command("view_report", help="View a report from a list of reports")
def view_report_command():
    print("------------------REPORTS------------------")
    reports = list_reports_json()
    for report in reports:
        print(f"Report ID: {report['reportId']} | Generated on: {report['dateGenerated']}")
    reportId = click.prompt("Enter a report ID: ", type=int)
    
    try:
        report = get_report(reportId)
        print(report.get_json())
        print(f'{pretty_print_report_json(report.get_json())}')
    except Exception as e:
        print(e)
        

@admin_cli.command("view_staff", help="View a staff user's details from a list of users")
def view_staff_admin_command():
    view_staff()
    

app.cli.add_command(admin_cli) # add the group to the cli



'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("run", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AdminUnitTests or StaffUnitTests or ShiftUnitTests or ReportUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "AdminIntegrationTests or StaffIntegrationTests or ShiftIntegrationTests or ReportIntegrationTests or DeleteIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)