import requests
import pandas as pd
import datetime
import jdatetime
from pathlib import Path 

# This function is for check if description of the day is matched with one in Hijri List or not
def Desc_Match(event_name, Hijri_Holidays):
    match_item = None
    for j in range(len(Hijri_Holidays)):
    
        if event_name == Hijri_Holidays[j][4]:
            match_item = Hijri_Holidays[j][2]

    return match_item

# This function is for getting information from https://persiancalapi.ir for each Gregorian date
def get_info(Date):
    Desc = None
    link = 'https://persiancalapi.ir/gregorian/%s/%s/%s' %(Date.strftime('%Y'), Date.strftime('%m'), Date.strftime('%d'))
    response = requests.get(link)
    event_size = len(response.json()['events'])
    if response.json()['is_holiday'] == True and event_size > 0:

        for i in range(event_size):
            event_name = response.json()['events'][i]['description']
            Desc_temp = Desc_Match(event_name, Hijri_Holidays)
            if Desc_temp != None: Desc = Desc_temp
    
    return Desc

# This function is for recognizing any national holidays and based of Jalali dates
def National_Holiday(ShamsiMonth, ShamsiDay, Jalali_Holidays):
    Desc = None
    for i in range(len(Jalali_Holidays)):
        if Jalali_Holidays[i][0] == ShamsiDay and Jalali_Holidays[i][1] == ShamsiMonth:
            Desc = Jalali_Holidays[i][2]

    return Desc


# Load official holidays excel file 
filepath = "C:\\Users\\Hessum\\OneDrive\\Python Projects\\Iranian Holidays\\Iranian-Calendar-Holidays\\Official Holiodays.xlsx"
df = pd.read_excel(filepath)

# Separate national and religious holidays from each other. Both are list of lists
# [Day, Month, English Description, Persian Month Name, Persian Description which is copied from Time.ir, Keyword]
Hijri_Holidays = df[df['Calendar Type'] == 'Hijri'].drop(columns=['Calendar Type']).values.tolist()
Jalali_Holidays = df[df['Calendar Type'] == 'Jalali'].drop(columns=['Calendar Type']).values.tolist() 

Delta = datetime.timedelta(1)                       # One day object
MiladiDate = datetime.date(2022, 1, 1) - Delta      # Start Date in Gregorian
rows_list= []
year = 1                                            # Number of years to sweep
iter = int(year * 366)                              # Number of days to sweep

for i in range(iter):
    info = {}
    MiladiDate = MiladiDate + Delta

    ShamsiDate = jdatetime.datetime.fromgregorian(datetime=MiladiDate).date()
    ShamsiMonth, ShamsiDay = int(ShamsiDate.strftime('%m')), int(ShamsiDate.strftime('%d'))
    print(ShamsiDate, MiladiDate, MiladiDate.strftime('%a'))
    info['Date'] = MiladiDate
    info['Jalali_Date'] = ShamsiDate
    info['Description'] = National_Holiday(ShamsiMonth, ShamsiDay, Jalali_Holidays)
    Desc_temp = get_info(MiladiDate)
    if Desc_temp != None and info['Description'] != None: 
        info['Description2'] = Desc_temp

    elif Desc_temp != None: 
        info['Description'] = Desc_temp
        info['Description2'] = None

    if info['Description'] == None: continue
    print(info['Description'])
    rows_list.append(info)

df = pd.DataFrame(rows_list)
df.tail(5)

filepath2 = Path("C:\\Users\\Hessum\\OneDrive\\Python Projects\\Iranian Holidays\\Iranian-Calendar-Holidays\\Iranian Calendar Holidays.csv", exist_ok=True)  
filepath2.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(filepath2, index=False)