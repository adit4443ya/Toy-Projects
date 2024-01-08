import pandas as pd 
import re 
from datetime import datetime


def textPreProcessor(data):
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s[^\/]+:[^\d{1,2}]+'
    messages = re.findall(pattern, data)

    #splitting each lines
    message_data = [message.split(' - ',1) for message in messages]
    date_time = [message[0] for message in message_data]
    sender_message = [message[1].split(': ',1) for message in message_data]

    # Creating the dataframe
    df = pd.DataFrame(sender_message, columns=['Sender', 'Message'])
    df['Date'] = [dt.split(',')[0] for dt in date_time]
    df['Time'] = [f"{dt.split(',')[1]} {'AM' if 'AM' in dt else 'PM'}" for dt in date_time]
    df.Message=df.Message.astype('str')
    df['Message'] = df['Message'].apply(lambda x: ' '.join(x.split('\n')))
    df.Time=df.Time.apply(lambda x:" ".join(x.split()[0:2]))
    df['datetime']=df['Date']+ " " +df['Time']
    df['datet']=df.datetime.apply(lambda x: datetime.strptime(x, '%m/%d/%y %I:%M %p'))
    df=df[['Sender','Message','Date','Time','datet']]
    df['year']=df.datet.dt.year
    df['Minute']=df.datet.dt.minute
    df['months']=df.datet.dt.month_name()
    df['days']=df.datet.dt.day_name()
    df['date']=df.datet.dt.day
    df['month_num']=df.datet.dt.month
    df['hours']=df.datet.dt.hour
    period=[]
    for hour in df.hours:
        if hour==23:
            period.append(str(hour)+"-"+str(00))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    df=df[df['Sender']!='group notification']
    df=df[df['Message']!='<Media omitted> ']
    f=open('stop_hinglish.txt','r',encoding='utf-8')
    s=f.read()
    s=s.split('\n')
    df['Cleaned MSG'] = df['Message'].apply(lambda x: ' '.join([word for word in x.split() if word not in s]))
    df=df[df['Sender']!='Aditya Trivedi:']
    df['time_diff'] = df['datet'].diff().dt.total_seconds() / 60
    df['continuous_group'] = (df['time_diff'] > 10).cumsum()
    df['group_duration'] = df.groupby(['continuous_group'])['datet'].transform(lambda x: (x.max() - x.min()).total_seconds() / 3600)

    
    return df