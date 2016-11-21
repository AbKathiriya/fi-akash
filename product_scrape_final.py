import selenium
import xlrd
import xlwt
from xlwt import Workbook
from xlrd import open_workbook
from xlutils.copy import copy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

##------------------------------- CONFIG OPTIONS ----------------------------------------##

url = 'http://webconnect.groupnews.com.au/'
sheet_no = 0                        # Here you can configure sheet number, for first sheet give sheet_no = 0
sheetname = 'office4001-4500.xls'                # Here change the filename everytime you run the script otherwise it will override the existing same xls file.

##------------------------------------- END ---------------------------------------------##

driver = webdriver.Chrome()

def scrape_info(id):
    result = []
    prod_url = ''
    info = ''
    try:
        search = driver.find_element_by_name("ctl00$ControlNavTop1$txtTopSearch")
        search.send_keys(id)
        driver.find_element_by_name("ctl00$ControlNavTop1$btnTopSearch").click()
        driver.find_element_by_id('ctl00_contentMain_gridMain_ctl02_linkProduct').click()
        soup = BeautifulSoup(driver.page_source,'html.parser')
        prod_img = soup.find('a', id = 'ctl00_contentMain_imgProduct')

        if prod_img is not None:
            prod_url = prod_img.attrs['href']
            prod_url = url + prod_url
        add_info = soup.find('span', id = 'ctl00_contentMain_LoginView2_lblAdditionalDescription1')
        if add_info is not None:
            p = add_info.find('p')
            if p is not None:
                info = p.text.strip()
            else:
                info = add_info.text.strip()
        print id
        print prod_url
        print info
        print
    except (NoSuchElementException, TimeoutException) as e:
        print e
        pass
    except:
        print 'Exception'
        pass
    result.append(prod_url)
    result.append(info)

    return result



if __name__ == '__main__':
    rb = open_workbook('Workbook4001-4500.xlsx')
    wb = Workbook()
    # Open login page http://webconnect.groupnews.com.au/
    driver.get(url)
    # Find username and password field from login page
    username = driver.find_element_by_id("ctl00_contentMain_loginMain_UserName")
    password = driver.find_element_by_id("ctl00_contentMain_loginMain_Password")
    # Fill up those fields by sending these key strokes
    username.send_keys("8000186A")
    password.send_keys("1234")
    # Click on Submit button
    driver.find_element_by_name("ctl00$contentMain$loginMain$LoginButton").click()
    # for s in rb.sheets():
    s = rb.sheet_by_index(sheet_no)
    headers = []
    content = []
    sheet_name = s.name
    sheet = wb.add_sheet(sheet_name)
    for row1 in range(s.ncols):
        headers.append(s.cell(0,row1).value)
    # headers.append('Image url')
    # headers.append('Additional Information')
    content.append(headers)
    for row in range(1,s.nrows):
        values = []
        for col in range(0,s.ncols):
            values.append(s.cell(row,col).value)
        try:
            product_id = int(values[0])
            char_product_id = str(product_id)
            if(len(char_product_id) == 3):
                char_product_id = '00'+char_product_id
                product_id = int(char_product_id)
                print product_id
            else if(len(char_product_id) == 4):
                char_product_id = '0'+char_product_id
                product_id = int(char_product_id)
                print product_id
        except:
            product_id = values[0]
        # res = scrape_info(product_id)
        values.append(res[0])
        values.append(res[1])
        content.append(values)
    # for rowno,rowcon in enumerate(content):
    #     for i,val in enumerate(rowcon):
    #         sheet.write(rowno,i,val)
    # wb.save(sheetname)
