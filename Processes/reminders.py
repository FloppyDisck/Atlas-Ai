import pytz
import sqlite3
from datetime import datetime, timezone, timedelta

class CurrentReminders:
    def __init__(self, dbPath = 'Processes/DataBases/remindersDB'):
        """
        Create a reminder monitor object.

        This will store all upcoming reminders and remind when
        theyre due.

        Args:
            dbPath: Where to get the reminders from.
        """
        self.conn = sqlite3.connect(dbPath)
        self.update_list()

    def get_time_in(self, alarm, timeUTC=datetime.now(timezone.utc)):
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

        return int(timeAlarm.timestamp())

    def get_time_at(self, alarm, timeUTC=datetime.now(timezone.utc)):
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
        timeLocal = timeUTC.astimezone() #local time
        timeLocal_tuple = timeLocal.timetuple()

        #If the alarm index is None then replace with current time
        for index in range(0, 6):
            if alarm[index] == None:
                alarm[index] = timeLocal_tuple[index]
            
        timeAlarm = datetime(*alarm)
        #return timeAlarm.timestamp()
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
        #TODO:If the alarm_epoch < x hour limit then add
        commandSet = [reminder, alarm_epoch, reminderStatus, repeatFrequency]
        self.reminders.append(commandSet)

        #Sort by the smallest epoch
        self.reminders.sort(key = lambda x: x[2])

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
        #second, minute, hour, Day, Month, Year, Times, Week, week (week day 1-7) (days divided by -)
        repetition = reminder_old[3].split('/')
        newAlarm = [0, 0, 0, 0, 0, 0]
        alarmHeaders = ['s', 'm', 'h', 'D', 'M', 'Y'] #used to find newAlarm index
        repetition_str = ""
        for value in repetition:
            #Set the header Char
            valueHeader = value[:1]
            if valueHeader in alarmHeaders:
                newAlarm[alarmHeaders.index(valueHeader)] += int(value[1:])
            #Remove a repetition since this is finite
            if valueHeader == 'T':
                times = int(value[1:]) - 1
                if times == 0:
                    return None
                value = 'T' + times
            if valueHeader == 'W':
                newAlarm[alarmHeaders.index(valueHeader)] += (int(value[1:]) * 7)
            if valueHeader == 'w':
                #TODO: calulate the days and sum to epoch
                #Assuming in this string weeks start with 1
                weekDay_now = datetime.utcfromtimestamp(UTCSec).weekday() + 1
                weekDays = value[1:].split('-')

                #If day passed minimum
                if weekDay_now > weekDays[-1]:

                else:
                    for weekDay in weekDays:
                        pass
            repetition_str += '/' + value


        newEpoch = self.get_time_in(newAlarm, reminder_old[1])
        #TODO: sum the other two values
        
        reminder_new = [reminder_old[0], newEpoch, 2, repetition_str]

        #TODO: Add new reminder to DB
        return reminder_new

    def check_alarm(self):
        """
        Go through self.reminders and check what alarm is ready.

        Args:
            self.reminders: List of all the reminders in a threshold.

        Returns:
            Return list of alarms that are due.
        """
        threshold = 60 #add second threshold for current time
        currentTime_epoch = datetime.now(timezone.utc).timestamp() + threshold

        dueAlarm = []
        for reminder in self.reminders:
            #Since list is sorted break when number is greater
            if currentTime_epoch < reminder[2]:
                break
            #Add reminder to dueAlarm and remove from reminders
            dueAlarm.append(reminder)
            if reminder[3] == 2: #Standard
                reminder_new = reminder_concurrency(reminder)
                if reminder_new != None:
                    self.reminders.append()

            db.execute('UPDATE remindersTbl r SET reminderStr = ?, alarm = ? WHERE status = ?', ([reminder[0]], [reminder[1]], [0]))
            self.reminders.remove(reminder)

        #TODO: create a string for each value that the ai can read
        return dueAlarm

    def update_list(self):
        """
        Update the self.reminders from the database.

        Returns:
            self.reminders witt the populated reminders.
        """
        #TODO: update every x hours and get reminders under those x hours
        timeUTC_epoch = datetime.now(timezone.utc).timestamp()
        db = self.conn.cursor()
        db.execute("""
        SELECT reminderStr, alarm, status FROM remindersTbl r
        WHERE r.status > 0""")
        #If status is greater than 0 then it is still available
        self.reminders = []
        
        for reminder in db.fetchall():
            self.reminders.append(reminder)

        #sort by epoch
        self.reminders.sort(key = lambda x: x[2])

if __name__ == "__main__":
    reminder = CurrentReminders()
    reminder.set_reminder("Testing Reminder", [None, 20, 40, 30, 70, None], False)
    UTCSec = datetime.now(timezone.utc).timestamp()
    print(UTCSec, )