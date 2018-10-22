from requests import get
from requests.exceptions import RequestException
import pandas as pd
import time
from bs4 import BeautifulSoup

def get_data(url):
    try:
        with get(url, stream=True) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def parse_data(raw_html):
    df = pd.DataFrame(columns=['Date', 'Time','Headline'])
    html = BeautifulSoup(raw_html, 'html.parser')
    stories = html.find('ul', {"id":"pipeline_assetlist_0"})
    for story in stories.find_all('div',{'class' : 'headline'}):
        headline = story.find('a').text.strip()
        raw_time = story.find('a').findNext().text
        tim = time.strptime(raw_time.split("ET")[0], '%I:%M %p')
        dat = datetimedate.strptime(raw_time.split(",")[1], '%d %B, %Y')
        print(headline, raw_time)
        df = df.append(pd.DataFrame(columns=df.columns, data=[[]]))
    return df


for i in range(1,99):
    raw_data = get_data("https://www.cnbc.com/bitcoin/?page=" + str(i))
    df = parse_data(raw_data)
