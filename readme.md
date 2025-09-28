# Rostering App

* (Admin) Schedule a staff member shifts for the week
* (Staff) View combined roster of all staff
* (Staff) Time in/Time out at the stat/end of shift
* (Admin) View shift report for the week

# CLI Commands

Initializes the database with staff, admins and shifts. Shifts are scheduled based on the current real world week.
```
flask init
```

## Staff Commands

Create a new staff user.
```
flask staff create {username} {password}
```

List all staff users.
```
flask staff list
```

View a staff user's details(including shifts) by selecting from a list.
```
flask staff view
```

Time a shift in/out, by selecting a staff user from a dropdown, then selecting one of their shifts this week.
```
flask staff time_shift {in|out}
```

View the combined staff roster for this week.
```
flask staff view_roster
```

## Admin Commands

Create a new admin user.
```
flask admin create {username} {password}
```

List all admin users.
```
flask admin list
```

View an admin user's details(including shifts they created) by selecting from a list.
```
flask admin view
```

View a staff user's details by selecting from a list.
```
flask admin view_staff
```

Schedule a shift for a staff user, by first selecting the admin who is scheduling the shift, then selecting the staff for whom to schedule the shift for, then entering a start time and end time for the shift in "YYYY/MM/DD HH:MM" format
```
flask admin schedule_shift
```

Reschedule a shift by first selecting a staff user, then selecting one of their shifts, then entering a new start time and end time.
```
flask admin reschedule_shift
```

Generate a shift report for the week
```
flask admin generate_report
```

View a report by selecting one from the list of generated reports.
```
flask admin view_report
```
