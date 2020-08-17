import os,random,sys,subprocess,copy
import time,eel,ast
# from instabot import Bot,utils
# import multiprocessing,threading,logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import logging,os,time,json,requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

# xattr -d com.apple.quarantine chromedriver

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"

# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------

application_path = ''

class BOT:

    def __init__(
                    self,username,password,proxy,
                    TARGET_HASHTAGS,TARGET_ACCOUNTS_IF_ANY,
                    WANT_L,WANT_F,WANT_UNFOLLOW,WANT_DM,WANT_WHITLIST_FOLLOW,
                    dms,
                    following_file_path,
                    unfollow_after_x_days,white_list_users,
                    likes_per_hour,follows_per_hour,unfollows_per_hour,dms_per_hour,whitelist_follows_per_hour

                ):
        self.username,self.password,self.proxy = username,password,proxy
        self.target_hashtags,self.target_accounts = TARGET_HASHTAGS,TARGET_ACCOUNTS_IF_ANY
        self.WANT_L,self.WANT_F,self.WANT_UNFOLLOW,self.WANT_DM,self.WANT_WHITLIST_FOLLOW = WANT_L,WANT_F,WANT_UNFOLLOW,WANT_DM,WANT_WHITLIST_FOLLOW
        self.driver = None
        self.messages = dms
        self.operations = 0
        self.following_file_path = following_file_path
        self.unfollow_after_x_days = unfollow_after_x_days
        self.white_list_users = white_list_users
        self.likes_per_hour = likes_per_hour
        self.follows_per_hour = follows_per_hour
        self.unfollows_per_hour = unfollows_per_hour
        self.dms_per_hour = dms_per_hour
        self.whitelist_follows_per_hour = whitelist_follows_per_hour
        self.my_followings = []
        self.my_followers = []

    def get_driver(self):
        if bool(self.driver):
            return
        chrome_options = Options()
        chrome_options.add_argument("–lang= en")
        chrome_options.add_extension(os.path.join(application_path,'files','core','extension.crx'))
        # add proxy
        if self.proxy:
            pass
        
        # add profile path
        profile_path = os.path.join(application_path,'files','profiles',self.username.replace('@','').replace('.','')+"_profile")
        if not os.path.exists(profile_path):
            os.mkdir(profile_path)
        chrome_options.add_argument("user-data-dir={}".format(profile_path))
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_experimental_option("prefs",prefs) 

        # add chrome driver according to window
        if os.name == 'nt':
            chrome = os.path.join(application_path,'files','core','chromedriver.exe')
        else:
            chrome = os.path.join(application_path,'files','core','chromedriver')
        
        dr =  webdriver.Chrome(executable_path=chrome,options=chrome_options)
        return dr

    def login(self):
        print("\n[+] Trying TO login with username -> "+self.username)
        if not self.driver:self.driver = self.get_driver()
        self.driver.get("https://www.instagram.com/accounts/login/")
        el,st = 0,time.time()
        while 1:
            if el>15:break
            el = time.time()-st
            if self.driver.current_url == 'https://www.instagram.com':return True
            try:
                username_f = self.driver.find_element_by_xpath("//input[@name='username']")
                password_f = self.driver.find_element_by_xpath("//input[@name='password']")
                username_f.clear()
                password_f.clear()
                username_f.send_keys(self.username)
                time.sleep(1)
                password_f.send_keys(self.password)
                password_f.send_keys(Keys.RETURN)
                time.sleep(1)
                password_f.send_keys(Keys.RETURN)
                time.sleep(1)
                break
            except:
                pass
        el,st = 0,time.time()
        alert = ''
        while True:
            if el>15:break 
            try:
                self.driver.find_element_by_xpath("//*[text()='Not Now']").click()
            except:
                pass
            try:
                self.driver.find_element_by_xpath("//input[@placeholder='Search']")
                return True
            except:
                pass
            try:
                alert = self.driver.find_element_by_xpath("//p[@role='alert']").text.strip()
            except:
                pass
            try:
                if 'challenge' in self.driver.current_url:
                    alert = "Chalange completion required."
                    break
            except:
                pass
            if self.driver.current_url == 'https://www.instagram.com':return True
            
            el = time.time() - st
        try:
            self.driver.find_element_by_xpath("//*[text()='Not Now']").click()
            return True
        except:
            pass
        m = "\n[{}] " + alert
        print(m.format(self.username))
        return False

    def set_page(self):
        self.driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(5)

    def countdown(self,for_pause=False):
        if for_pause:
            print("\n[+] Bot Goes on Rest for 5 minutes.")
            time.sleep(5*60)
        else:
            self.driver.get("https://www.google.com/")
            included = []
            if self.WANT_F:included.append(self.follows_per_hour)
            if self.WANT_L:included.append(self.likes_per_hour)
            if self.WANT_DM:included.append(self.dms_per_hour)
            if self.WANT_WHITLIST_FOLLOW:included.append(self.whitelist_follows_per_hour)
            maximum_action = max(included)
            tym = 3600/maximum_action
            print('\n[{}] Sleep for {} seconds.'.format(self.username,tym))
            time.sleep(tym)

    def set_agant(self):
        print("[{}] Setting Agent.".format(self.username))
        self.driver.get("chrome-extension://mapkmdeokpfddaiojeekdhjjllaaaldm/popup.html")
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@id='add']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='addUaName']").send_keys("def")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='addUaValue']").send_keys(agent)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='addUaSubmit']").click()
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath("//*[text()='def']").click()
        except:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath("//*[text()='def']"))

        time.sleep(2)
        print("[{}] Agent Setting Done.".format(self.username))

    def set_default_agent(self):
        self.driver.get("chrome-extension://mapkmdeokpfddaiojeekdhjjllaaaldm/popup.html")
        time.sleep(1)
        while 1:
            try:
                self.driver.find_element_by_xpath("//*[text()='Default']").click()
                print("[{}] Agent Reset Done.".format(self.username))
                break
            except:
                pass

    def read_following_with_dates(self):
        try:
            file = open(self.following_file_path,'r')
        except:
            file = open(self.following_file_path,'w')
            file.close()
            return []
        my_following = []
        for line in file.readlines():
            line = line.strip()
            line = ast.literal_eval(line)
            my_following.append(line)
        return my_following

    def get_intruder_followings(self):
        following = self.read_following_with_dates()
        if not following:
            return
        intruders_folowing = []
        date_format = "%d/%m/%Y"
        today_date = datetime.strptime(datetime.today().strftime('%d/%m/%Y'), date_format)
        for foll in following:
            foll_date = foll['date']
            user_id = foll['user_id']
            foll_date = datetime.strptime(foll_date, date_format)
            delta = today_date - foll_date
            diff = delta.days
            if diff>=self.unfollow_after_x_days:
                intruders_folowing.append(user_id)
        return intruders_folowing

    def save_following_to_file(self, data):
        try:
            file = open(self.following_file_path,'a')
            data = str(data)
            file.write(data+"\n")
            file.close()
        except Exception as e:
            print(e)

    def update_following_file(self,foll_ids):
        all_foll = self.read_following_with_dates()
        try:
            file = open(self.following_file_path,'w')
            for foll in all_foll:
                if foll['user_id'] in foll_ids:
                    continue
                else:
                    data = str(foll)
                    file.write(data+"\n")
            file.close()
        except Exception as e:
            print(e)

    ################################################################################################
    ################################################################################################
    ################################################################################################

    def get_user_id(self,user):
        res = requests.get("https://www.instagram.com/{}?__a=1".format(user))
        data = res.text
        data = json.loads(data)
        ID = data.get('graphql').get('user').get('id')
        return ID

    def get_message(self):
        return self.messages[random.randint(0,len(self.messages)-1)]

    def get_hashtag_medias(self):
        all_data = []
        for hashtag in self.target_hashtags:
            print("[+] Fetching data from hashtags -> '{}' ".format(hashtag))
            hashtag = hashtag.replace('#','')
            self.driver.get("https://www.instagram.com/explore/tags/{}/?__a=1".format(hashtag))
            try:
                soup = BeautifulSoup(self.driver.page_source,features="html5lib")
                data = json.loads(soup.find("body").text)
                for media in data.get('graphql').get('hashtag').get('edge_hashtag_to_media').get('edges'):
                    for data in media:
                        all_data.append(media.get(data).get('shortcode'))
            except:
                print("[+] Fetching data from hashtag '{}' failed.".format(hashtag))
        return all_data

    def get_user_followers(self):
        self.driver.execute_script('''window.open("http://google.com","");''')
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.set_agant()
        ALL_DATA = []
        for target_user in self.target_accounts:
            print("[{}] Getting Followers of user {} ".format(self.username,target_user))
            ID = self.get_user_id(target_user)
            self.driver.get("https://i.instagram.com/api/v1/friendships/{}/followers".format(ID))
            soup = BeautifulSoup(self.driver.page_source,features="html5lib")
            data = json.loads(soup.find("body").text)
            for user in data.get('users'):
                ALL_DATA.append((user.get('pk'),user.get('username')))

        if not bool(self.my_followings):
            ID = self.get_user_id(self.username)
            url_1 = "https://i.instagram.com/api/v1/friendships/"+str(ID)+"/following/?max_id={}"
            next_max_id = 0
            all_following_data = []
            while True:
                self.driver.get(url_1.format(next_max_id))
                soup = BeautifulSoup(self.driver.page_source,features="html5lib")
                data = json.loads(soup.find("body").text)
                for user in data.get('users'):
                    all_following_data.append((user.get('pk'),user.get('username')))
                next_max_id = data.get('next_max_id')
                if not next_max_id:
                    break
            self.my_followings = copy.copy(all_following_data)

        if not bool(self.my_followers):
            ID = self.get_user_id(self.username)
            url_2 = "https://i.instagram.com/api/v1/friendships/"+str(ID)+"/followers/?next_max_id={}"
            next_max_id = 0
            all_followers_data = []
            while True:
                self.driver.get(url_2.format(next_max_id))
                soup = BeautifulSoup(self.driver.page_source,features="html5lib")
                data = json.loads(soup.find("body").text)
                for user in data.get('users'):
                    all_followers_data.append((user.get('pk'),user.get('username')))
                next_max_id = data.get('next_max_id')
                if not next_max_id:
                    break
            self.my_followers = copy.copy(all_followers_data)

        
        self.set_default_agent()
        time.sleep(2)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        for i in range(10):random.shuffle(ALL_DATA)
        return ALL_DATA

    def fetch_all_my_followings_followers(self):
        if not bool(self.my_followings) or not bool(self.my_followers):
            self.driver.execute_script('''window.open("http://google.com","");''')
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.set_agant()
            ID = self.get_user_id(self.username)
            url_1 = "https://i.instagram.com/api/v1/friendships/"+str(ID)+"/following/?max_id={}"
            next_max_id = 0
            all_following_data = []
            while True:
                self.driver.get(url_1.format(next_max_id))
                soup = BeautifulSoup(self.driver.page_source,features="html5lib")
                data = json.loads(soup.find("body").text)
                for user in data.get('users'):
                    all_following_data.append((user.get('pk'),user.get('username')))
                next_max_id = data.get('next_max_id')
                if not next_max_id:
                    break
            self.my_followings = copy.copy(all_following_data)

            url_2 = "https://i.instagram.com/api/v1/friendships/"+str(ID)+"/followers/?next_max_id={}"
            next_max_id = 0
            all_followers_data = []
            while True:
                self.driver.get(url_2.format(next_max_id))
                soup = BeautifulSoup(self.driver.page_source,features="html5lib")
                data = json.loads(soup.find("body").text)
                for user in data.get('users'):
                    all_followers_data.append((user.get('pk'),user.get('username')))
                next_max_id = data.get('next_max_id')
                if not next_max_id:
                    break
            self.my_followers = copy.copy(all_followers_data)

            self.set_default_agent()
            time.sleep(2)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            pass

    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################z

    def send_dm(self,user):
        self.driver.get("https://www.instagram.com/direct/new/")
        username = user
        msg = self.get_message()
        print("\n[{}] Sending Dm to User '{}' ".format(self.username,username))
        searhced_box = self.driver.find_element_by_xpath("//input[@placeholder='Search...']")
        searhced_box.send_keys(username)
        time.sleep(3)
        alls = self.driver.find_elements_by_xpath("//input[@placeholder='Search...']/parent::div/parent::div/parent::div/parent::div/div[2]/div")
        alls[0].click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[text()='Next']").click()
        while 1:
            try:
                self.driver.find_element_by_xpath("//textarea[@placeholder='Message...']")
                break
            except:
                pass
        self.driver.find_element_by_xpath("//textarea[@placeholder='Message...']").send_keys(msg)
        time.sleep(1)
        self.driver.find_element_by_xpath("//textarea[@placeholder='Message...']").send_keys(Keys.RETURN)
        print('[{}] Message Sent successfully.'.format(self.username))
        time.sleep(random.randint(5,20))
        # self.countdown()

    def follow(self,user):
        print("\n[+] Trying TO follow user -> "+user)
        today_date = datetime.today().strftime('%d/%m/%Y')
        self.driver.get("https://www.instagram.com/"+user)
        el,st = 0,time.time()
        while el<20:
            el = time.time() - st
            try:
                self.driver.find_element_by_xpath("//*[text()='Follow']").click()
                print("[+] User Followed Successfully.")
                one_data = {'user_id':user,'date':today_date}
                self.save_following_to_file(one_data)
                time.sleep(random.randint(10,20))
                return
            except:
                pass
        print("[+] User Followed Failed.")
            
    def like(self,link):
        print("\n[+] Trying TO Like Post -> "+link)
        self.driver.get(link)
        el,st = 0,time.time()
        while el<20:
            el = time.time() - st
            try:
                self.driver.find_element_by_xpath("((//section)[2]//button)[1]").click()
                print("[+] Post Liked Successfully.")
                self.save_me(link,os.path.join(os.getcwd(),'files','core','HASHTAGS_LINK_DONE.txt'))
                time.sleep(random.randint(10,20))
                return
            except:
                pass
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='Unlike']")
                print("[+] Post is Already liked.")
                return
            except:
                pass
        print("[+] Post Liked Failed/or it is deleted.")

    def check_time_and_stuck(self):
        current_datetime = datetime.now()
        if current_datetime.hour>=9 and current_datetime.hour<22:
            return False
        else:
            print("\n[+] Today Sleep time reaches, Going to sleep.")
            self.driver.quit()
            while datetime.now().hour >= 22 or (datetime.now().hour>=0 and datetime.now().hour<=8):
                pass
            print("[+] SLEEEPING END..... ")
            print("\n[+] STARTING ACTIVITY AGAIN........... ")
            time.sleep(5)
            self.driver = self.get_driver()
            self.operations = 0
            return True

    def read_saved(self,fileName):
        data = []
        try:
            file = open(fileName,'r')
            for line in file.readlines():
                data.append(line.strip())
            file.close()
            return data
        except:
            file = open(fileName,'w')
            file.close()
            return data

    def save_me(self,data,fileName):
        try:
            file = open(fileName,'a')
        except:
            file = open(fileName,'w')
        file.write(data+"\n")
        file.close()

    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################

    def UNFOLLOW_NON_FOLLOWERS(self):
        int_foll = self.get_intruder_followings()
        if bool(int_foll):
            print("\n[~~~]  ->  UNFOLLOW USER WHICH NOT FOLLOW ME AFTER X Days  <-   [~~~~]")
            for foll in int_foll:
                print('\n[+] Unfollowing User -> '+foll)
                
                if foll in self.white_list_users:
                    print("[+] User {} Found in White List, so Bot skipping this user.".format(foll))
                    time.sleep(10)
                    continue

                self.driver.get("https://www.instagram.com/"+foll)
                el,st = 0,time.time()
                unfollow_done = False
                while el<20:
                    el = time.time() - st
                    try:
                        self.driver.find_element_by_xpath("(//span//span/button)[1]").click()
                        time.sleep(4)
                        self.driver.find_element_by_xpath("//*[text()='Unfollow']").click()
                        unfollow_done = True
                        break
                    except:
                        pass
                if unfollow_done:
                    print("[+] Unfollow User '{}' Successfully.  ".format(foll))
                    self.update_following_file([foll])
                    print("[+] Sleep for 30 sec.")
                    time.sleep(random.randint(20,50))
                else:
                    print("[+] User Not Unfollowed :(")
                    time.sleep(random.randint(20,25))
        else:
            return
        print("\n[~~~]  ->  UNFOLLOWING END  <-   [~~~~]\n")

    def execute_main(self,all_hashtag_medias,all_followers):
        res = False
        follow_f_done = 0
        whitelist_follow_f_done = 0
        like_f_done = 0
        dm_f_done = 0
        start_time,elapsed_time = time.time(),0
        index_for_white_list_user = 0
        self.operations = 0

        if len(all_hashtag_medias) > len(all_followers) and bool(all_hashtag_medias) and bool(all_followers): 
            print("\n[info] if-1 one executing ...")
            all_hashtag_medias = all_hashtag_medias[:len(all_followers)]

            for i in range(len(all_hashtag_medias)):
                done_any_thing = False

                res = self.check_time_and_stuck()
                if res:
                    break

                if elapsed_time>3600:
                    elapsed_time = 0
                    start_time = time.time()
                    like_f_done = 0
                    whitelist_follow_f_done = 0
                    follow_f_done = 0
                    dm_f_done = 0

                if self.operations!=0 and self.operations%10 == 0:
                    self.driver.quit()
                    self.countdown(for_pause=True)
                    self.driver = self.get_driver()
                    # time.sleep(10)
                    self.login()

                if i!=0 and i%2==0 and index_for_white_list_user<len(self.white_list_users) and elapsed_time<3600 and whitelist_follow_f_done<self.whitelist_follows_per_hour:
                    if not self.white_list_users[index_for_white_list_user] in self.read_saved(os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt')):
                        if self.white_list_users[index_for_white_list_user] in [user[1] for user in self.my_followings]:
                            pass
                        else:
                            self.follow(self.white_list_users[index_for_white_list_user])
                            self.save_me(self.white_list_users[index_for_white_list_user],os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt'))
                            whitelist_follow_f_done+=1
                            done_any_thing = True

                        index_for_white_list_user+=1                

                ##### like hashtag post #####
                if elapsed_time<3600 and like_f_done < self.likes_per_hour and self.WANT_L:
                    link = all_hashtag_medias[i]
                    link = 'https://instagram.com/p/'+link
                    print("\n[+] Current link -> "+link)

                    if link in self.read_saved(os.path.join(os.getcwd(),'files','core','HASHTAGS_LINK_DONE.txt')):
                        print('[+] this link is already done.')
                        # time.sleep(5)
                    else:
                        self.like(link)
                        done_any_thing = True
                        like_f_done+=1


                ##### actions on followers of person #####
                owner = all_followers[i][1]

                if owner in self.read_saved(os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt')) or owner in [user[1] for user in self.my_followings]:
                    print('[+] User "{}" is already done.'.format(owner))
                    # time.sleep(5)
                else:
                    ## send dm to follower
                    if self.WANT_DM and elapsed_time<3600 and dm_f_done<self.dms_per_hour:
                        self.send_dm(owner)
                        done_any_thing = True
                        dm_f_done+=1

                    ## Follow follower
                    if self.WANT_F and elapsed_time<3600 and follow_f_done<=self.follows_per_hour:
                        self.follow(owner)
                        done_any_thing = True
                        follow_f_done+=1
                    
                    self.save_me(owner,os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt'))

                if done_any_thing:
                    self.operations+=1
                    self.countdown()

                elapsed_time = time.time() - start_time
            
        elif len(all_followers) > len(all_hashtag_medias) and bool(all_hashtag_medias) and bool(all_followers):
            print("\n[info] if-2 one executing ...")

            all_followers = all_followers[:len(all_hashtag_medias)]

            for i in range(len(all_hashtag_medias)):
                done_any_thing = False

                res = self.check_time_and_stuck()
                if res:
                    break

                if elapsed_time>3600:
                    elapsed_time = 0
                    start_time = time.time()
                    like_f_done = 0
                    whitelist_follow_f_done = 0
                    follow_f_done = 0
                    dm_f_done = 0

                if self.operations!=0 and self.operations%10 == 0:
                    self.driver.quit()
                    self.countdown(for_pause=True)
                    self.driver = self.get_driver()
                    time.sleep(10)
                    self.login()

                if i!=0 and i%2==0 and index_for_white_list_user<len(self.white_list_users) and elapsed_time<3600 and whitelist_follow_f_done<self.whitelist_follows_per_hour:
                    if not self.white_list_users[index_for_white_list_user] in self.read_saved(os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt')):
                        if self.white_list_users[index_for_white_list_user] in [user[1] for user in self.my_followings]:
                            pass
                        else:
                            self.follow(self.white_list_users[index_for_white_list_user])
                            self.save_me(self.white_list_users[index_for_white_list_user],os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt'))
                            whitelist_follow_f_done+=1
                            done_any_thing = True
                        index_for_white_list_user+=1                


                ##### like hashtag post #####
                if elapsed_time<3600 and like_f_done < self.likes_per_hour and self.WANT_L:
                    link = all_hashtag_medias[i]
                    link = 'https://instagram.com/p/'+link
                    print("[+] Current link -> "+link)

                    if link in self.read_saved(os.path.join(os.getcwd(),'files','core','HASHTAGS_LINK_DONE.txt')):
                        print('[+] this link is already done.')
                    else:
                        self.like(link)
                        done_any_thing = True
                        like_f_done+=1


                ##### actions on followers of person #####
                owner = all_followers[i][1]

                if owner in self.read_saved(os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt')) or owner in [user[1] for user in self.my_followings]:
                    print('[+] User "{}" is already done.'.format(owner))
                else:
                    ## send dm to follower
                    if self.WANT_DM and elapsed_time<3600 and dm_f_done<self.dms_per_hour:
                        self.send_dm(owner)
                        done_any_thing = True
                        dm_f_done+=1

                    ## Follow follower
                    if self.WANT_F and elapsed_time<3600 and follow_f_done<=self.follows_per_hour:
                        self.follow(owner)
                        done_any_thing = True
                        follow_f_done+=1
                    
                    self.save_me(owner,os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt'))

                # self.operations+=1
                if done_any_thing:
                    self.operations+=1
                    self.countdown()

                elapsed_time = time.time() - start_time
            
        elif (not bool(all_hashtag_medias)) and bool(all_followers):
            print("\n[info] if-3 one executing ...")

            for i in range(len(all_followers)):
                
                done_any_thing = False

                res = self.check_time_and_stuck()
                if res:
                    break

                if elapsed_time>3600:
                    elapsed_time = 0
                    start_time = time.time()
                    like_f_done = 0
                    whitelist_follow_f_done = 0
                    follow_f_done = 0
                    dm_f_done = 0

                if self.operations!=0 and self.operations%10 == 0:
                    self.driver.quit()
                    self.countdown(for_pause=True)
                    self.driver = self.get_driver()
                    time.sleep(10)
                    self.login()

                if i!=0 and i%2==0 and index_for_white_list_user<len(self.white_list_users) and elapsed_time<3600 and whitelist_follow_f_done<self.whitelist_follows_per_hour:
                    if not self.white_list_users[index_for_white_list_user] in self.read_saved(os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt')):
                        if self.white_list_users[index_for_white_list_user] in [user[1] for user in self.my_followings]:
                            print("[+] This person is already followed")
                        else:
                            self.follow(self.white_list_users[index_for_white_list_user])
                            self.save_me(self.white_list_users[index_for_white_list_user],os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt'))
                            done_any_thing = True
                            whitelist_follow_f_done+=1
                        index_for_white_list_user+=1                

                ##### actions on followers of person #####
                owner = all_followers[i][1]

                if owner in self.read_saved(os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt')) or owner in [user[1] for user in self.my_followings]:
                    print('[+] User "{}" is already done.'.format(owner))
                else:
                    ## send dm to follower
                    if self.WANT_DM and elapsed_time<3600 and dm_f_done<self.dms_per_hour:
                        self.send_dm(owner)
                        done_any_thing = True
                        dm_f_done+=1

                    ## Follow follower
                    if self.WANT_F and elapsed_time<3600 and follow_f_done<self.follows_per_hour:
                        self.follow(owner)
                        done_any_thing = True
                        follow_f_done+=1
                    
                    self.save_me(owner,os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt'))

                if done_any_thing:
                    self.operations+=1
                    self.countdown()

                elapsed_time = time.time() - start_time
            
        elif (not bool(all_followers)) and bool(all_hashtag_medias):
            print("\n[info] if-4 one executing ...")

            for i in range(len(all_hashtag_medias)):
                done_any_thing = False
                res = self.check_time_and_stuck()
                if res:
                    break

                if elapsed_time>3600:
                    elapsed_time = 0
                    start_time = time.time()
                    like_f_done = 0
                    whitelist_follow_f_done = 0
                    follow_f_done = 0
                    dm_f_done = 0

                if self.operations!=0 and self.operations%10 == 0:
                    self.driver.quit()
                    self.countdown(for_pause=True)
                    self.driver = self.get_driver()
                    time.sleep(10)
                    self.login()

                if i!=0 and i%2==0 and index_for_white_list_user<len(self.white_list_users) and elapsed_time<3600 and whitelist_follow_f_done<self.whitelist_follows_per_hour:
                    if not self.white_list_users[index_for_white_list_user] in self.read_saved(os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt')):
                        if self.white_list_users[index_for_white_list_user] in [user[1] for user in self.my_followings]:
                            print("[+] This person is already followed")
                        else:
                            self.follow(self.white_list_users[index_for_white_list_user])
                            self.save_me(self.white_list_users[index_for_white_list_user],os.path.join(os.getcwd(),'files','core','USER_FOLLOWERS_DONE.txt'))
                            whitelist_follow_f_done+=1
                            done_any_thing = True
                        index_for_white_list_user+=1                

                #### like hashtag post #####
                if elapsed_time<3600 and like_f_done < self.likes_per_hour and self.WANT_L:
                    link = all_hashtag_medias[i]
                    link = 'https://instagram.com/p/'+link
                    # print("\n[+] Current link -> "+link)

                    if link in self.read_saved(os.path.join(os.getcwd(),'files','core','HASHTAGS_LINK_DONE.txt')):
                        print('[+] this link is already done.')
                        # time.sleep(5)
                    else:
                        self.like(link)
                        done_any_thing = True
                        like_f_done+=1

                # time.sleep(1)
                if done_any_thing:
                    self.operations+=1
                    self.countdown()

                elapsed_time = time.time() - start_time
       
        else:
            print("\n[info] if-5 one executing ...")

        return res

    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################

    def bot_driver(self):
        if not bool(self.username) or not bool(self.password):
            print("[{}] Username/Password is missing in 'input.json' file.".format(self.username))
            return

        while 1:

            if self.login():
                print("[{}] Login Succeed.".format(self.username))
                print("")
                
                self.UNFOLLOW_NON_FOLLOWERS()

                ### get_hashtags medias
                if self.WANT_L:
                    all_hashtag_medias = self.get_hashtag_medias()
                else:      
                    all_hashtag_medias = []

                # ### get userfollowers
                if self.WANT_DM or self.WANT_F:
                    all_followers = self.get_user_followers()
                else:
                    all_followers = []

                self.fetch_all_my_followings_followers()

                res = self.execute_main(all_hashtag_medias,all_followers)

                if res:continue
                else:
                    try:
                        self.driver.quit()
                    except:pass
                    self.countdown(for_pause=True)
                    self.driver = self.get_driver()
            else:
                print("\n[{}] Login Failed.".format(self.username))
                break

# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------

comment_file = os.path.join(application_path,'files','COMMENTS.txt')
dm_file = os.path.join(application_path,'files','DMS.txt')

def readFile(file_path):
    try:
        file = open(file_path,'r')
    except:
        file = open(file_path,'w')
        file.close()
        print("[+] '{}' is empty ".format(file_path))
        return []
    data = []
    for line in file.readlines():
        data.append(line.strip())
    return data

def main(username, password, target_hashtags, target_usernames, mode, like, follow, unfollow, dm, whitelist_follow, unfollow_after_x_days, white_list_users, likes_per_hour, follows_per_hour, unfollows_per_hour, dms_per_hour, whitelist_follows_per_hour):

    following_file_path = os.path.join(application_path,'files',username+"_.txt")
    dms = readFile(dm_file)
    if (not dms and dm):
        print("\n\n[+] 'DMS.txt' is empty, Fill the comments and then try again")
        while 1:continue
        return

    # TARGET_HASHTAGS = [h.strip() for h in target_hashtags.strip().split(',')]
    # TARGET_ACCOUNTS_IF_ANY = target_usernames.strip().split(',')
    # white_list_users = white_list_users.split(',')

    TARGET_HASHTAGS = [h.strip() for h in target_hashtags.strip().split(',')]
    TARGET_ACCOUNTS_IF_ANY = [u.strip() for u in target_usernames.strip().split(',')]
    white_list_users = [w.strip() for w in white_list_users.strip().split(',')]



    WANT_L = like
    WANT_DM = dm
    WANT_F = follow
    WANT_UNFOLLOW = unfollow
    WANT_WHITLIST_FOLLOW = whitelist_follow


    bot = BOT(
                username,password,None,
                TARGET_HASHTAGS,TARGET_ACCOUNTS_IF_ANY,
                WANT_L,WANT_F,WANT_UNFOLLOW,WANT_DM,WANT_WHITLIST_FOLLOW,
                dms,
                following_file_path,
                unfollow_after_x_days,white_list_users,
                likes_per_hour,follows_per_hour,unfollows_per_hour,dms_per_hour,whitelist_follows_per_hour
            )

    bot.bot_driver()


# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------


prefs = os.path.join(application_path,'files','core','prefs.txt')

def save_me(username, password, target_hashtags, target_usernames, mode, like, follow, unfollow, dms, whitelist_follow, unfollow_after_x_days, white_list_users, likes_per_hour, follows_per_hour, unfollows_per_hour, dms_per_hour, whitelist_follows_per_hour):
    try:
        file = open(prefs,'w')
        file.write(str({
                        'username':username,
                        'password':password,
                        'target_hashtags':target_hashtags,
                        'target_usernames':target_usernames,
                        'mode':mode,
                        'like':like,
                        'follow':follow,
                        'unfollow':unfollow,
                        'dms':dms,
                        'whitelist_follow':whitelist_follow,
                        'follows_per_hour':follows_per_hour,
                        'unfollows_per_hour':unfollows_per_hour,
                        'likes_per_hour':likes_per_hour,
                        'dms_per_hour':dms_per_hour,
                        'unfollow_after_x_days':unfollow_after_x_days,
                        'whitelist_follows_per_hour':whitelist_follows_per_hour,
                        'white_list_users':white_list_users
                    })+"\n")
        file.close()
    except Exception as e:
        print(e)

@eel.expose
def get_save():
    try:
        file = open(prefs,'r')
        return ast.literal_eval(file.readline().strip())
    except:
        open(prefs,'w').close()
        return None

@eel.expose
def START_BOT(username, password, target_hashtags, target_usernames, mode, like, follow, unfollow, dms, whitelist_follow, unfollow_after_x_days, white_list_users, likes_per_hour, follows_per_hour, unfollows_per_hour, dms_per_hour, whitelist_follows_per_hour):
    save_me(username, password, target_hashtags, target_usernames, mode, like, follow, unfollow, dms, whitelist_follow, unfollow_after_x_days, white_list_users, likes_per_hour, follows_per_hour, unfollows_per_hour, dms_per_hour, whitelist_follows_per_hour)
    main(username, password, target_hashtags, target_usernames, mode, like, follow, unfollow, dms, whitelist_follow, unfollow_after_x_days, white_list_users, likes_per_hour, follows_per_hour, unfollows_per_hour, dms_per_hour, whitelist_follows_per_hour)
    # main(username, password, data, mode, like, follow, unfollow, dms)

@eel.expose
def set_comments():
    commentFile = os.path.join(application_path,'files','COMMENTS.txt')
    try:
        file = open(commentFile,'r') 
        file.close()
    except:
        file = open(commentFile,'w') 
        file.write("ONE COMMENT PER LINE.")
        file.close()
        
    if sys.platform == "win32":
        os.system('"{}" notepad.exe'.format(commentFile))
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, commentFile])

@eel.expose
def set_dms():
    dmsFile = os.path.join(application_path,'files','DMS.txt')
    try:
        file = open(dmsFile,'r') 
        file.close()
    except:
        file = open(dmsFile,'w') 
        file.write("ONE DM PER LINE.")
        file.close()
        
    if sys.platform == "win32":
        os.system('"{}" notepad.exe'.format(dmsFile))
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, dmsFile])

def onExit(x,y):
    pass

def main_main():
    eel.init('web')
    eel.start('index.html',port=random.randint(100,4000),size=(2000, 2000),close_callback=onExit(1,2))
    while True:
        eel.sleep(20)

def check_and_make():
    # if not os.path.exists(os.path.join(application_path,'config')):
    #     os.mkdir(os.path.join(application_path,'config'))
    # if not os.path.exists(os.path.join(application_path,'logs')):
    #     os.mkdir(os.path.join(application_path,'logs'))
    # if not os.path.exists(os.path.join(application_path,'logs','log')):
    #     os.mkdir(os.path.join(application_path,'logs','log'))
    if not os.path.exists(os.path.join(application_path,'files')):
        os.mkdir(os.path.join(application_path,'files'))
    if not os.path.exists(os.path.join(application_path,'files','core')):
        os.mkdir(os.path.join(application_path,'files','core'))
    if not os.path.exists(os.path.join(application_path,'files','profiles')):
        os.mkdir(os.path.join(application_path,'files','profiles'))

    

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        running_mode = 'Frozen/executable'
    else:
        try:
            app_full_path = os.path.realpath(__file__)
            application_path = os.path.dirname(app_full_path)
            running_mode = "Non-interactive (e.g. 'python myapp.py')"
        except NameError:
            application_path = application_path
            running_mode = 'Interactive'

    sys.stdout.flush()
    check_and_make()
    main_main()
    print("\n\n[][][][][][][][][][][][][][][][][][][][][][][]")
    print("[][][][][]       EXECUTION END      [][][][][]")
    print("[][][][][][][][][][][][][][][][][][][][][][][]\n\n")
    while 1:continue