'''
    Instagram Bot
    Created By : Biswaraj
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

class InstagramBot:

    def __init__(self, username, password):

        '''
            Args :
                username : (String) The Username of the user for Login.
                password : (String) The password of the user for Login.

        '''
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome('chromedriver.exe') # Path of the Chrome driver Executable.

        
    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(1)

        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(self.username) # or self.driver.find_elements_by_css_selector('form input')[0]
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.password) # or self.driver.find_elements_by_css_selector('form input')[1]
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()

        time.sleep(4)
        self.driver.find_element_by_xpath('//button[text() = "Not Now"]').click()

    def nav_user(self, user):
        self.driver.get('https://www.instagram.com/{}'.format(user))


    def follow_user(self):
        
        time.sleep(2)

        follow_button = self.driver.find_element_by_css_selector('button')
        if follow_button.text != 'Message':
            follow_button.click()
            time.sleep(2)
        else:
            print('You are already following this User!!\n')

    
    def unfollow_user(self):
        
        time.sleep(2)

        unfollow_button = self.driver.find_elements_by_css_selector('button')[1]
        unfollow_button.click()
        time.sleep(1)
        confirmation_button = self.driver.find_elements_by_xpath('//button[text() = "Unfollow"]')[0]
        confirmation_button.click()

        time.sleep(4)
        # Get back to homePage
        self.driver.get('https://www.instagram.com/')


    def logout(self):
        self.nav_user(self.username)
        time.sleep(2)
        options_button = self.driver.find_elements_by_css_selector('button')[2]
        options_button.click()

        time.sleep(2)
        self.driver.find_elements_by_xpath('//button[text() = "Log Out"]')[0].click()


    def get_users_followers(self, user, maxfollowers):

        '''
            Args :
                user : (String) The username of the person to find their followers.
                maxfollowers : (Integer) The no. of followers to be fetched.

        '''
        self.nav_user(user)

        time.sleep(1)

        followers_link = self.driver.find_element_by_css_selector('ul li a')
        followers_link.click()

        time.sleep(2)
        followers_list = self.driver.find_element_by_css_selector('div[role = \'dialog\'] ul')
        number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))
        followers_list.click()

        action_chain = webdriver.ActionChains(self.driver)
        while number_of_followers_in_list < maxfollowers:
            action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))
            print(number_of_followers_in_list)
            followers_list.click()

        followers = []
        index_no = 0
        for users in followers_list.find_elements_by_css_selector('li'):
            userlink = self.driver.find_elements_by_css_selector('div[role = \'dialog\'] ul li a')[index_no].get_attribute('href')
            print('\n user link is : {}'.format(userlink))
            followers.append(userlink)
            index_no += 1
            if len(followers) == maxfollowers:
                break
        return followers


if __name__ == "__main__":
    ig_bot = InstagramBot('Your_Username', 'Your_Password')

    ig_bot.login()
    time.sleep(4)
    ig_bot.nav_user('wonderwoman')
    ig_bot.follow_user()
    time.sleep(4)
    ig_bot.nav_user('batman')
    ig_bot.follow_user()
    time.sleep(4)
    ig_bot.nav_user('wonderwoman')
    ig_bot.unfollow_user()
    print(ig_bot.get_users_followers('therock', 30))
    ig_bot.logout()
    
