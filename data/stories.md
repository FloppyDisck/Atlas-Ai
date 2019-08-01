## fallback
- utter_default

## greeting path 1
* greet
    - utter_greet

## fine path 1
* fine_normal
    - utter_help

## fine path 2
* fine_ask
    - utter_reply

## thanks path 1
* thanks
    - utter_anything_else

## bye path 1
* bye
    - utter_bye

## request weather
* weather_request
    - action_weather_return

## Reminder complete
* reminder_set{reminder:'clean up the bedroom', time:'2019-07-29T00:00:00.000+00:00'}
    - action_reminder_set

## Reminder no intent
* reminder_set{time:'2019-07-29T00:00:00.000+00:00'}
    - utter_reminder_noReminder
* inform{reminder:'clean up the bedroom'}
    - action_reminder_set

## Reminder no time
* reminder_set{reminder:'clean up the bedroom'}
    - utter_reminder_noTime
* inform{time:'2019-07-29T00:00:00.000+00:00'}
    - action_reminder_set

## Reminder empty
* reminder_set
    - utter_reminder_noReminder
* inform{reminder:'clean up the bedroom'}
    - utter_reminder_noTime
* inform{time:'2019-07-29T00:00:00.000+00:00'}
    - action_reminder_set