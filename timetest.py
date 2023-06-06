from datetime import datetime

now = datetime.now()


def get_time_of_day(time):
    if time > 19 or time < 4:
        return "night"
    elif time < 12:
        return "morning"
    elif time == 12:
        return "Noon"
    elif time < 16:
        return "Afternoon"
    else:
        return "Evening"


time_of_day = get_time_of_day(now.hour)
current_time = now.strftime("%H:%M %p")

print(time_of_day)
print(current_time)