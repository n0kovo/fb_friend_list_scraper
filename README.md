# Facebook Friend List Scraper
Tool to scrape names and usernames from large friend lists on Facebook, without being rate limited.

### Getting started:
* Install using pip: `python -m pip install fb-friend-list-scraper`
* Script is now installed as `fbfriendlistscraper`
* Run with `-h` or `--help` to show usage information.

### Usage:
```
usage: fbfriendlistscraper [-h] -e EMAIL [-p PASSWORD] -u USERNAME [-o OUTFILE] [-q]

Tool to scrape names and usernames from large friend lists on Facebook, without being rate limited

options:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        Email address to login with.
  -p PASSWORD, --password PASSWORD
                        Password to login with. If not supplied you will be prompted.
  -u USERNAME, --username USERNAME
                        Username of the user to scrape.
  -o OUTFILE, --outfile OUTFILE
                        Path of the output file. (Default: ./scraped_friends.txt)
  -q, --headless        Run webdriver in headless mode.

Examples:
        fbfriendlistscraper -e your@email.com -p YourPassword123 -u someusername.123 -o my_file.txt
        fbfriendlistscraper --email your@email.com --username another.user --headless
```

### NOTE:
Facebook changes the markup of it's pages regularly, so the script might break from time to time. Please open an issue if something doesn't work and I'll take a look at it. Pull requests are welcome as well.
