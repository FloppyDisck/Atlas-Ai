class CurrentReminders:
    #keep reminders in ram
    def __init__(self, dbPath = 'commandDB'):
        conn = sqlite3.connect(dbPath)
        update_list()

    def set_reminder(self):
        #TODO: this update adds a new reminder
        pass

    def edit_reminder(self):
        #TODO: This function updates the list values if anything happens
        pass

    def check_alarm(self):
        #TODO: if the time is less than the current time then set off alarm
        pass

    def update_list(self):
        #TODO: This function is going to update the list
        db = conn.cursor()
        db.execute("""
        SELECT * FROM remindersTbl r
        WHERE 
                r.status > 0""")
        self.reminders = []
        
        for reminder in db.fetchall():
            self.reminders.append(reminder)

#Set reminder at 5pm
#Set teminder in this 5Hrs
import pytz
from datetime import datetime, timezone, timedelta
def set_reminder_in(reminder, alarm):
    timeUTC = datetime.now(timezone.utc) # UTC time
    print(timeUTC)
    print(utc_dt.replace(minute=utc_dt.minute + 60))

    #sum number of time to UTC epoch
    pass
def set_reminder_at(reminder, alarm):
    #get local time and turn to epoch
    #replace alarm value with the current time value
    timeUTC = datetime.now(timezone.utc) #UTC time
    timeLocal = timeUTC.astimezone() #local time
    timeLocal_tuple = timeLocal.timetuple()

    for index in range(0, 6):
        if alarm[index] == None:
            alarm[index] = timeLocal_tuple[index]
        else:
            alarm[index] = alarm[index]
        
    timeAlarm = datetime(*alarm)
    print(timeAlarm.timestamp())

def set_reminder(reminder, alarm):
    #YYYY-MM-DD HH:MM:SS

    import pytz
    from datetime import datetime, timezone, timedelta
    localTime = datetime.now(pytz.utc)
    print(localTime)

    utc_dt = datetime.now(timezone.utc) # UTC time
    dt = utc_dt.astimezone() # local time
    print(str(utc_dt), dt)

    #Turn into time since epoch for finding time zone difference
    utc_dt = datetime.now(timezone.utc) # UTC time
    dt = utc_dt.astimezone().strftime('%s') # local time
    utc_dt = utc_dt.strftime('%s')
    print(utc_dt, dt)

    #Get time difference and change local to UTC
    timeDifference = int(utc_dt) - int(dt) #Get time difference
    print(timeDifference)

    turnUTC = int(dt) + int(timeDifference) #Turn local to UTC


    #Add time to UTC ex:remind me in x hours
    s = (timedelta(seconds=int(utc_dt)) + timedelta(hours=5)).total_seconds()
    print(s)

    value = datetime.fromtimestamp(s)
    print(value.strftime('%Y-%m-%d %H:%M:%S'))

    commands = [['h',7], ['d',1]]
    commandSum = timedelta(hours=0)
    for command in commands:
        if command[0] == 'h':    
            commandSum += timedelta(hours=command[1])
        if command[0] == 'd':
            commandSum += timedelta(days=command[1])
    
    print(commandSum)


    #when i say in 7 hours, turn that into seconds then sum it to the utc epoch time

    #Find specific time from local ex: Remind me tomorrow at 7pm
    


    #TODO: this update adds a new reminder, create steps for repeating and start/end
    pass

#input is [years, months, days, hours, minutes, seconds]
set_reminder_at("reminder", [None, None, None, 2, 30, None]) 