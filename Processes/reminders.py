import pytz
import sqlite3
from datetime import datetime, timezone, timedelta

class CurrentReminders:
    def __init__(self, dbPath = 'Processes/DataBases/remindersDB'):
        self.conn = sqlite3.connect(dbPath)
        self.update_list()

    def get_time_in(self, alarm):
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

        timeAlarm = datetime(*alarm)

        return int(timeAlarm.timestamp())

    def get_time_at(self, alarm):
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

        if exactTime == True:
            alarm_epoch = self.get_time_at(alarm)
        else:
            alarm_epoch = self.get_time_in(alarm)

        reminderStatus = 1
        commandSet = [reminder, alarm_epoch, reminderStatus]
        self.reminders.append(commandSet)
        self.reminders.sort(key = lambda x: x[2]) #sort by the epoch

        db = self.conn.cursor()
        db.execute('INSERT INTO reminderstbl (reminderStr, alarm, status) VALUES (?, ?, ?)', commandSet)
        self.conn.commit()

        #return string confirmation of "set blah blah at TIMEHERE"

    def edit_reminder(self):
        #TODO: This function updates the list values if anything happens
        pass

    def check_alarm(self):
        threshold = 60 #add second threshold for current time
        currentTime_epoch = datetime.now(timezone.utc).timestamp() + threshold
        
        dueAlarm = []
        for reminder in self.reminders:
            if currentTime_epoch < reminder[2]:
                break
            #If the alarm time is less than current time
            #then add to dueAlarm and remove from reminders
            dueAlarm.append(reminder)
            if reminder[3] == 1: #Standard
                self.reminders.remove(reminder)

        #TODO: create a string for each value that the ai can read
        return dueAlarm

    def update_list(self):
        #TODO: Add a new column where i can create a routine
        #Example: Remind me in 2 hours for the next 5 days every monday
        timeUTC_epoch = datetime.now(timezone.utc).timestamp()
        db = self.conn.cursor()
        db.execute("""
        SELECT reminderStr, alarm, status FROM remindersTbl r
        WHERE
                r.alarm >= {} AND
                r.status > 0""".format(timeUTC_epoch))
        #If status is greater than 0 then it is still available
        self.reminders = []
        
        for reminder in db.fetchall():
            self.reminders.append(reminder)

        self.reminders.sort(key = lambda x: x[2]) #sort by the epoch

if __name__ == "__main__":
    reminder = CurrentReminders()
    reminder.set_reminder("Testing Reminder", [None, 20, 40, 30, 70, None], False)