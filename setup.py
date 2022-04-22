from setuptools import setup
from sys import argv, exit
import glob
import os


with open('README.md') as readme_file:
    long_description = readme_file.read()


# 'setup.py publish' shortcut.
if argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    exit()
elif argv[-1] == 'clean':
    import shutil
    if os.path.isdir('build'):
        shutil.rmtree('build')
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    if os.path.isdir('fb_friend_list_scraper.egg-info'):
        shutil.rmtree('fb_friend_list_scraper.egg-info')


setup(
    name="fb_friend_list_scraper",
    version="0.3.3",
    description="Tool to scrape names and usernames from large friend lists on Facebook, without being rate limited.",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="https://github.com/narkopolo/fb_friend_list_scraper",
    author="narkopolo",
    author_email="narkopolo@riseup.net",
    license="GPL-3.0",
    packages=["fb_friend_list_scraper"],
    entry_points={
        "console_scripts": ["fbfriendlistscraper=fb_friend_list_scraper.scraper:main"],
    },
    python_requires=">=3.6",
    install_requires=[
        "pyautogecko==0.1.3",
        "beautifulsoup4==4.10.0",
        "selenium==4.1.3",
        "tqdm==4.43.0",
        "rich==12.2.0"
        "selenium-wire==4.6.3"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Topic :: System :: Installation/Setup',
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
