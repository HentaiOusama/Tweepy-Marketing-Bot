import os
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TwitterManualMode:
    def __init__(self, firefox_profile_path: str = "",
                 username: str = str(os.environ.get("twitterUsername")),
                 password: str = str(os.environ.get("twitterPassword"))):
        self.username = username
        self.password = password
        self.shouldFollowUsers = True
        self.shouldTagUsers = True
        if firefox_profile_path == "":
            self.FWD = webdriver.Firefox()
        else:
            self.FWD = webdriver.Firefox(firefox_profile=firefox_profile_path)  # FWD = Firefox Web Driver
        self.FWD.set_page_load_timeout(7.5)

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
        time.sleep(5)
        pass_input = self.FWD.find_element(by=By.XPATH,
                                           value="//input[@autocomplete='current-password']")
        pass_input.clear()
        pass_input.send_keys(self.password)
        pass_input.send_keys(Keys.RETURN)
        time.sleep(self.FWD.timeouts.page_load)

    # Not used, but it is an alternative.
    def click_follow_button(self, button_x_path: str) -> bool:
        return self.FWD.execute_script(script="let getElementByXpath = (path) => {return document.evaluate(path, "
                                              "document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, "
                                              "null).singleNodeValue;}; try {getElementByXpath(\"" + button_x_path +
                                              "\").click(); return true;} catch {return false;}")

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
                return True, "Success"
            except NoSuchElementException:
                return False, "Already Following"
        else:
            return False, "User doesn't satisfy the constrains"

    def bulk_follow_users(self, min_followers: int = 0, max_followers: int = sys.maxsize, min_following: int = 0,
                          max_following: int = sys.maxsize, max_iteration: int = sys.maxsize, end_time: float = 0):
        if not self.shouldFollowUsers:
            return
        elif end_time == 0:
            end_time = time.time() + (23 * 60 * 60)

        i = 0
        input_file = open("TwitterHelper/FilesForManualMode/Input/ToFollowList.txt", "r")
        output_file = open("TwitterHelper/FilesForManualMode/Output/FollowedList.txt", "a")

        for username in input_file:
            if (time.time() >= end_time) or (not self.shouldFollowUsers):
                return
            username = username.strip()
            if username != "":
                success, message = self.follow_user(username=username, min_followers=min_followers,
                                                    max_followers=max_followers, min_following=min_following,
                                                    max_following=max_following)
                print_msg = f"{username} {success} {message}"
                output_file.write(print_msg + "\n")
                output_file.flush()
                print(print_msg)
                i += 1
            else:
                break
            if i >= max_iteration:
                break
            time.sleep(50)

        print("Processed all follow usernames in Input File")
        output_file.close()
        input_file.close()

    def create_new_tweet(self, tweet_message: str):
        try:
            try:
                self.FWD.find_element(by=By.XPATH,
                                      value="//div[@class='css-1dbjc4n r-11z020y r-1p0dtai r-1d2f490 r-1xcajam "
                                            "r-zchlnj r-ipm5af']")
                print("Existing Modal Overlay Detected")
            except NoSuchElementException:
                tweet_button = self.FWD.find_element(by=By.XPATH,
                                                     value="//a[@href='/compose/tweet' and @aria-label='Tweet']")
                tweet_button.click()
                time.sleep(3)

            tweet_input = self.FWD.find_element(by=By.XPATH,
                                                value="//div[@aria-labelledby='modal-header']//*/div["
                                                      "@aria-label='Tweet text' and @role='textbox' and "
                                                      "@class='notranslate public-DraftEditor-content']")

            tweet_input.send_keys(tweet_message)
            tweet_button = self.FWD.find_element(by=By.XPATH,
                                                 value="//div[@data-testid='toolBar']/div/div["
                                                       "@data-testid='tweetButton']")
            tweet_button.click()
            return True, "Success"
        except NoSuchElementException as err:
            print(err)
            return False, "Selenium Error"

    def bulk_tag_users(self, base_message: str, max_len: int, should_prepend: bool = True,
                       max_iteration: int = sys.maxsize, end_time: float = 0):
        if not self.shouldTagUsers:
            return
        elif end_time == 0:
            end_time = time.time() + (23 * 60 * 60)

        input_file = open("TwitterHelper/FilesForManualMode/Input/ToTagList.txt", "r")
        output_file = open("TwitterHelper/FilesForManualMode/Output/TaggedList.txt", "a")
        self.FWD.get("https://twitter.com")

        current_message = f"\n{base_message}" if should_prepend else f"{base_message}\n"
        current_length = len(base_message)
        current_users = []
        i = 0
        for username in input_file:
            if (time.time() >= end_time) or (not self.shouldTagUsers):
                return

            username = username.strip()
            selected_username = f"@{username} "
            selected_length = len(selected_username)
            if (current_length + selected_length) < max_len:
                current_message = f"{selected_username}{current_message}" if should_prepend \
                    else f"{current_message}{selected_username}"
                current_length += selected_length
                current_users.append(username)
            else:
                success, message = self.create_new_tweet(tweet_message=current_message)
                print_text = f"{current_users} {success} {message}"
                print(print_text)
                output_file.write(f"{print_text}\n")
                output_file.flush()
                time.sleep(72)
                current_message = f"{selected_username}\n{base_message}" if should_prepend \
                    else f"{base_message}\n{selected_username}"
                current_length = len(base_message)
                current_users = [username]

            if i >= max_iteration:
                break

        if len(current_message) > (len(base_message) + 1):
            success, message = self.create_new_tweet(tweet_message=current_message)
            print_text = f"{current_users} {success} {message}"
            print(print_text)
            output_file.write(f"{print_text}\n")

        print("Processed all tag usernames in Input File")
        output_file.close()
        input_file.close()
