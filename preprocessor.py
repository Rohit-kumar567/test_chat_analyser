import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime format (robust parsing)
    df['message_date'] = pd.to_datetime(df['message_date'], dayfirst=True, errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate Users and Messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])  # Extract username
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract multiple date-time components
    if 'date' in df.columns and not df['date'].isnull().all():
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
    else:
        # Fill with default values if date parsing fails
        df['only_date'] = pd.NaT
        df['year'] = pd.NaT
        df['month_num'] = pd.NaT
        df['month'] = pd.NaT
        df['day'] = pd.NaT
        df['day_name'] = pd.NaT
        df['hour'] = pd.NaT
        df['minute'] = pd.NaT

    # Extract period for better time-based analysis
    if 'hour' in df.columns:
        df['period'] = df['hour'].apply(lambda x: f"{int(x)}-{(int(x) + 1) % 24}" if pd.notna(x) else '')
    else:
        df['period'] = ''

    return df
