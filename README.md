<img src="https://user-images.githubusercontent.com/16690056/181832615-30f5d44d-307a-4c3d-9cb0-c31fbef1b15c.png">

<p float="left">
<img src="https://img.shields.io/badge/Built%20with-Python3-red" />
<img src="https://img.shields.io/badge/Version-0.3.6-green" /> 
<img src="https://img.shields.io/pypi/dm/fb-friend-list-scraper.svg" />
<a href="https://makeapullrequest.com/"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square&color=green" /></a>
</p>

## Facebook Friend List Scraper

OSINT tool to scrape names and usernames from large friend lists on Facebook, without being rate limited.

### Getting started:
* Install using pip: `python -m pip install fb-friend-list-scraper`
* Script is now installed as `fbfriendlistscraper`
* Run with `-h` or `--help` to show usage information.

### Usage:

```
usage: fbfriendlistscraper [-h] -e EMAIL [-p PASSWORD] -u USERNAME [-o OUTFILE] [-w] [-q] [-x] [-s SLEEPMULTIPLIER] [-i PROXY] [-c CMD]

Tool to scrape names and usernames from large friend lists on Facebook, without being rate limited

options:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        Email address or phone number to login with.
  -p PASSWORD, --password PASSWORD
                        Password to login with. If not supplied you will be prompted. You really shouldn't use this for security reasons.
  -u USERNAME, --username USERNAME
                        Username of the user to scrape.
  -o OUTFILE, --outfile OUTFILE
                        Path of the output file. (Default: ./scraped_friends.txt)
  -w, --headless        Run webdriver in headless mode.
  -q, --quiet           Do not print scraped users to screen.
  -x, --onlyusernames   Only the usernames/IDs will be written to the output file.
  -s SLEEPMULTIPLIER, --sleepmultiplier SLEEPMULTIPLIER
                        Multiply sleep time between each page scrape by n. Useful when being easily rate-limited.
  -i PROXY, --proxy PROXY
                        Proxy server to use for connecting. Username/password can be supplied like: socks5://user:pass@host:port
  -c CMD, --cmd CMD     Shell command to run after each page scrape. Useful for changing proxy/VPN exit.

examples:
        fbfriendlistscraper -e your@email.com -p YourPassword123 -u someusername.123 -o my_file.txt
        fbfriendlistscraper --email your@email.com --username another.user --headless -s 2 -x
        fbfriendlistscraper -e your@email.com -u username.johnson -w --proxy socks5://127.0.0.1:9050
        fbfriendlistscraper -e your@email.com -u xxuserxx --headless --cmd "mullvad relay set provider Quadranet"
        fbfriendlistscraper -e your@email.com -u markzuckerburger -w -o ./test.txt --cmd "killall -HUP tor"
```

### NOTE:
Facebook changes the markup of it's pages regularly, so the script might break from time to time. Please open an issue if something doesn't work and I'll take a look at it. Pull requests are welcome as well.


### TODO:
* Make script check for followers if friend list isn't public.
* Add more error handling.
* Add proxy rotation.