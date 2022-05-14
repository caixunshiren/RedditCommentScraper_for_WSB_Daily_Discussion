import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date, timedelta
from dateutil.parser import parse
from tqdm import tqdm

driver = webdriver.Chrome(ChromeDriverManager().install())
MONTH_DICT = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


def get_thread_id(target_date):
    '''
    :param target_date: string in format "yyyy-mm-dd"
    :return: url of the thread
    '''
    dates = target_date.split('-')
    year, month, day = dates[0], MONTH_DICT[dates[1]], dates[2]

    # try daily discussion
    url = f"https://www.reddit.com/r/wallstreetbets/search/?q=Daily%20Discussion%20Thread%20for%20{month}%20{day}" \
          f"%20{year}&restrict_sr=1&sr_nsfw="
    driver.get(url)
    links = driver.find_elements_by_xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]')
    for a in links:
        if a.text.startswith('Daily Discussion Thread'):
            date = " ".join(a.text.split(' ')[-3:])
            parsed = parse(date)
            if parse(target_date) == parsed:
                link = a.find_element_by_xpath('../..').get_attribute('href')
                return link

    # try weekend discussion
    url = f"https://www.reddit.com/r/wallstreetbets/search/?q=Weekend%20Discussion%20Thread%20for%20the%20Weekend%20" \
          f"of%20{month}%20{day}%2C%20{year}&restrict_sr=1&sr_nsfw="
    driver.get(url)
    links = driver.find_elements_by_xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]')
    for a in links:
        if a.text.startswith('Weekend Discussion Thread'):
            date = " ".join(a.text.split(' ')[-3:])
            parsed = parse(date)
            if parse(target_date) == parsed:
                link = a.find_element_by_xpath('../..').get_attribute('href')
                return link

    return "NA"


# date_input = "2021-10-09"
# print(get_thread_id(target_date=date_input))
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == '__main__':
    start_date = date(2020, 1, 1)# "2020-01-01"
    end_date = date(2022, 5, 13)# "2022-05-13"
    data = []
    for single_date in tqdm(daterange(start_date, end_date)):
        date_input = single_date.strftime("%Y-%m-%d")
        try:
            url = get_thread_id(target_date=str(date_input))
            data.append((str(date_input), url))
        except:
            url = "NA"
            data.append((str(date_input), url))
    data = pd.DataFrame(data, columns = ['date', 'url'])
    data.to_csv("daily_discussion_thread_urls.csv")