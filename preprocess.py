import pandas as pd
import re

def preprocess(file_data):
    file_data = file_data.replace('\u202f', ' ')
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[AP]M\s-\s'
    message = re.split(pattern, file_data)[1:]
    dates = re.findall(pattern, file_data)
    data = pd.DataFrame({'user_message': message, 'message_dates': dates})
    data['message_dates'] = (data['message_dates'].str.replace(
        ' -', ' ', regex=False).str.strip())
    data['message_dates'] = pd.to_datetime(
        data['message_dates'], format='%m/%d/%y, %I:%M %p', errors='coerce')
    users = []
    messages = []
    for message in data['user_message']:
        entry = re.split(r'(.*?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append("".join(entry[2]))
        else:
            users.append('user-notification')
            messages.append(entry[0])
    data['user'] = users
    data['message'] = messages
    data.drop(columns=['user_message'], inplace=True)
    data['date'] = data['message_dates'].dt.date
    data['day'] = data['message_dates'].dt.day
    data['day_name'] = data['message_dates'].dt.day_name()
    data['hour'] = data['message_dates'].dt.hour
    data['minutes'] = data['message_dates'].dt.minute
    data['month'] = data['message_dates'].dt.month
    data['month_name'] = data['message_dates'].dt.month_name()
    data['year'] = data['message_dates'].dt.year
    data.drop(columns=['message_dates'], inplace=True)
    period = []
    for hour in data['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    data['period'] = period
    
    return pd.DataFrame(data)

