import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TwitterManualMode:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.FWD = webdriver.Firefox()  # FWD = Firefox Web Driver
        self.FWD.set_page_load_timeout(5)
        self.FWD.get("https://twitter.com/")
        time.sleep(2)

    @staticmethod
    def str_to_int(val: str) -> int:
        total_stars = 0
        num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        if val.isdigit():
            total_stars = int(val)
        else:
            if len(val) > 1:
                total_stars = float(val[:-1]) * num_map.get(val[-1].upper(), 1)
        return int(total_stars)

    def log_in_on_twitter(self) -> None:
        required_url = "https://twitter.com/i/flow/login"
        self.FWD.get(required_url)
        if self.FWD.current_url != required_url:
            Exception("Invalid Window Location")

        email_input = self.FWD.find_element(by=By.XPATH,
                                            value="//input[@autocomplete='username']")
        email_input.clear()
        email_input.send_keys(self.username)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)
        pass_input = self.FWD.find_element(by=By.XPATH,
                                           value="//input[@autocomplete='current-password']")
        pass_input.clear()
        pass_input.send_keys(self.password)
        pass_input.send_keys(Keys.RETURN)
        time.sleep(self.FWD.timeouts.page_load)

    def follow_user(self, username: str, min_followers: int = 0, max_followers: int = sys.maxsize,
                    min_following: int = 0, max_following: int = sys.maxsize) -> tuple[bool, str]:
        redirect_url = f"https://twitter.com/{username}"
        self.FWD.get(redirect_url)
        try:
            followers_elem = self.FWD.find_element(by=By.XPATH,
                                                   value=f"//a[@href='/{username}/followers']/span[1]/span")
            following_elem = self.FWD.find_element(by=By.XPATH,
                                                   value=f"//a[@href='/{username}/following']/span[1]/span")
        except NoSuchElementException:
            return False, "Invalid Username"
        followers_count = self.str_to_int(followers_elem.get_attribute('innerHTML'))
        following_count = self.str_to_int(following_elem.get_attribute('innerHTML'))

        if min_followers <= followers_count <= max_followers and min_following <= following_count <= max_following:
            try:
                follow_button = self.FWD.find_element(by=By.XPATH,
                                                      value=f"//div[@aria-label='Follow @{username}' "
                                                            "and ./div/span/span[text()='Follow']]")
                follow_button.click()
                time.sleep(1)
                return True, "Success"
            except NoSuchElementException:
                return False, "Already Following"
        else:
            return False, "User doesn't satisfy the constrains"
