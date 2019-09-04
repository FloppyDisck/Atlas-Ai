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

## reminder_set complete
* reminder_set{"reminder":"clean up the bedroom", "time":"2019-07-29T00:00:00.000+00:00"}
    - action_reminder_set

## reminder_set no intent
* reminder_set{"time":"2019-07-29T00:00:00.000+00:00"}
    - utter_reminder_set_noReminder
* inform{"reminder":"clean up the bedroom"}
    - action_reminder_set

## reminder_set no time
* reminder_set{"reminder":"clean up the bedroom"}
    - utter_reminder_set_noTime
* inform{"time":"2019-07-29T00:00:00.000+00:00"}
    - action_reminder_set

## reminder_set empty
* reminder_set
    - utter_reminder_set_noReminder
* inform{"reminder":"clean up the bedroom"}
    - utter_reminder_set_noTime
* inform{"time":"2019-07-29T00:00:00.000+00:00"}
    - action_reminder_set

## reminder_delete complete
* reminder_delete{"reminder":"turn off the computer"}
    - action_reminder_delete

## reminder_delete empty
* reminder_delete
    - utter_reminder_delete_noReminder
* inform{"reminder":"buy groceries"}
    - action_reminder_delete

## reminder_list complete
* reminder_list{"time":"2019-07-29T00:00:00.000+00:00"}
    - action_reminder_list

## reminder_list empty
* reminder_delete
    - utter_reminder_delete_noReminder
* inform{"time":"2019-07-29T00:00:00.000+00:00"}
    - action_reminder_list