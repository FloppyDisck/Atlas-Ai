import pytz
import sqlite3
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import *
from operator import itemgetter

class CurrentReminders:
    def __init__(self, db_path = 'custom_actions/storage/remindersDB'):
        """
        Create a reminder monitor object.

        This will store all upcoming reminders and remind when
        theyre due.

        Args:
            db_path: Where to get the reminders from.
        """
        self.conn = sqlite3.connect(db_path)
        self.update_list()

    def set_reminder(self, reminder, alarm_epoch, repeat_frequency = None):
        """
        Create a reminder and add it to the reminder DB

        Args:
            reminder: The reminder description.
            alarm: Array list that will be added to time.
            exactTime: A boolean that describes the alarm type.
            repeat_frequency: A string that describes the repetition type.
                Repeat every:
                s[second]/m[minutes]/h[hour]/D[day]/M[month]/Y[year]/T[times]/w[week_day]/W[Weeks]

        Returns:
            Returns info that confirms the saved data.
        """

        if repeat_frequency == None:
            reminder_status = 1
        else:
            #Run reminder_concurrency after alarm is done
            reminder_status = 2

        #Add the reminder to the ram
        command_set = [reminder, alarm_epoch, reminder_status, repeat_frequency]
        self.reminders.append(command_set)

        #Sort by the smallest epoch
        self.reminders.sort(key = itemgetter(1))

        db = self.conn.cursor()
        db.execute('INSERT INTO reminderstbl (reminderStr, alarm, status, concurrency) VALUES (?, ?, ?, ?)', command_set)
        self.conn.commit()

        #return string confirmation of "set blah blah at TIMEHERE"
        return command_set

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
        reminder_list = []
        
        for reminder in db.fetchall():
            reminder_list.append(reminder)

        #sort by epoch
        reminder_list.sort(key = itemgetter(1))

        #if a day in the close week say so
        #You have reminders tomorrow; you have reminders this sunday
        day_date = datetime.fromtimestamp(epoch_day).strftime('%m %d') 
        if len(reminder_list) == 0:
            return_string = f"You have no reminders for {day_date}"
        elif len(reminder_list) == 1:
            return_string = f"You only have to {reminder_list[0][0]} at {datetime.fromtimestamp(reminder_list[0][1]).strftime('%H %M')}"
        elif len(reminder_list) == 2:
            return_string = f"You have to {reminder_list[0][0]} at {datetime.fromtimestamp(reminder_list[0][1]).strftime('%H %M')} and then {reminder_list[1][0]} at {datetime.fromtimestamp(reminder_list[1][1]).strftime('%H %M')}"
        elif len(reminder_list) > 2:
            import random
            flavor_string = ["then ", "later ", "after ", "and ", "also "]
            return_string = f"You have to {reminder_list[0][0]} at {datetime.fromtimestamp(reminder_list[0][1]).strftime('%H %M')} "
            for index in range(1, len(reminder_list) - 1):
                rand_index = random.randint(0, len(flavor_string) - 1)
                return_string = return_string + flavor_string[rand_index] + f"{reminder_list[index][0]} at {datetime.fromtimestamp(reminder_list[index][1]).strftime('%H %M')} "
            return_string = return_string + f"finally remember to {reminder_list[-1][0]} at {datetime.fromtimestamp(reminder_list[-1][1]).strftime('%H %M')}"
        return return_string
    
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
        new_alarm = datetime.fromtimestamp(reminder_old[1])

        repetition_str = ""
        for value in repetition:
            if value != "":
                #Set the header Char
                value_header = value[:1]

                #Relative delta handles leapyears and month disbalances
                if value_header == 'Y':
                    new_alarm += relativedelta(years=int(value[1:]))
                if value_header == 'M':
                    new_alarm += relativedelta(months=int(value[1:]))
                if value_header == 'D':
                    new_alarm += relativedelta(days=int(value[1:]))
                if value_header == 'h':
                    new_alarm += relativedelta(hours=int(value[1:]))
                if value_header == 'm':
                    new_alarm += relativedelta(minutes=int(value[1:]))
                if value_header == 's':
                    new_alarm += relativedelta(seconds=int(value[1:]))
                if value_header == 's':
                    new_alarm += relativedelta(weeks=int(value[1:]))

                #Remove a repetition since this is finite
                if value_header == 'T':
                    times = int(value[1:])
                    if times == 0:
                        return None
                    value = 'T' + str(times-1)

                if value_header == 'w':
                    #Assuming in this string weeks start with 1
                    next_day = 0
                    week_day_now = datetime.now(timezone.utc).weekday() + 1
                    week_days = sorted(value[1:].split('-'))

                    #Check which week_day is the next one
                    for week_day in week_days:
                        if week_day_now <= week_day:
                            next_day = week_day
                    if next_day == 0:
                        next_day = week_days[0]

                    #Calculate how many days to skip
                    if week_day_now == next_day:
                        new_alarm += relativedelta(days=7)
                    elif week_day_now > next_day:
                        new_alarm += relativedelta(days=(7 - week_day_now + next_day))
                    else:
                        new_alarm += relativedelta(days=(next_day - week_day_now))
 
                repetition_str += '/' + value

        new_reminder = self.set_reminder(reminder_old[0], new_alarm.timestamp(), repeat_frequency=repetition_str)
        return new_reminder

    def check_alarm(self):
        """
        Go through self.reminders and check what alarm is ready.

        Args:
            self.reminders: List of all the reminders in a threshold.

        Returns:
            Return list of alarms that are due.
        """
        threshold = 0 #add second threshold for current time
        current_time_epoch = datetime.now(timezone.utc).timestamp() + threshold
        due_alarm = []
        for reminder in self.reminders:
            #Since list is sorted break when number is greater
            if current_time_epoch < reminder[1]:
                break
            #Add reminder to due_alarm and remove from reminders
            due_alarm.append(reminder)
            if reminder[2] == 2: #Standard
                self.reminder_concurrency(reminder)
 
            db = self.conn.cursor()
            db.execute('UPDATE remindersTbl SET status = ? WHERE reminderStr = ? AND alarm = ?', (0, reminder[0], reminder[1]))
            self.reminders.remove(reminder)
            self.conn.commit()

        #TODO: create a string for each value that the ai can read
        return due_alarm

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
    #TODO: Test all concurrency features, make a fake spedup timer to test them all; test the delete function; delete done reminders from database
    #print(reminder.set_reminder("2 minute reminder", 1565103208))
    #print(reminder.set_reminder("4 minute reminder", 1565103328))
    #print(reminder.set_reminder("8 minute reminder", 1565103568))
    print(reminder.set_reminder("Repeat reminder", 1565413354, "m2/T2"))
    print(f"Listing reminders: {reminder.reminders}")
    print(reminder.list_reminder(1565413354))

    utc_secs = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    current_time = datetime.now()
    print(current_time, utc_secs, "Start Time") #This has proven to be the accurate time

    while True:
        reminders = reminder.check_alarm()
        if reminders != []:
            utc_secs = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
            current_time = datetime.now()
            print(current_time, utc_secs, reminders)