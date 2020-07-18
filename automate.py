import json
import time
import datetime

import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager



class Teams:
    def __init__(self):

        self.opts = ChromeOptions()
        self.opts.add_experimental_option("detach", True)
        self.opts.add_argument('--ignore-certificate-errors')
        self.opts.add_argument('--ignore-ssl-errors')
        self.opts.add_argument("--use-fake-ui-for-media-stream")

        self.browser = Chrome(executable_path = 'Chrome-Driver/V83/chromedriver' , chrome_options=self.opts)

        self.link = 'https://www.microsoft.com/en-in/microsoft-365/microsoft-teams/group-chat-software'
        self.x = 1600
        self.y = 1600

        self.sign_in = 'mectrl_main_trigger'
        self.login_id = 'i0116'
        self.password_id = 'i0118'
        self.btn_class = 'inline-block'
        self.popup_id = 'use-app-lnk'
        self.team_name_id = 'team-name-text'
        self.meeting_class = 'ts-sym ts-btn ts-btn-primary inset-border icons-call-jump-in ts-calling-join-button app-title-bar-button app-icons-fill-hover call-jump-in'


    def start_window(self):


        self.browser.set_window_size(self.x , self.y)
        self.browser.get(self.link)
        
        login_href = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, self.sign_in))
        )

        login_href.click()


    def add_credentials(self):
        with open('assets/credentials.json') as json_data:
            credentials = json.load(json_data)

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, self.login_id))
        )
        email_field.send_keys(credentials['email'] , Keys.ENTER)

        password_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, self.password_id))
        )
        password_field.send_keys(credentials['password'])

        #### To find better method

        time.sleep(5) # DOM to load
        submit_btn = self.browser.find_element_by_class_name(self.btn_class).click()


    def popup_login(self):

        submit_btn = self.browser.find_element_by_class_name(self.btn_class)
        submit_btn.click()


    def popup_ad(self):

        web_app_btn = self.browser.find_element_by_class_name(self.popup_id)
        web_app_btn.click()

    def join_group(self , class_name):
    
        all_user_groups = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.team_name_id))
        )
        all_user_groups = self.browser.find_elements_by_class_name(self.team_name_id)

        for group in range(0 ,len(all_user_groups)):
            if all_user_groups[group].text.lower() == class_name.lower():
                all_user_groups[group].click()
                break
    

    def mute_audio(self):
        
        audio_btn = self.browser.find_element_by_css_selector("toggle-button[data-tid='toggle-mute']>div>button")
        audio_is_on = audio_btn.get_attribute("aria-pressed")
        if audio_is_on == "true":
            audio_btn.click()

    def close_video(self):
        
        video_btn = self.browser.find_element_by_css_selector("toggle-button[data-tid='toggle-video']>div>button")
        video_is_on = video_btn.get_attribute("aria-pressed")
        if video_is_on == "true":
            video_btn.click()


    def join_meeting(self):

        time.sleep(20)

        try:
            meeting_button = WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"button[ng-click='ctrl.joinCall()']"))
            )
        except selenium.common.exceptions.TimeoutException:
            print("Couldn't load the link or Maybe meeting has not been started yet .")
        
        else:
            time.sleep(20)

            meeting_button.click()

            time.sleep(20)

            self.mute_audio()
            self.close_video()

            join_button = WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"div.flex-fill.input-section > div > div > button"))
            )

            join_button.click()

    
    def show_chat(self):

        background = self.browser.find_element_by_css_selector('div > div.video-stream-container')    
        hover = ActionChains(self.browser).move_to_element(background)
        hover.perform()
        chat_btn = self.browser.find_element_by_css_selector('#callingButtons-showMoreBtn > ng-include > svg')
        chat_btn.click()

    def getchats(self):
        pass

    

    def hang_call(self):
        WebDriverWait(self.browser, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#app-bar-2a84919f-59d8-4441-a975-2a8c2643b741'))
    ).click()
        time.sleep(20)
    #     time.sleep(20)
    #     WebDriverWait(self.browser, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'calling-myself-video > div > div.user-avatar-container'))
    # ).click()
        hangup_btn = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-tid='call-hangup']"))
        )
        time.sleep(50) # For a 50 minute class
        print(hangup_btn)
        hangup_btn.click() 
        




def main():

    t1 = Teams()

    # with open('assets/agenda.json') as json_data:
    #     agenda = json.load(json_data)
    
    t1.start_window()
    t1.add_credentials()
    t1.popup_login()
    t1.popup_ad()
    t1.join_group('own') # For example
    t1.join_meeting()
    t1.hang_call()
            

if __name__ == "__main__":
    main()

#es-bottom-overlay