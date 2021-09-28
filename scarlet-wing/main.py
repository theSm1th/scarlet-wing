import logging
import datetime as date
import timeTable

# now = date.datetime.now()
now = date.datetime(2021, 9, 27, 19, 56)  # For testing purposes

#  Try create a log file, exception is caught if it already exists
try:
    file = open("log.txt", "x")
    file.close()
except FileExistsError:
    pass

#  Store the data from the rotation config into usable variables
with open("weekRotation.txt", "r") as week:
    weekRotation = int(week.readline())
    lastChanged = int(week.readline())

#  do a little logging
logging.basicConfig(filename="log.txt", filemode="a", level=logging.INFO)

#  Day is sliced to the first three letters as the timetable indexes work off of a rotation and the first three letters
#  of the week, such as "AMon" and "BTue"
day = now.strftime("%A")[:3]
#  Sets dayNum to the numeric day
dayNum = now.day

if day == "Mon" and lastChanged != dayNum:
    logging.info("Condition fulfilled, changing week type")
    with open("weekRotation.txt", "w") as week:
        if weekRotation == 2:
            week.writelines(f"1\n{dayNum}")
        elif weekRotation == 1:
            week.writelines(f"2\n{dayNum}")

    with open("weekRotation.txt", "r") as week:
        weekRotation = int(week.readline())

#  This statement MUST be here so the usable rotation is only set once it has been changed on Mondays
if weekRotation == 2:
    rotation = "B"
elif weekRotation == 1:
    rotation = "A"

dayDataSet = timeTable.table[rotation + day]


def get_next_period():
    lessonCounter = 0  # Must be set to 1 because the time formats are in index 0, offsetting the other indices by 1
    for time in dayDataSet[0]:
        lessonCounter += 1
        parsedTime = date.datetime(now.year, now.month, now.day, int(time[:2]), int(time[3:]))
        if parsedTime > now:
            print(parsedTime)
            break
    print(lessonCounter)
    return lessonCounter


def get_current_period():
    return get_next_period() - 1


def parse_period(periodNumber):
    return dayDataSet[periodNumber]


print(parse_period(get_current_period()))
