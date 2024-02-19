from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
import os
from dotenv import load_dotenv
import pandas as pd

class LinkedInMessageSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.options = webdriver.ChromeOptions()
        user_data = r"C:\Users\jenni\AppData\Local\Google\Chrome\User Data"
        self.options.add_argument(f'--user-data-dir={user_data}')
        self.options.add_argument(f'profile-directory=Default')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
    #메시지 전송
    def send_message(self, profile_url, message):
        self.driver.get(profile_url)
        time.sleep(15)
        message_button= self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button/span')
        message_button.click()
        self.driver.implicitly_wait(1)
        print("message button clicked")
        try:
            title = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/div/input')
            content = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/div[3]/div[3]/form/div[3]/div/div/div[1]')
            title.send_keys(message['title'])
            content.send_keys(message['content'])
            time.sleep(5)
            send_button = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/div[3]/div[3]/form/footer/div[2]')
            send_button.click()
        except:
            content =  self.driver.find_element(By.XPATH,'/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/form/div[3]/div/div[1]/div[1]')
            content.send_keys(message['content'])
            time.sleep(5)
            send_button = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/form/footer/div[2]/div[1]')
            send_button.click()
            time.sleep(3)
            delete_button = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/header/div[4]/button[3]')
            time.sleep(3)
            delete_button.click()
        print("message sent")

    def close(self):
        self.driver.quit()