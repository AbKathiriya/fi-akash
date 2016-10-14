#--------------------------------------------------------------------------------------#
# To install dependencies :
# pip install beautifulsoup4
# pip install selenium
# Download chrome driver from here https://sites.google.com/a/chromium.org/chromedriver/downloads
# Put driver executable path in $PATH variable
# To run this file : python final.py
#--------------------------------------------------------------------------------------#
import selenium
import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import sys


reload(sys)
sys.setdefaultencoding('utf8')
url = "https://www.venturedeal.com/Security/Logon.aspx"
writer = csv.writer(open("investor.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)
# Function which scrapes investor names and emails from page
def scrape(soup):
    # Find the Investor name
    span = soup.find('span',id = 'ctl00_LeftColumnContentPlaceholder_txtInvestoryCompanyName')
    name = str(span.text).encode('utf-8')
    writer.writerow([name])
    div = soup.find('div',id = 'ctl00_LeftColumnContentPlaceholder_UpdatePanel1')
    # Find the table which has all the investor names and emails
    table = div.find_all('table')[1]
    tds = table.find_all('td')
    details = []
    cnt = 0
    for td in tds[1:]:
        if cnt == 3:
            writer.writerow(details)
            details = []
            cnt = 0
        # Finding Investor positions and their names
        span = td.find('span')
        if span:
            details.append(str(span.text).encode('utf-8'))
            cnt = cnt + 1
        # Finding email attribute
        img = td.find('img')
        if img:
            if 'onclick' in img.attrs:
                email = img.attrs['onclick']
                email = re.findall("'(.*?)'",email)
                details.append(str(email[0]).encode('utf-8'))
                cnt = cnt + 1
# Initialize chrome driver
driver = webdriver.Chrome()
# Open login page
driver.get(url)
# Find username and password field
username = driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_tbEmailAddress")
password = driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_tbPassword")
# Fill up those fields
username.send_keys("mlg33k@gmail.com")
password.send_keys("j@Mg83knf")
# Click on Submit button
driver.find_element_by_name("ctl00$LeftColumnContentPlaceholder$btnLogon").click()
# Find selection tag
select = Select(driver.find_element_by_id('ctl00_LeftColumnContentPlaceholder_drpSearchType'))
# Select venture investors values
select.select_by_value('1')
# Find and click on search button
driver.find_element_by_id("ctl00_LeftColumnContentPlaceholder_btnSubmit").click()
# Wait for results to finish loading
wait = WebDriverWait(driver, 10)
soup = BeautifulSoup(driver.page_source,'html.parser')
table = soup.find('table', id = 'ctl00_SingleColumnContentPlaceholder_grd1')
values = []
# Store all venture Investors result in values list
for td in table.find_all('td'):
    a = td.find('a')
    if a:
        if 'SearchResultInvestorDetail' in a.attrs['href']:
             values.append(a.text)
# Click on the first Investor name
driver.find_element_by_link_text(values[0]).click()
while True:
    try:
        invest = BeautifulSoup(driver.page_source,'html.parser')
        scrape(invest)
        # Find Next button and click on that to view and scrape the next page
        elem = driver.find_element_by_link_text('NEXT >')
        if elem.is_enabled():
            elem.click()
        else:
            break
    except NoSuchElementException:
        break
driver.quit()
