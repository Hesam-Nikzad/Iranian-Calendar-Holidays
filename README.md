# Iranian-Calendar-Holidays
This is a project for those who need a dataset of Iranian calendar holidays.
I inspired by the "hpez" user and thanks him for his/her deeds. This is his/her repository: https://github.com/hpez/persiancalapi.git .

Requirements:
`pip install pandas jdatetime asyncio aiohttp beautifulsoup4`



Example:

```python
```

from IRC import *



if __name__ == '__main__':

  cal = calendar('1411-01-01', '1430-12-29')

  asyncio.run(cal.crawl_pages())

  cal.save()

```
