from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
import os


class InstagramAutomation():

    #TODO: Differentiate between pictures, gifs and video and amend sleep times accordingly

    def __init__(self, username, password, hashtag_list, number_of_posts):

        self.username = username
        self.password = password
        self.hashtag_list = hashtag_list
        self.number_of_posts = int(number_of_posts)
        self.chromedriver_path = f'{os.getcwd()}/chromedriver.exe'
        self.webdriver = webdriver.Chrome(executable_path=self.chromedriver_path)

        self.instagram_likes_and_follows()




    def instagram_login(self):
        """
        Handles login to instagram and returns the webdriver for use downstream
        """

        webdriver = self.webdriver
        sleep(2)
        webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        sleep(3)

        try:
            allow_cookies = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.bIiDR')
            allow_cookies.click()
        except:
            pass
        sleep(3)

        username = webdriver.find_element_by_name('username')
        username.send_keys(self.username)
        password = webdriver.find_element_by_name('password')
        password.send_keys(self.password)

        button_login = webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
        button_login.click()
        sleep(3)

        return webdriver


    def instagram_likes_and_follows(self):

        webdriver = self.instagram_login()

        hashtag_list = self.hashtag_list

        # If the log file doesn't exist, likely on first run then instantiate an empty list for use
        # Otherwise use the log from previous runs
        if os.path.exists(f'{os.getcwd()}/users_followed_list.csv'):
            prev_user_list = pd.read_csv(f'{os.getcwd()}/users_followed_list.csv', delimiter=',')  # useful to build a user log
            prev_user_list = list(prev_user_list['Usernames'])

        else:
            prev_user_list = []

        
        new_followed = []
        tag = -1
        followed = 0
        likes = 0
        comments = 0

        for hashtag in hashtag_list:
            tag += 1
            webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
            sleep(5)
            first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
            
            first_thumbnail.click()
            sleep(randint(1,2))    
          #  try:        
            for x in range(1,self.number_of_posts):
                #username = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/h2/div/span/a').text
                username = webdriver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.e1e1d > span > a').text

                if username not in prev_user_list:
                    # If we already follow, do not unfollow
                    if webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                        
                        webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                        
                        new_followed.append(username)
                        followed += 1

                        # Liking the picture
                        button_like = webdriver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > div > span > svg')
                        button_like.click()
                        likes += 1
                        sleep(randint(10,17))

                        # Comments and tracker
                        comm_prob = randint(1,10)
                        print('{}_{}: {}'.format(hashtag, x,comm_prob))
                        if comm_prob > 7:
                            comments += 1
                            webdriver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span._15y0l > button > div > svg').click()
                            comment_box = webdriver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea')

                            if (comm_prob < 7):
                                comment_box.send_keys('Really cool!')
                                sleep(1)
                            elif (comm_prob > 6) and (comm_prob < 9):
                                comment_box.send_keys('Nice work :)')
                                sleep(1)
                            elif comm_prob == 9:
                                comment_box.send_keys('Nice gallery!!')
                                sleep(1)
                            elif comm_prob == 10:
                                comment_box.send_keys('So cool! :)')
                                sleep(1)
                            # Enter to post comment
                            comment_box.send_keys(Keys.ENTER)
                            sleep(randint(14,20))

                    # Next picture
                    webdriver.find_element_by_link_text('Next').click()
                    sleep(randint(17,21))
                else:
                    webdriver.find_element_by_link_text('Next').click()
                    sleep(randint(12,18))
            # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
            #except:
            #    continue

        for n in new_followed:
            prev_user_list.append(n)
            
        updated_user_df = pd.DataFrame(prev_user_list, columns=['Usernames'])
        updated_user_df.to_csv(f'{os.getcwd()}/users_followed_list.csv', index=False)
        print(f'Liked {likes} photos.')
        print(f'Commented {comments} photos.')
        print(f'Followed {followed} new people.')
