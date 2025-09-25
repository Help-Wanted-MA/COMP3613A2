import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Staff, Admin, Shift, Report
from App.main import create_app
from App.controllers import ( 
    create_user, get_all_users_json, get_all_users, initialize,
    create_admin_user, scheduleShift, get_all_admins, get_all_admins_json, list_admins, get_admin,
    create_staff_user, timeShift, get_all_staff, get_all_staff_json, list_staff, get_staff,
    get_shift_info, is_shift_timed_in, pretty_print_shift_json,
    generate_roster, generate_report_data, generate_report, get_report, get_all_reports, pretty_print_report_json, list_reports)


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
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Staff Commands
'''
def view_staff():
    print(list_staff())
    staffId = click.prompt("Enter a staff id: ", type=int)
    
    staff = get_staff(staffId)
    if not staff:
        print("Could not find staff user for given id")
    else:
        data = staff.get_json()
        shifts = data["shifts"]
        str = ''
        for shift in shifts:
            str += pretty_print_shift_json(shift)
            
        print(f'''
              StaffID: {data["id"]}
              Name: {data["name"]}
              shifts: {str}''')
        
staff_cli = AppGroup('staff', help='Staff object commands') 

@staff_cli.command("list", help="Lists all staff users")
def list_staff_command():
    print(list_staff())
   
@staff_cli.command("view", help="View a staff user's details from a list of users")
def view_staff_command():
    view_staff()
     
@staff_cli.command("view_roster", help="View the combined staff roster for this week")
def view_roster_command():
    roster = generate_roster()
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
    staff = create_staff_user(name, password)
    if not staff:
        print("Error creating staff user")
    else:
        print(f'Staff user {staff.name} successfully created!')
        
        
@staff_cli.command("time_shift", help="Time in/out of a shift")
@click.argument("type", type=click.Choice(["in", "out"], case_sensitive=False))
def time_shift_command(type):
    view_staff()
    
    shiftId = click.prompt(f'Enter a shift ID to time {type}: ', type=int)
    string = timeShift(shiftId, type)
    print(string)

app.cli.add_command(staff_cli) # add the group to the cli



'''
Admin Commands
'''
def view_admin():
    print(list_admins())
    adminId = click.prompt("Enter an admin number: ", type=int)
    
    admin = get_admin(adminId)
    if not admin:
        print("Could not find admin user for given id")
    else:
        data = admin.get_json()
        shifts = data["createdShifts"]
        str = ''
        for shift in shifts:
            str += pretty_print_shift_json(shift)
            
        print(f'''
              AdminID: {data["id"]}
              Name: {data["name"]}
              CreatedShifts: {str}''')
        
admin_cli = AppGroup('admin', help='Admin object commands') 

@admin_cli.command("list", help="Lists all admin users")
def list_admin_command():
    print(list_admins())
    
@admin_cli.command("view", help="View an admin user's details from a list of admins")
def list_admin_command():
    view_admin()
        
@admin_cli.command("create", help="Creates an admin user")
@click.argument('name', default="john")
@click.argument('password', default="johnpass")
def create_admin_command(name, password):
    admin = create_admin_user(name, password)
    if not admin:
        print("Error creating admin user")
    else:
        print(f'Admin user {admin.name} successfully created!')

@admin_cli.command("schedule_shift", help='Schedules a shift for a staff user.')
def schedule_shift_command():
    print("ADMINS:")
    print(list_admins())
    adminId = click.prompt("Enter the ID of the admin who is creating this shift: ", type=int)
    
    print("STAFF")
    print(list_staff())
    staffId = click.prompt("Enter the ID of the staff to create the shift for: ", type=int)
    
    startTime = click.prompt("Enter the start time of the shift(YYYY/MM/DD HH:MM): ")
    endTime = click.prompt("Enter the end time of the shift(YYYY/MM/DD HH:MM): ")
    shift = scheduleShift(staffId, adminId, startTime, endTime)
    if not shift:
        print("Error scheduling shift")
        return
    else:
        print(f'Shift scheduled! Details:\n{pretty_print_shift_json(shift.get_json())}')

@admin_cli.command("generate_report", help="Generates a report")
def generate_report_command():
    report = generate_report()
    if not report:
        print("Error generating report")
    else:
        print(f'Report generated!\n\n {pretty_print_report_json(report.get_json())}')
    
@admin_cli.command("view_report", help="View a report from a list of reports")
def view_report_command():
    print("------------------REPORTS------------------")
    reports = list_reports()
    print(reports)
    reportId = click.prompt("Enter a report ID: ", type=int)
    
    report = get_report(reportId)
    if not report:
        print("Could not find report")
        return
    else:
        print(f'{pretty_print_report_json(report.get_json())}')


app.cli.add_command(admin_cli) # add the group to the cli



'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)