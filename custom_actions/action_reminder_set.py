import pytz
import sqlite3
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import *
from operator import itemgetter

class CurrentReminders:
    def __init__(self, dbPath = 'custom_actions/storage/remindersDB'):
        """
        Create a reminder monitor object.

        This will store all upcoming reminders and remind when
        theyre due.

        Args:
            dbPath: Where to get the reminders from.
        """
        self.conn = sqlite3.connect(dbPath)
        self.update_list()

    def set_reminder(self, reminder, alarm_epoch, repeatFrequency = None):
        """
        Create a reminder and add it to the reminder DB

        Args:
            reminder: The reminder description.
            alarm: Array list that will be added to time.
            exactTime: A boolean that describes the alarm type.
            repeatFrequency: A string that describes the repetition type.
                Repeat every:
                s[second]/m[minutes]/h[hour]/D[day]/M[month]/Y[year]/T[times]/w[WeekDay]/W[Weeks]

        Returns:
            Returns info that confirms the saved data.
        """

        if repeatFrequency == None:
            reminderStatus = 1
        else:
            #Run reminder_concurrency after alarm is done
            reminderStatus = 2

        #Add the reminder to the ram
        commandSet = [reminder, alarm_epoch, reminderStatus, repeatFrequency]
        self.reminders.append(commandSet)

        #Sort by the smallest epoch
        self.reminders.sort(key = itemgetter(1))

        db = self.conn.cursor()
        db.execute('INSERT INTO reminderstbl (reminderStr, alarm, status, concurrency) VALUES (?, ?, ?, ?)', commandSet)
        self.conn.commit()

        #return string confirmation of "set blah blah at TIMEHERE"
        return commandSet

    def delete_reminder(self, reminder):
        try:
            db = self.conn.cursor()
            db.execute('DELETE FROM reminderstbl WHERE reminderStr = ?', (reminder))
            self.conn.commit()
            self.update_list()
            return f"Deleted {reminder} from reminders"
        except:
            return f"Could not find {reminder} as a reminder."

    def list_reminder(self, alarm_epoch):
        #Get all reminders that match that day
        epoch_day = int(alarm_epoch / 86400) * 86400 #This will cleanup epoch

        #check that dates between epoch_today and epoch_tomorrow
        db = self.conn.cursor()
        db.execute("""
        SELECT reminderStr, alarm, status FROM remindersTbl r
        WHERE r.status > 0 AND r.alarm >= ? AND r.alarm < ?""", (epoch_day, epoch_day + 86400))
        self.conn.commit()
        #If status is greater than 0 then it is still available
        reminderList = []
        
        for reminder in db.fetchall():
            reminderList.append(reminder)

        #sort by epoch
        reminderList.sort(key = itemgetter(1))

        #if a day in the close week say so
        #You have reminders tomorrow; you have reminders this sunday
        dayDate = datetime.fromtimestamp(epoch_day).strftime('%m %d') 
        if len(reminderList) == 0:
            returnString = f"You have no reminders for {dayDate}"
        elif len(reminderList) == 1:
            returnString = f"You only have to {reminderList[0][0]} at {datetime.fromtimestamp(reminderList[0][1]).strftime('%H %M')}"
        elif len(reminderList) == 2:
            returnString = f"You have to {reminderList[0][0]} at {datetime.fromtimestamp(reminderList[0][1]).strftime('%H %M')} and then {reminderList[1][0]} at {datetime.fromtimestamp(reminderList[1][1]).strftime('%H %M')}"
        elif len(reminderList) > 2:
            import random
            flavorStrings = ["then ", "later ", "after ", "and ", "also "]
            returnString = f"You have to {reminderList[0][0]} at {datetime.fromtimestamp(reminderList[0][1]).strftime('%H %M')} "
            for index in range(1, len(reminderList) - 1):
                randIndex = random.randint(0, len(flavorStrings) - 1)
                returnString = returnString + flavorStrings[randIndex] + f"{reminderList[index][0]} at {datetime.fromtimestamp(reminderList[index][1]).strftime('%H %M')} "
            returnString = returnString + f"finally remember to {reminderList[-1][0]} at {datetime.fromtimestamp(reminderList[-1][1]).strftime('%H %M')}"
        return returnString
    
    def reminder_concurrency(self, reminder_old):
        """
        Make a new reminder with a concurrent reminder.

        Args:
            reminder_old: The reminder to be updated.

        Returns:
            The updated value is returned or None when there is no next reminder.
        """
        #second, minute, hour, Day, Month, Year, Times, Weeks, week (week day 1-7) (days divided by -)
        repetition = reminder_old[3].split('/')
        newAlarm = datetime.fromtimestamp(reminder_old[1])

        repetition_str = ""
        for value in repetition:
            if value != "":
                #Set the header Char
                valueHeader = value[:1]

                #Relative delta handles leapyears and month disbalances
                if valueHeader == 'Y':
                    newAlarm += relativedelta(years=int(value[1:]))
                if valueHeader == 'M':
                    newAlarm += relativedelta(months=int(value[1:]))
                if valueHeader == 'D':
                    newAlarm += relativedelta(days=int(value[1:]))
                if valueHeader == 'h':
                    newAlarm += relativedelta(hours=int(value[1:]))
                if valueHeader == 'm':
                    newAlarm += relativedelta(minutes=int(value[1:]))
                if valueHeader == 's':
                    newAlarm += relativedelta(seconds=int(value[1:]))
                if valueHeader == 's':
                    newAlarm += relativedelta(weeks=int(value[1:]))

                #Remove a repetition since this is finite
                if valueHeader == 'T':
                    times = int(value[1:])
                    if times == 0:
                        return None
                    value = 'T' + str(times-1)

                if valueHeader == 'w':
                    #Assuming in this string weeks start with 1
                    nextDay = 0
                    weekDay_now = datetime.now(timezone.utc).weekday() + 1
                    weekDays = sorted(value[1:].split('-'))

                    #Check which weekDay is the next one
                    for weekDay in weekDays:
                        if weekDay_now <= weekDay:
                            nextDay = weekDay
                    if nextDay == 0:
                        nextDay = weekDays[0]

                    #Calculate how many days to skip
                    if weekDay_now == nextDay:
                        newAlarm += relativedelta(days=7)
                    elif weekDay_now > nextDay:
                        newAlarm += relativedelta(days=(7 - weekDay_now + nextDay))
                    else:
                        newAlarm += relativedelta(days=(nextDay - weekDay_now))
 
                repetition_str += '/' + value

        newReminder = self.set_reminder(reminder_old[0], newAlarm, repeatFrequency=repetition_str)
        return newReminder

    def check_alarm(self):
        """
        Go through self.reminders and check what alarm is ready.

        Args:
            self.reminders: List of all the reminders in a threshold.

        Returns:
            Return list of alarms that are due.
        """
        threshold = 0 #add second threshold for current time
        currentTime_epoch = datetime.now(timezone.utc).timestamp() + threshold
        dueAlarm = []
        for reminder in self.reminders:
            #Since list is sorted break when number is greater
            if currentTime_epoch < reminder[1]:
                break
            #Add reminder to dueAlarm and remove from reminders
            dueAlarm.append(reminder)
            if reminder[2] == 2: #Standard
                self.reminder_concurrency(reminder)
 
            db = self.conn.cursor()
            db.execute('UPDATE remindersTbl SET status = ? WHERE reminderStr = ? AND alarm = ?', (0, reminder[0], reminder[1]))
            self.reminders.remove(reminder)
            self.conn.commit()

        #TODO: create a string for each value that the ai can read
        return dueAlarm

    def update_list(self):
        """
        Update the self.reminders from the database.

        Returns:
            self.reminders witt the populated reminders.
        """
        #timeUTC_epoch = datetime.now(timezone.utc).timestamp()
        db = self.conn.cursor()
        db.execute("""
        SELECT reminderStr, alarm, status, concurrency FROM remindersTbl r
        WHERE r.status > 0""")
        self.conn.commit()
        #If status is greater than 0 then it is still available
        self.reminders = []
        
        for reminder in db.fetchall():
            self.reminders.append(reminder)

        #sort by epoch
        self.reminders.sort(key = itemgetter(1))

if __name__ == "__main__":
    reminder = CurrentReminders()
    #TODO: update concurrency into a dictionary system
    print(reminder.set_reminder("2 minute reminder", 1565103208))
    print(reminder.set_reminder("4 minute reminder", 1565103328))
    print(reminder.set_reminder("8 minute reminder", 1565103568))
    print(reminder.set_reminder("Repeat reminder", 1565103568, "m2/T2"))
    print(reminder.reminders)
    print(reminder.list_reminder(1565103568))

    UTCSec = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    curTime = datetime.now()
    print(curTime, UTCSec, "Start Time") #This has proven to be the accurate time

    while True:
        reminders = reminder.check_alarm()
        if reminders != []:
            UTCSec = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
            curTime = datetime.now()
            print(curTime, UTCSec, reminders)