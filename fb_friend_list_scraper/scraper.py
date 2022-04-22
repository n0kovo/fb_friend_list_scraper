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
from sys import argv, stdout
from time import sleep

import pyautogecko
from os import system
from bs4 import BeautifulSoup
from rich import box, print
from rich.console import Console
from rich.progress import Progress, track
from rich.rule import Rule
from rich.table import Table
from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def logprint(text):
    text = f"[cyan][+][/cyan] [blue]{text}[/blue]"
    console.print(text)
    

console = Console()


def print_banner():
    credits = "[blue][italic]by narkopolo[/italic][/blue]"
    version = "[blue][italic]v0.3.3[/italic][/blue]"
    lol = "[grey30](banners are cool, shut up)[/grey30]"
    banner = f"""    ______    ____     _                _____      __                                      
   / __/ /_  / __/____(_)__  ____  ____/ / (_)____/ /____________________  ____  ___  _____
  / /_/ __ \/ /_/ ___/ / _ \/ __ \/ __  / / / ___/ __/ ___/ ___/ ___/ __ `/ __ \/ _ \/ ___/
 / __/ /_/ / __/ /  / /  __/ / / / /_/ / / (__  ) /_(__  ) /__/ /  / /_/ / /_/ /  __/ /    
/_/ /_.___/_/ /_/  /_/\___/_/ /_/\__,_/_/_/____/\__/____/\___/_/   \__,_/ .___/\___/_/      
{lol}                                     {version} /_/ {credits}                 

"""
    for i, line in enumerate(banner.splitlines()):
        if i == 0:
            line = line.replace("_", "[white]_[/white]")
        if i == 1:
            line = line.replace("/_", "/[white]_[/white]")
            line = line.replace("__", "[white]__[/white]")
            line = line.replace("_ ", "[white]_ [/white]")
            line = line.replace("_", "[white]_[/white]")
        
        if i in [0, 1, 4, 5]:
            console.print(line, style="red", highlight=False)
        elif i == 3:
            console.print(line, style="cyan", highlight=False)
        else:
            console.print(line, style="blue", highlight=False)



def parse_proxy(proxy_string):
    proxy_user = ""
    proxy_pass = ""
    
    if proxy_string.startswith(("http://", "socks5://")) == False:
        parser.error("Invalid schema for --proxy. Must be https or socks5.")
        return False
    
    proxy_schema = "".join(proxy_string.partition("://")[:2])
    proxy_type = proxy_schema.replace("://", "")
    proxy_port = proxy_string.replace(proxy_schema, "").split(":")[-1]
    if "@" in proxy_string:
        before_at, proxy_host = proxy_string.split("@")
        proxy_user = before_at.replace(proxy_schema, "")
        if ":" in proxy_user:
            proxy_user, proxy_pass = proxy_user.split(":")
    else:
        proxy_host = proxy_string.replace(proxy_schema, "")
    
    return {"user": proxy_user,
            "pass": proxy_pass,
            "type": proxy_schema,
            "host": proxy_host,
            "port": int(proxy_port)}



def change_language(driver):
    logprint("Non-english detected. Changing language to English (UK)")
    driver.get("https://m.facebook.com/language/")
    try:
        english_btn = driver.find_element(By.XPATH, '//*[@value="English (UK)"]')
    except NoSuchElementException:
        english_btn = driver.find_element(By.XPATH, '//*[@value="en_gb"]')
    english_btn.click()


def login(driver, email, password):
    logprint("Requesting login page")
    driver.get("https://m.facebook.com/login")

    forgot_pw = driver.find_element(By.XPATH, '//*[@id="forgot-password-link"]')
    if forgot_pw.text != 'Forgotten password?':
        change_language(driver)

    try:
        cookie_btn = driver.find_element(By.XPATH, '//*[@value="Only Allow Essential Cookies"]')
    except NoSuchElementException:
        cookie_btn = driver.find_element(By.XPATH,'//*[@value="Only allow essential cookies"]',)
        cookie_btn.click()

    email_input = driver.find_element(By.XPATH, '//*[@id="m_login_email"]')
    email_input.send_keys(email)
    password_input = driver.find_element(By.XPATH, '//*[@id="m_login_password"]')
    password_input.send_keys(password)
    login_btn = driver.find_element(By.XPATH,'//*[@value="Log In"]',)
    logprint("Submitting login form")
    login_btn.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_changes("https://m.facebook.com/login"))


def get_total_friends(driver, user_to_scrape):
    logprint("Getting total friends count")
    driver.get(f"https://m.facebook.com/{user_to_scrape}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    friends_count_div = soup.find("div", class_="_7-1j")
    friends_count_text = friends_count_div.get_text()
    
    # Remove mutual friends string if present
    friends_count_text = friends_count_text.split("(")[0]
    friends_count = re.sub(r'\D', '', friends_count_text)

    logprint(f"Friends count = {friends_count}")
    return int(friends_count)


def scrape_profiles(driver, outfile_path, progress, args):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profiles = soup.find_all("div", class_="_84l2")
    scraped_profiles = []
    
    table = Table(show_header=True, show_edge=True, box=box.DOUBLE, expand=False, highlight=True, header_style="bold magenta")
    table.add_column("Name", style="dim")
    table.add_column("Profile URL")

    for div in profiles:
        username = div.find("a")["href"][1:].replace("profile.php?id=", "")
        link = f"https://www.fb.com/{username}"
        name = div.get_text()
        
        if args.onlyusernames:
            profilestring = username
        else:
            profilestring = f"{name} ({link})"

        with open(outfile_path, "a+") as outfile:
            outfile.write(f"{profilestring}\n")

        table.add_row(f"[bold]{name}[/bold]", link)
    
    if not args.quiet:
        progress.console.print(table)


def remove_visible(driver, progress):
    logprint("Removing scraped elements from page")
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


def cleanup(driver, progress):

    logprint("Cleaning up leftover elements")
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

    logprint("Waiting a bit...")
    sleep(5)


def scroll_down(driver, progress):
    logprint("Scrolling to the bottom")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def wait(range_start, range_stop, progress):
    wait_time = randint(range_start, range_stop)
    minutes = "%d.%d" % (wait_time / 60, wait_time % 60)
    waitbar = progress.add_task(f"[green]Waiting {minutes} minutes", total=wait_time * 5)
    progress.update(waitbar, advance=0)
    
    progress.console.print("")
    for second in range(wait_time * 5):
        sleep(0.2)
        progress.advance(waitbar)
    progress.update(waitbar, visible=False)
    progress.console.print("")


def do_scrape(driver, email, password, user_to_scrape, outfile_path, args):
    progress = Progress(console=console)
    
    with progress.console.status("[bold magenta]Logging in...") as status:
        login(driver, email, password)
        
    with progress:
        total_friends = get_total_friends(driver, user_to_scrape)
        logprint("Requesting friends page")
        driver.get(f"https://m.facebook.com/{user_to_scrape}/friends")
        logprint("Starting...\n")
        
        pbar = progress.add_task("[blue]Total progress", total=total_friends)
        progress.update(pbar, advance=0)

        total_pages = ceil(total_friends / 36)
        for i, page in enumerate(range(total_pages)):
            progress.console.print(Rule(title=f"Scraping page {i+1} of {total_pages}"))
            progress.update(pbar, advance=24)
            scrape_profiles(driver, outfile_path, progress, args)
            sleep_multiplier = args.sleepmultiplier
            
            if args.cmd:
                logprint(f"Executing command: '{args.cmd}'")
                logprint(f"Command exited with status code '{system(args.cmd)}'")
                
            wait(240*sleep_multiplier, 320*sleep_multiplier, progress)
            scroll_down(driver, progress)
            remove_visible(driver, progress)
            cleanup(driver, progress)


def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        prog='fbfriendlistscraper',
        description='Tool to scrape names and usernames from large friend lists on Facebook, without being rate limited',
        epilog=f"""examples:
        fbfriendlistscraper -e your@email.com -p YourPassword123 -u someusername.123 -o my_file.txt
        fbfriendlistscraper --email your@email.com --username another.user --headless -s 2 -x
        fbfriendlistscraper -e your@email.com -u username.johnson -w --proxy socks5://127.0.0.1:9050 --cmd "killall -HUP tor"
        fbfriendlistscraper -e your@email.com -u xxuserxx --headless --cmd "mullvad relay set provider Quadranet"
        """, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-e', '--email', action="store", required=True, help='Email address to login with.')
    parser.add_argument('-p', '--password', action="store", help='Password to login with. If not supplied you will be prompted. You really shouldn\'t use this for security reasons.')
    parser.add_argument('-u', '--username', action="store", required=True, help='Username of the user to scrape.')
    parser.add_argument('-o', '--outfile', action="store", default="./scraped_friends.txt", help='Path of the output file. (Default: ./scraped_friends.txt)')
    parser.add_argument('-w', '--headless', action='store_true', help='Run webdriver in headless mode.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Do not print scraped users to screen.')
    parser.add_argument('-x', '--onlyusernames', action='store_true', help='Only the usernames/IDs will be written to the output file.')
    parser.add_argument('-s', '--sleepmultiplier', action='store', default=1, type=int, help='Multiply sleep time between each page scrape by n. Useful when being easily rate-limited.')
    parser.add_argument('-i', '--proxy', action="store", help='Proxy server to use for connecting. Username/password can be supplied like: socks5://user:pass@host:port')
    parser.add_argument('-c', '--cmd', action="store", help='Shell command to run after each page scrape. Useful for changing proxy/VPN exit.')
    args = parser.parse_args()
    
    email = args.email
    user_to_scrape = args.username
    outfile_path = args.outfile
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt=f'Password for {args.email}: ')
        print("")

    if args.proxy:
        logprint(f"Proxy set to '{args.proxy}'")
        seleniumwire_options = {
        'proxy': {
            'http': args.proxy,
            'https': args.proxy,
            'no_proxy': 'localhost,127.0.0.1'
            }
        }
    
    logprint("Starting webdriver")
        
    firefox_options = Options()
    pyautogecko.install()
    
    if args.headless:
        firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options, seleniumwire_options=seleniumwire_options)

    do_scrape(driver, email, password, user_to_scrape, outfile_path, args)


if __name__ == "__main__":
    main()
