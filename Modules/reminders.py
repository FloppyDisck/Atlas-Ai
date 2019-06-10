import pytz
import sqlite3
from datetime import datetime, timezone, timedelta
from operator import itemgetter

class CurrentReminders:
    def __init__(self, dbPath = 'Modules/DataBases/remindersDB'):
        """
        Create a reminder monitor object.

        This will store all upcoming reminders and remind when
        theyre due.

        Args:
            dbPath: Where to get the reminders from.
        """
        self.conn = sqlite3.connect(dbPath)
        self.update_list()

    def get_time_in(self, alarm, timeUTC=None):
        """
        Add the requested time on top of the UTC.

        This function takes an array and sums those
        values to the current time, it will automatically
        fix any conflicts with time and return the correct time.

        Args:
            alarm: Array list that will be added to time.
                [years, months, days, hours, minutes, seconds]
            timeUTC: Get time to be summed

        Returns:
            The epoch time with the alarm added.
        """
        if timeUTC == None:
            timeUTC=datetime.now(timezone.utc)
        timeUTC_tuple = timeUTC.timetuple()
        for index in range(0, 6):
            if alarm[index] == None:
                alarm[index] = timeUTC_tuple[index] #copy original value
            else:
                alarm[index] += timeUTC_tuple[index] #sum the new val to the original

        correctionList = [12, None, 24, 59, 59] #number thresholds for each value

        import calendar
        #Iterate through the array backwards, from seconds to years
        for index in range(5, 1, -1):
            #If true the next value is the day value
            #The problem here is that days vary by month
            if correctionList[index - 1] == None: #ATM its index=2
                #Loop untill nothing is left to calculate
                while True:
                    #years are equal to months / 12
                    alarm[index-2] += int(alarm[index-1] / correctionList[index-2])
                    #months are equal to months MOD 12
                    alarm[index-1] = int(alarm[index-1] % correctionList[index-2])

                    #the max amound of days in that year,month
                    dayLimit = calendar.monthrange(alarm[index-2], alarm[index-1])[1]
                    if alarm[index] > dayLimit:
                        #when the total days is greater that max days in month
                        #substract max days and sum one to months
                        alarm[index] -= dayLimit
                        alarm[index - 1] += 1
                    else:
                        #once total days is smaller than the max days in month
                        #   break out of loop
                        break
            else:
                #next value is equal to the dividion of current value by its limit
                alarm[index-1] += int(alarm[index] / correctionList[index-1])
                #current value is equal to current value MOD its limit
                alarm[index] = int(alarm[index] % correctionList[index-1])
        timeAlarm = datetime(*alarm)
        return int(timeAlarm.replace(tzinfo=timezone.utc).timestamp())

    def get_time_at(self, alarm, timeUTC=None):
        """
        Replace current time with requested values.

        Will replace parameters where the request is not Null

        Args:
            alarm: Array list that will be added to time.
                [years, months, days, hours, minutes, seconds]
            timeUTC: Get time to be summed

        Returns:
            The epoch time with the alarm added.
        """
        if timeUTC == None:
            timeUTC=datetime.now(timezone.utc)
        timeLocal = timeUTC.astimezone() #local time
        timeLocal_tuple = timeLocal.timetuple()

        #If the alarm index is None then replace with current time
        for index in range(0, 6):
            if alarm[index] == None:
                alarm[index] = timeLocal_tuple[index]
            
        timeAlarm = datetime(*alarm)
        return int(timeAlarm.timestamp())

    def set_reminder(self, reminder, alarm, exactTime, repeatFrequency = None):
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

        if exactTime == True:
            alarm_epoch = self.get_time_at(alarm)
        else:
            alarm_epoch = self.get_time_in(alarm)
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
        newAlarm = [0, 0, 0, 0, 0, 0]
        alarmHeaders = ['Y', 'M', 'D', 'h', 'm', 's'] #used to find newAlarm index
        repetition_str = ""
        for value in repetition:
            if value != "":
                #Set the header Char
                valueHeader = value[:1]

                if valueHeader in alarmHeaders:
                    newAlarm[alarmHeaders.index(valueHeader)] += int(value[1:])

                #Remove a repetition since this is finite
                if valueHeader == 'T':
                    times = int(value[1:])
                    if times == 0:
                        return None
                    value = 'T' + str(times-1)

                if valueHeader == 'W':
                    #Add that many days
                    newAlarm[alarmHeaders.index('D')] += (int(value[1:]) * 7)

                if valueHeader == 'w':
                    #Assuming in this string weeks start with 1
                    weekDay_now = datetime.now(timezone.utc).weekday() + 1
                    weekDays = value[1:].split('-')

                    #Calculate nearest weekday
                    for index in range(0, len(weekDays)):
                        if weekDay_now > weekDays[index]:
                            weekDay_near = index - 1
                        weekDay_near = weekDays[index]
                    if weekDay_near < 0:
                        weekDay_near = 0

                    newAlarm[alarmHeaders.index('D')] += abs(weekDay_now - weekDays[weekDay_near])
 
                repetition_str += '/' + value

        newReminder = self.set_reminder(reminder_old[0], newAlarm, False, repeatFrequency=repetition_str)
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
        timeUTC_epoch = datetime.now(timezone.utc).timestamp()
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
    print(reminder.set_reminder("2 minute reminder", [0, 0, 0, 0, 2, 0], False))
    print(reminder.set_reminder("4 minute reminder", [0, 0, 0, 0, 4, 0], False))
    print(reminder.set_reminder("8 minute reminder", [0, 0, 0, 0, 8, 0], False))
    print(reminder.set_reminder("At 2:35PM", [None, None, None, 14, 35, 0], True))
    print(reminder.set_reminder("Repeat reminder", [0, 0, 0, 0, 2, 0], False, "m2/T2"))
    print(reminder.reminders)

    UTCSec = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    curTime = datetime.now()
    print(curTime, UTCSec, "Start Time") #This has proven to be the accurate time

    while True:
        reminders = reminder.check_alarm()
        if reminders != []:
            UTCSec = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
            curTime = datetime.now()
            print(curTime, UTCSec, reminders)