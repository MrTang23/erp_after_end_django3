from datetime import datetime

current_time = datetime.now()
month = str(current_time.month)
day = str(current_time.day)
hour = str(current_time.hour)
minute = str(current_time.minute)
second = str(current_time.second)

if current_time.month < 10:
    month = '0' + str(current_time.month)
if current_time.day < 10:
    day = '0' + str(current_time.day)
if current_time.hour < 10:
    hour = '0' + str(current_time.hour)
if current_time.minute < 10:
    minute = '0' + str(current_time.minute)
if current_time.second < 10:
    second = '0' + str(current_time.second)
print(str(current_time.year) + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second)
