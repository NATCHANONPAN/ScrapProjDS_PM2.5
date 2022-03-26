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
loc = '99.325355,9.126057'
loc_name = 'Surat'

service = ChromeService(executable_path=ChromeDriverManager().install())

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images":2}
chrome_prefs["profile.managed_default_content_settings"] = {"images":2}

driver = webdriver.Chrome(service = service,options = option)

counter = (31+31+30+31+30+32)*8

url = 'https://earth.nullschool.net/#2020/06/30/1800Z/wind/surface/level/overlay=temp/orthographic=-266.70,-1.65,436/loc=' + loc

while(counter>=0):
        driver.get(url = url)

        #wait all data
        WebDriverWait(driver,100).until(lambda x: x.find_element(By.XPATH,'/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")!= "N/A")
        date = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")
        wind = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[2]/div').text
        temp = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[3]/div').text
        counter-=1

        forward = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[5]/div[3]/div[1]/div/button[3]')      
            
        driver.execute_script("arguments[0].click();", forward)
        
            
        print(loc_name,date,wind,temp)
        province.append(loc_name)
        wind_list.append(wind)
        temp_list.append(temp)
        datetime.append(date)
        url = driver.current_url
        
counter = (31+28+31+30+30+32)*24

url = 'https://earth.nullschool.net/#2021/01/01/0000Z/wind/surface/level/overlay=temp/orthographic=-255.00,0.00,661/loc=' + loc
while(counter>=0):        
            driver.get(url = url)

            WebDriverWait(driver,100).until(lambda x: x.find_element(By.XPATH,'/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")!= "N/A")
            date = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[2]/div[3]').get_attribute("innerText")
            wind = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[2]/div').text
            temp = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[3]/div').text
            counter-=1

            forward = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[4]/div/div[5]/div[3]/div[1]/div/button[3]')    
            driver.execute_script("arguments[0].click();", forward)         
            url = driver.current_url 
         
            print(loc_name,date,wind,temp)
            province.append(loc_name)
            wind_list.append(wind)
            temp_list.append(temp)
            datetime.append(date)
    
    
d = {'Province': province, 'DateTime': datetime, 'Wind' : wind_list , 'Temp' :temp_list}
wind_temp = pd.DataFrame(data = d)
wind_temp.to_csv('Surat_every1.csv',index=False)