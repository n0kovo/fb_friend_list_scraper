# Facebook Friend List Scraper
Tool to scrape names and usernames from large friend lists on Facebook, without being rate limited.

### Getting started:
* Clone repo: `git clone https://github.com/narkopolo/fb_friend_list_scraper.git`
* Enter directory: `cd fb_friend_list_scraper`
* Install requirements:
`python -m pip install -r requirements.txt`
* Edit the following variables in `scraper.py` and save:
```python
email = "YOUR_EMAIL_HERE"
password = "YOUR_PASSWORD_HERE"
user_to_scrape = "USERNAME_TO_SCRAPE_HERE"
outfile_path = "./scraped_friends.txt"
```
* Run script: `python scraper.py`

### NOTE:
Facebook changes it's source code regularly, so the script might break from time to time. Please open an issue if something doesn't work and I'll take a look at it. Pull requests are welcome as well.
