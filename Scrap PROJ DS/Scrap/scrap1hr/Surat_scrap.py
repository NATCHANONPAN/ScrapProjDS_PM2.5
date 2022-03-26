from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

province = []
datetime = []
wind_list = []
temp_list = []
loc = '99.325,9.126'
loc_name = 'Surat'

service = ChromeService(executable_path=ChromeDriverManager().install())

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images":2}
chrome_prefs["profile.managed_default_content_settings"] = {"images":2}

driver = webdriver.Chrome(service = service,options = option)

url = 'https://earth.nullschool.net/#2020/06/30/1500Z/wind/surface/level/overlay=temp/orthographic=-266.70,-1.65,436/loc=' + loc
endurl = 'https://earth.nullschool.net/#2021/01/1/0100Z/wind/surface/level/overlay=temp/orthographic=-266.70,-1.65,436/loc=' + loc

while(True):
        driver.get(url = url)

        #wait all data
        WebDriverWait(driver,100).until(lambda x: x.find_element(By.XPATH,'/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")!= "N/A")
        date = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")
        wind = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[2]/div').text
        temp = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[3]/div').text

        forward = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[5]/div[3]/div[1]/div/button[3]')      
            
        driver.execute_script("arguments[0].click();", forward)
        
        
        print(loc_name,date,wind,temp)
        province.append(loc_name)
        wind_list.append(wind)
        temp_list.append(temp)
        datetime.append(date)

        url = driver.current_url        
        if(url == endurl): break


url = 'https://earth.nullschool.net/#2021/01/01/0100Z/wind/surface/level/overlay=temp/orthographic=-255.00,0.00,661/loc=' + loc
endurl = 'https://earth.nullschool.net/#2021/07/02/0000Z/wind/surface/level/overlay=temp/orthographic=-255.00,0.00,661/loc=' + loc
while(True):        
        driver.get(url = url)

        WebDriverWait(driver,100).until(lambda x: x.find_element(By.XPATH,'/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")!= "N/A")
        date = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")
        wind = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[2]/div').text
        temp = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[3]/div').text

        forward = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[5]/div[3]/div[1]/div/button[3]')    
        driver.execute_script("arguments[0].click();", forward)         
         
        print(loc_name,date,wind,temp)
        province.append(loc_name)
        wind_list.append(wind)
        temp_list.append(temp)
        datetime.append(date)

        url = driver.current_url        
        if(url == endurl): break
    
    
d = {'Province': province, 'DateTime': datetime, 'Wind' : wind_list , 'Temp' :temp_list}
wind_temp = pd.DataFrame(data = d)
wind_temp.to_csv('wt_surat.csv',index=False)