nlu_md = """
## intent:greet
- hey
- hello there
- hi
- hello there
- good morning
- good evening
- moin
- hey there
- goodmorning
- goodevening
- good afternoon
- hey
- hello
- hi
- good morning
- good evening
- good afternoon
- hey there
- hi there
- hii
- Hi

## intent:fine_ask
- I am good, how are you doing?
- I'm fine, how are you?
- I'm good, how are you?
- I am good, how are you?
- Doing good, how are you?
- Awesome, how are you?
- im fine, how are you?
- im good, how are you?
- I am doing good. what about you?
- I'm good, what about you
- awesome what about you

## intent:fine_normal
- I am doing great
- I'm doing great
- I'm fine
- I'm good
- Doing good
- Awesome
- im fine
- im good

## intent:thanks
- Thanks
- Thank you so much
- awesome

## intent:bye
- No, I am good as of now. Bye
- Bye
- see ya

## intent:goodbye
- good by
- see you later
- good night
- good afternoon
- bye
- goodbye
- have a nice day
- see you around
- bye bye
- see you later

## intent:mood_affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:mood_deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:mood_great
- perfect
- very good
- great
- amazing
- feeling like a king
- wonderful
- I am feeling very good
- I am great
- I am amazing
- I am going to save the world
- super
- extremely good
- so so perfect
- so good
- so perfect

## intent:mood_unhappy
- my day was horrible
- I am sad
- I don't feel very well
- I am disappointed
- super sad
- I'm so sad
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not so good
- not very good
- extremly sad
- so saad

## intent:weather_request
<!-- 0 entity questions -->
- How is the weather
- Show me the weather
- Give me the weather
- What's the current atmospheric conditions
<!-- 1 entity questions --> 
- What's the weather for [today](weather_arg:date) <!--Define a synonim (intent:word)-->
- Will it be [cold](weather_arg:temp)
- How [hot](weather_arg:temp) is it
- What is the current [temperature](weather_arg:temp)
- Will it [rain](weather_arg:rain)
- Is it [raining](weather_arg:rain)
- How [clowdy](weather_arg:clowdy) is it going to be
- What is the current [humidity](weather_arg:humidity)
- How [humid](weather_arg:humidity) can it get
- What is the weather like in [Spain](weather_arg:location)
<!-- 2 entity questions -->
- What is the [temperature](weather_arg:temp) like in [Russia](weather_arg:location)
- How [cold](weather_arg:temp) will it be [tomorrow](weather_arg:date)
- How [humid](weather_arg:humidity) is it how [hot](weather_arg:temp) can it get
- Is it [raining](weather_arg:rain) over in [Arizona](weather_arg:location)
- Will it [rain](weather_arg:rain) [today](weather_arg:date)
- How [much](weather_arg:quantity) will it [rain](weather_arg:rain)
<!-- Multiple entity questions -->
- Will it be [raining](weather_arg:rain) and what [temp](weather_arg:temp) will it be [tomorrow](weather_arg:date) in [Puerto Rico](weather_arg:location)

## intent:reminder_set
- set a reminder
- can you set a reminder
- set a reminder for [today](reminder_date) at [eleven thirty](reminder_arg_time)
- remind me to [lock the door](reminder_arg)
- remind me to [turn off the lights](reminder_arg) [tomorrow](reminder_arg_date) at [night](reminder_arg_time)
- 
"""