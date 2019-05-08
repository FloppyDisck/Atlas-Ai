import pytz
import sqlite3
from datetime import datetime, timezone, timedelta

class CurrentReminders:
    #keep reminders in ram
    def __init__(self, dbPath = 'Processes/DataBases/remindersDB'):
        self.conn = sqlite3.connect(dbPath)
        self.update_list()

    def get_time_in(alarm):
        timeUTC = datetime.now(timezone.utc) # UTC time
        timeUTC_tuple = timeUTC.timetuple()

        for index in range(0, 6):
            if alarm[index] == None:
                alarm[index] = timeUTC_tuple[index] #copy original value
            else:
                alarm[index] += timeUTC_tuple[index] #sum the new val to the original
        
        correctionList = [12, None, 24, 59, 59] #number thresholds for each value

        import calendar
        for index in range(5, 1, -1):
            if correctionList[index - 1] == None:
                while True:
                    alarm[index-2] += int(alarm[index-1] / correctionList[index-2])
                    alarm[index-1] = int(alarm[index-1] % correctionList[index-2])

                    dayLimit = calendar.monthrange(alarm[index-2], alarm[index-1])[1]
                    if alarm[index] > dayLimit:
                        alarm[index] -= dayLimit
                        alarm[index - 1] += 1
                    else:
                        break
            else:
                alarm[index-1] += int(alarm[index] / correctionList[index-1])
                alarm[index] = int(alarm[index] % correctionList[index-1])
            print(alarm)

        timeAlarm = datetime(*alarm)

        return int(timeAlarm.timestamp())

    def get_time_at(alarm):
        timeUTC = datetime.now(timezone.utc) #UTC time
        timeLocal = timeUTC.astimezone() #local time
        timeLocal_tuple = timeLocal.timetuple()

        for index in range(0, 6):
            if alarm[index] == None:
                alarm[index] = timeLocal_tuple[index]
            
        timeAlarm = datetime(*alarm)
        #return timeAlarm.timestamp()
        return int(timeAlarm.timestamp())

    def set_reminder(self, reminder, alarm, exactTime):
        '''Reminder is the string being saved
           Alarm is the date either in adition or replacement
           exactTime is a boolean that decides one of the two above.'''
        #TODO: this update adds a new reminder
        #TODO: when the time input is placed it uses the get_time function

        if exactTime == True:
            alarm_epoch = get_time_at(alarm)
        else:
            alarm_epoch = get_time_in(alarm) 

    def edit_reminder(self):
        #TODO: This function updates the list values if anything happens
        pass

    def check_alarm(self):
        #TODO: if the time is less than the current time then set off alarm
        pass

    def update_list(self):
        #TODO: This function is going to update the list
        timeUTC_epoch = datetime.now(timezone.utc).timestamp()

        db = self.conn.cursor()
        db.execute("""
        SELECT * FROM remindersTbl r
        WHERE
                r.alarm >= {} AND
                r.status > 0""".format(timeUTC_epoch))
        #If status is greater than 0 then it is still available
        self.reminders = []
        
        for reminder in db.fetchall():
            self.reminders.append(reminder)

#input is [years, months, days, hours, minutes, seconds]
#get_time_in([None, 20, 40, 30, 70, None]) 

if __name__ == "__main__":
    reminder = CurrentReminders()