import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Staff, Admin, Shift, Report
from App.main import create_app
from App.controllers import ( 
    create_user, get_all_users_json, get_all_users, initialize,
    create_admin_user, scheduleShift, get_all_admins, get_all_admins_json, list_admins, get_admin,
    create_staff_user, timeShift, get_all_staff, get_all_staff_json, list_staff, get_staff,
    get_shift_info, is_shift_timed_in,
    generate_roster, generate_report_data, create_report, get_report, get_all_reports)


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
staff_cli = AppGroup('staff', help='Staff object commands') 

@staff_cli.command("list", help="Lists all staff users")
def list_staff_command():
    print(list_staff())
   
@staff_cli.command("view", help="View a staff user's details")
@click.argument('staff_id', default=1)
def list_staff_command(staff_id):
    staff = get_staff(staff_id)
    if not staff:
        print("Could not find staff user for given id")
    else:
        print(staff.get_json())
     
@staff_cli.command("create", help="Creates a staff user")
@click.argument('name', default="tom")
@click.argument('password', default="tompass")
def create_staff_command(name, password):
    staff = create_staff_user(name, password)
    if not staff:
        print("Error creating staff user")
    else:
        print(f'Staff user {staff.name} successfully created!')
        
        
@staff_cli.command("timeShift", help="Time in/out of a shift")
@click.argument("type", type=click.Choice(["in", "out"], case_sensitive=False))
@click.argument("shift_id", default=1)
def time_shift_command(shift_id, type):
    string = timeShift(shift_id, type)
    print(string)

app.cli.add_command(staff_cli) # add the group to the cli



'''
Test Commands
'''
admin_cli = AppGroup('admin', help='Admin object commands') 

@admin_cli.command("list", help="Lists all admin users")
def list_admin_command():
    print(list_admins())
    
@staff_cli.command("view", help="View an admin user's details")
@click.argument('admin_id', default=1)
def list_staff_command(admin_id):
    admin = get_staff(admin_id)
    if not admin:
        print("Could not find admin user for given id")
    else:
        print(admin.get_json())
        
@admin_cli.command("create", help="Creates an admin user")
@click.argument('name', default="john")
@click.argument('password', default="johnpass")
def create_admin_command(name, password):
    admin = create_admin_user(name, password)
    if not admin:
        print("Error creating admin user")
    else:
        print(f'Staff user {admin.name} successfully created!')

@admin_cli.command("scheduleShift", help='Schedules a shift for a staff user. Time arguments should be formated as "YYYY-MM-DD HH:MM"')
@click.argument('staff_id', default=1)
@click.argument('admin_id', default=1)
@click.argument('start_time', default="2025-9-10 13:00")
@click.argument('end_time', default="2025-9-10 15:00")
def schedule_shift_command(staff_id, admin_id, start_time, end_time):
    shift = scheduleShift(staff_id, admin_id, start_time, end_time)
    if not shift:
        print("Error scheduling shift")
        return
    else:
        print(f'Shift scheduled! Details:\n{shift.get_json()}')

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