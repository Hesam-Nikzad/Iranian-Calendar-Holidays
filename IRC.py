import traceback
import pandas as pd
import jdatetime
import asyncio
import aiohttp
import os
from bs4 import BeautifulSoup


class calendar:
    def __init__(self, startDate, endDate):
        self.path = os.getcwd().replace('\\', '/')
        self.deltaDate = jdatetime.timedelta(1)
        self.baseUrl = 'https://www.time.ir/fa/event/list/0/'
        self.startDate = jdatetime.datetime.strptime(startDate, '%Y-%m-%d').date()
        self.endDate = jdatetime.datetime.strptime(endDate, '%Y-%m-%d').date()
        self.url_make()

    def url_make(self):
        self.urlList = []
        self.dates = []
        date = self.startDate
        while date <= self.endDate:
            year = date.year
            month = date.month
            day = date.day
            self.urlList.append(f'{self.baseUrl}{year}/{month}/{day}')
            self.dates.append(date)
            date += self.deltaDate

    def crawl(self, soup, date):
        day = {}
        day['date'] = date
        events = soup.find_all('li', class_ = 'eventHoliday')
        i = 1
        for event in events:
            event = event.get_text()
            event = event.split('\r')[1].strip()
            day[f'event_{i}'] = event
            i += 1

        return day

    async def crawl_pages(self):

        self.eventsList = []

        def get_tasks(session):
            tasks = []
            for url in self.urlList:
                tasks.append(session.get(url))
            
            return tasks 

        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            for response, date in zip(responses, self.dates):
                try:
                    self.eventsList.append(self.crawl(BeautifulSoup(await response.text(), "html.parser"), date))
                except:
                    with open(self.path + '/error.txt', 'a') as file:
                        file.write('%s \n' %(traceback.format_exc()))
        
        self.eventsList = [d for d in self.eventsList if len(d) > 1]
        
        return self.eventsList

    def save(self):
        df = pd.DataFrame(self.eventsList)
        df.to_csv(self.path + '/Iranian Calendar Holidays.csv', index=False)

        print(f'The holidays information saved on: {self.path}')


if __name__ == '__main__':
    cal = calendar('1411-01-01', '1430-12-29')
    asyncio.run(cal.crawl_pages())
    cal.save()