from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, strftime, localtime
from decouple import config
import os
import create_post
from pywinauto.application import Application
import shutil
import random
import schedule
from webdriver_manager.chrome import ChromeDriverManager

PWD = config('PWD')
USER = config('USER')
IMAGE = os.getcwd() + r'\images\final.jpg'
HASHTAGS = f"#{config('USER')} #quotes #quote #quoteoftheday #quotestoliveby #quotestagram #quotesoftheday #quotesdaily #quotesaboutlife #quotestags #quotesgram #quotesofinstagram #quotesandsayings #quotesforlife #quoted #quotegram #quotez #quotekillahs #quoteoftheweek #quoteofday #QuotesForYou #quotetoliveby #quoteslife #quotesaboutlifequotesandsayings #quotesvn #quotesoflife #quoteslove #quoteofthenight #quotesaboutlove #quotess"


class Instagram:
    def __init__(self):
        self.mobile_emulation = {
            "deviceMetrics": {"width": 411, "height": 731, "pixelRatio": 3.0},
            "userAgent": f"{config('USER_AGENT')}"}
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--auto-open-devtools-for-tabs")
        self.options.add_experimental_option(
            "mobileEmulation", self.mobile_emulation)

        # set chromedriver download path to .wdm folder
        os.environ['WDM_LOCAL'] = '1'
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=self.options)

        self.driver.get("https://instagram.com")
        try:
            log_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(text(), 'Log In')]"))
            )
        except:
            self.driver.quit()
            exit()
        log_btn.click()
        sleep(1)
        self.driver.find_element_by_xpath(
            '//input[@name="username"]').send_keys(USER)
        self.driver.find_element_by_xpath(
            '//input[@name="password"]').send_keys(PWD)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(6)
        self.driver.find_element_by_xpath(
            '//button[contains(text(), "Not Now")]').click()
        sleep(2)
        self.driver.find_element_by_xpath(
            '//button[contains(text(), "Cancel")]').click()
        sleep(2)
        self.driver.execute_script("window.scrollTo(0, 60);")
        try:
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
        except:
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

    def search(self, search_term):
        self.driver.find_element_by_xpath('//a[@href="/explore/"]').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//label[@class="NcCcD"]'))).click()
        self.driver.find_element_by_xpath(
            '//input[@placeholder="Search"]').send_keys(search_term)

    def home(self):
        self.driver.get("https://instagram.com")

    def activity(self):
        self.driver.get("https://instagram.com/accounts/activity/")
        top = random.randint(180, 900)
        self.driver.execute_script(
            f'window.scrollTo({{left: 0, top: {top}, behavior: "smooth"}});')

    def profile(self):
        self.driver.get(f"https://instagram.com/{USER}")
        top = random.randint(10, 100)
        self.driver.execute_script(
            f'window.scrollTo({{left: 0, top: {top}, behavior: "smooth"}});')

    def profile_num_followers(self):
        num_followers = self.driver.find_element_by_xpath(
            '//li[2]/a/span').get_attribute('title')
        num_followers = num_followers.replace(',', '')
        return int(num_followers)

    def profile_num_following(self):
        num_following = self.driver.find_element_by_xpath(
            '//li[3]/a/span').text
        num_following = num_following.replace(',', '')
        return int(num_following)

    def newpost(self):
        self.driver.refresh()
        sleep(2)
        print(strftime("[%Y-%m-%d %H:%M:%S]", localtime()) +
              ' - Publishing New Post...')
        # Create image post
        post_content = create_post.build_image_post()

        self.driver.find_element_by_xpath(
            '//div[@data-testid="new-post-button"]').click()
        sleep(3)

        upload_dialog = Application().connect(title_re='Open')
        upload_dialog.Open.Edit.type_keys(IMAGE)
        sleep(5)
        # upload_dialog.Open.Button.click()
        upload_dialog.window(title_re='Open').Open.click()
        sleep(5)
        self.driver.find_element_by_xpath(
            '//button[contains(text(), "Next")]').click()
        sleep(2)
        self.driver.find_element_by_xpath(
            '//textarea[@aria-label="Write a caption…"]').send_keys(post_content + '\n\n' + HASHTAGS)
        self.driver.find_element_by_xpath(
            '//button[contains(text(), "Share")]').click()
        # delete images folder
        shutil.rmtree(os.getcwd()+'/images', ignore_errors=True)

    def discover_people(self, follow_max=11, has_max_followers=15000, has_min_followers=450, follow_ratio=2):
        print(strftime("[%Y-%m-%d %H:%M:%S]", localtime()) +
              ' - Following Profiles...')
        self.profile()
        self.driver.refresh()
        sleep(2)
        self.driver.execute_script('window.scrollTo(0,0)')
        self.driver.find_element_by_xpath('//button[@class="wpO6b "]').click()
        sleep(2)
        # lazy loading scroll entire page
        check_height = self.driver.execute_script(
            "return document.body.scrollHeight;")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            height = self.driver.execute_script(
                "return document.body.scrollHeight;")
            if height == check_height:
                break
            check_height = height

        # find all user elements with links
        users = self.driver.find_elements_by_xpath('//main[@role="main"]')
        links = users[0].find_elements_by_tag_name("a")
        profile_links = [link.get_attribute("href") for link in links]
        # remove duplicates
        profile_links = list(set(profile_links))
        count_followings = 0
        for p in profile_links:
            if count_followings == follow_max:
                self.home()
                break
            self.driver.get(p)
            sleep(2)
            try:
                num_followers = self.profile_num_followers()
                num_following = self.profile_num_following()
                if has_min_followers < num_followers < has_max_followers or num_following/num_followers > follow_ratio:
                    follow_button = self.driver.find_element_by_xpath(
                        '//button[text()="Follow"]')
                    if follow_button:
                        follow_button.click()
                        sleep(1)
                        count_followings += 1
            except:
                pass
        print(f'Followed {count_followings} Profile(s)')
        self.profile()

    def scroll_list(self):
        # lazy loading scroll entire page
        check_height = self.driver.execute_script(
            "return document.body.scrollHeight;")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(4)
            height = self.driver.execute_script(
                "return document.body.scrollHeight;")
            if height == check_height:
                break
            check_height = height
        # find all user elements with links
        users = self.driver.find_elements_by_tag_name('ul')
        links = users[0].find_elements_by_tag_name("a")
        profiles_list = [link.get_attribute("href") for link in links]
        # remove duplicates
        profiles_list = list(set(profiles_list))
        return profiles_list

    def get_following(self):
        self.profile()
        sleep(5)
        self.driver.execute_script('window.scrollTo(0,0)')
        self.driver.find_element_by_xpath('//a[text()=" following"]').click()
        following = self.scroll_list()
        return following

    def get_followers(self):
        self.profile()
        sleep(5)
        self.driver.execute_script('window.scrollTo(0,0)')
        self.driver.find_element_by_xpath('//a[text()=" followers"]').click()
        followers = self.scroll_list()
        return followers

    def unfollow(self, unfollow=12):
        self.driver.refresh()
        sleep(2)
        print(strftime("[%Y-%m-%d %H:%M:%S]", localtime()) +
              ' - Unfollowing non-followers...')
        sleep(3)
        following = self.get_following()
        followers = self.get_followers()
        not_following_back = list(set(following) - set(followers))

        if len(not_following_back) > unfollow:
            unfollowers = unfollow
        else:
            unfollowers = len(not_following_back)

        self.profile()
        sleep(2)
        count_unfollowers = 0

        # go to your following list
        self.driver.find_element_by_xpath('//a[text()=" following"]').click()
        for i in range(unfollowers):
            sleep(4)
            self.driver.get(not_following_back[i])
            sleep(2)
            # random scrolling profile page
            top = random.randint(450, 850)
            self.driver.execute_script(
                f'window.scrollTo({{left: 0, top: {top}, behavior: "smooth"}});')
            sleep(3)
            self.driver.execute_script(
                f'window.scrollTo({{left: 0, top: 0, behavior: "smooth"}});')
            sleep(2)
            profile_page_unfollow = self.driver.find_element_by_xpath(
                '//span[@aria-label="Following"]')
            sleep(2)
            profile_page_unfollow.click()
            self.driver.find_element_by_xpath(
                '//button[text()="Unfollow"]').click()
            count_unfollowers += 1
            sleep(2)
            # back to following list
            self.driver.find_element_by_xpath('//a[@class=" Iazdo"]').click()
        self.profile()
        print(f'Unfollowed {count_unfollowers} profile(s)')

    def explore_like_follow(self, explore_times=3, to_follow=True):
        self.driver.refresh()
        sleep(2)
        self.profile()
        print(strftime("[%Y-%m-%d %H:%M:%S]", localtime()) +
              ' - Like & Follow Profiles...')
        self.driver.find_element_by_xpath('//a[@href="/explore/"]').click()
        sleep(5)
        to_refresh = 0
        for _ in range(explore_times):
            self.driver.execute_script('window.scrollTo(0,0)')
            # how many feeds to browse to like
            top = random.randint(800, 1250)
            sleep(5)
            self.driver.execute_script(
                f'window.scrollTo({{left: 0, top: {top}, behavior: "smooth"}});')
            image_feed = self.driver.find_elements_by_xpath(
                '//div[@class="pKKVh"]')
            sleep(4)
            r_pick = random.randint(0, 9)
            try:
                image_feed[r_pick].click()
                sleep(2)
                self.driver.find_element_by_xpath(
                    '//span[1]/button[@class="wpO6b "]').click()
                sleep(1)
                print('Explore - Liked Image!')
                to_refresh += 1
                if to_follow:
                    follow_profiles = self.driver.find_elements_by_xpath(
                        '//button[text()="Follow"]')
                    # how many to follow on page
                    f = random.randint(1, 4)
                    for i in range(f):
                        try:
                            follow_profiles[i].click()
                            print('Explore - Followed Profile!')
                        except:
                            pass
                sleep(2)
                # back to explore page
                self.driver.find_element_by_xpath(
                    '//a[@href="/explore/"]').click()
            except:
                pass
            if to_refresh > 3:
                self.driver.refresh()


if __name__ == "__main__":
    bot = Instagram()

    schedule.every(4).to(5).hours.do(bot.newpost)
    schedule.every(45).to(80).minutes.do(
        bot.explore_like_follow, random.randint(6, 11))
    schedule.every(80).to(130).minutes.do(bot.discover_people,
                                          random.randint(17, 35), 15000, 65)
    schedule.every(3).to(4).hours.do(bot.unfollow, random.randint(18, 28))

    while True:
        schedule.run_pending()
        sleep(1)
