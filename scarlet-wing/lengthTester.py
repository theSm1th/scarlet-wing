import timeTable

for day in timeTable.table:
    item = timeTable.table[day]
    for numerator in item:
        i = numerator
        if i[2] is None:
            string = i[0] + " 10m"
        else:
            string = i[0] + " " + i[1] + " " + i[2] + " 10m"
        if len(string) < 20:
            print(string + " passed")
        else:
            print(string + " failed, length " + str(len(string)))