#TODO: Add support for non Windows operating systems
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
import os
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from lxml import html
import requests


class UpdateChromeDriver(object):


    def __init__(self):

        self.download_latest_chromedriver()


    def identify_latest_chromedriver(self):
        """
        Identifies from the Chromedriver website which version in the most recent stable release
        and returns the download url for the windows 32 bit version
        """
        page = requests.get('https://chromedriver.chromium.org/')
        webpage = html.fromstring(page.content)
        links = [x for x in webpage.xpath('//a/@href') if "storage.googleapis" in x]
        links.pop(1)
        win32  = (str(links[0]) + 'chromedriver_win32.zip').replace('index.html?path=', '')

        return win32


    def download_latest_chromedriver(self):

        try:
            driver = webdriver.Chrome()
            #driver.get("https://www.google.com/")
            driver.close()
            driver.quit()
        except SessionNotCreatedException:

            zipurl = self.identify_latest_chromedriver()
            with urlopen(zipurl) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(f'{os.getcwd()}')
