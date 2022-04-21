#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import getpass
import re
from math import ceil
from random import randint
from time import sleep

import pyautogecko
from bs4 import BeautifulSoup
from sys import argv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


def change_language(driver):
    print("[+] Non-english detected. Changing language to English (UK)")
    driver.get("https://m.facebook.com/language/")
    try:
        english_btn = driver.find_element(By.XPATH, '//*[@value="English (UK)"]')
    except NoSuchElementException:
        english_btn = driver.find_element(By.XPATH, '//*[@value="en_gb"]')
    english_btn.click()


def login(driver, email, password):
    print("[+] Requesting login page")
    driver.get("https://m.facebook.com/login")

    forgot_pw = driver.find_element(By.XPATH, '//*[@id="forgot-password-link"]')
    if forgot_pw.text != 'Forgotten password?':
        change_language(driver)
    
    try:
        cookie_btn = driver.find_element(By.XPATH, '//*[@value="Only Allow Essential Cookies"]')
        cookie_btn.click()
    except NoSuchElementException:
        pass

    email_input = driver.find_element(By.XPATH, '//*[@id="m_login_email"]')
    email_input.send_keys(email)
    password_input = driver.find_element(By.XPATH, '//*[@id="m_login_password"]')
    password_input.send_keys(password)
    login_btn = driver.find_element(By.XPATH,'//*[@value="Log In"]',)
    print("[+] Logging in")
    login_btn.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_changes("https://m.facebook.com/login"))


def get_total_friends(driver, user_to_scrape):
    print("[+] Getting total friends count")
    driver.get(f"https://m.facebook.com/{user_to_scrape}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    friends_count_div = soup.find("div", class_="_7-1j")
    friends_count = re.sub(r'\D', '', friends_count_div.get_text())

    print(f"[+] Friends count = {friends_count}")
    return int(friends_count)


def scrape_profiles(driver, outfile_path, pbar=None):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profiles = soup.find_all("div", class_="_84l2")
    scraped_profiles = []

    with open(outfile_path, "a+") as outfile:
        for div in profiles:
            link = div.find("a")["href"][1:].replace("profile.php?id=", "")
            link = f"https://www.fb.com/{link}"
            name = div.get_text()
            profilestring = f"{name} ({link})"
            scraped_profiles.append(profilestring)
            outfile.write(f"{profilestring}\n")
    if pbar:
        for profile in scraped_profiles:
            pbar.write(profile)
        pbar.write


def remove_visible(driver, pbar=None):
    if pbar:
        pbar.write("[+] Removing scraped elements from page")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profile_classes = soup.find_all("div", class_="_7om2")
    for i in profile_classes[:-1]:
        driver.execute_script(
            """
        var element = document.querySelector("._7om2");
        if (element)
            element.parentNode.removeChild(element);
        """
        )


def cleanup(driver, pbar=None):
    if pbar:
        pbar.write("[+] Cleaning up leftover elements\n")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profile_slots = soup.find_all("div", class_="_55wp _5909 _5pxa _8yo0")

    element = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[4]/div/div[1]/div[1]"
    )
    driver.execute_script(
        """
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """,
        element,
    )

    for slot in profile_slots:

        element = driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[4]/div/div[1]/div[1]/div[1]"
        )
        driver.execute_script(
            """
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """,
            element,
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        first_remaining_slot = soup.find("div", class_="_55wp _5909 _5pxa _8yo0")
        try:
            has_child = len(first_remaining_slot.find_all()) != 0
        except AttributeError:
            break

        if has_child:
            break
    if pbar:
        pbar.write("Waiting a bit...")
    sleep(10)


def scroll_down(driver, pbar=None):
    if pbar:
        pbar.write("[+] Scrolling to the bottom")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def wait(range_start, range_stop):
    wait_time = randint(range_start, range_stop)

    minutes = "%d.%d" % (wait_time / 60, wait_time % 60)
    l_bar_ = f"Waiting {minutes} minutes: {{percentage:3.0f}}%|"
    r_bar_ = "[{remaining}]"
    wait_bar_format = f"{l_bar_}{{bar}}{r_bar_}"

    with tqdm(total=wait_time * 5, bar_format=wait_bar_format) as waitbar:
        waitbar.write("")
        for second in range(wait_time * 5):
            sleep(0.2)
            waitbar.update(1)
    waitbar.write("")


def do_scrape(driver, email, password, user_to_scrape, outfile_path):
    login(driver, email, password)
    total_friends = get_total_friends(driver, user_to_scrape)
    print("[+] Requesting friends page")
    driver.get(f"https://m.facebook.com/{user_to_scrape}/friends")
    print("[+] Starting...\n")

    pbar = tqdm(total=total_friends)
    pbar.display()
    pbar.set_description("Total progress")

    total_pages = ceil(total_friends / 36)
    for i, page in enumerate(range(total_pages)):
        pbar.write(f"------------ Scraping page {i+1} of {total_pages}: ------------\n")
        scrape_profiles(driver, outfile_path, pbar)
        pbar.update(24)
        wait(240, 320)
        scroll_down(driver, pbar)
        remove_visible(driver, pbar)
        cleanup(driver, pbar)


def main():
    parser = argparse.ArgumentParser(
        description='Tool to scrape names and usernames from large friend lists on Facebook, without being rate limited',
        epilog=f"""examples:
        fbfriendlistscraper -e your@email.com -p YourPassword123 -u someusername.123 -o my_file.txt
        fbfriendlistscraper --email your@email.com --username another.user --headless""", formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-e', '--email', action="store", required=True, help='Email address to login with.')
    parser.add_argument('-p', '--password', action="store", help='Password to login with. If not supplied you will be prompted.')
    parser.add_argument('-u', '--username', action="store", required=True, help='Username of the user to scrape.')
    parser.add_argument('-o', '--outfile', action="store", default="./scraped_friends.txt", help='Path of the output file. (Default: ./scraped_friends.txt)')
    parser.add_argument('-q', '--headless', action='store_true', help='Run webdriver in headless mode.')

    args = parser.parse_args()



    email = args.email
    user_to_scrape = args.username
    outfile_path = args.outfile
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt=f'Password for {args.email}: ')
    
    firefox_options = Options()
    pyautogecko.install()
    
    if args.headless:
        firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)

    do_scrape(driver, email, password, user_to_scrape, outfile_path)


if __name__ == "__main__":
    main()
