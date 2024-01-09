import requests
from bs4 import BeautifulSoup as soup
from lxml import etree
from time import sleep
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


def check_results(indexNumber, name):
    url = "https://results.knec.ac.ke/Home/CheckResults"
    payload = {
        "indexNumber": indexNumber,
        "name": name
    }

    # Sending a POST request with the payload data
    s = requests.post(url, data=payload)

    # Check if the request was successful before parsing
    if s.status_code == 200:
        # Parse the response content using Beautiful Soup and 'lxml' parser
        page = soup(s.content, 'html.parser')
        body = page.find("body")

        dom = etree.HTML(str(body)) # Parse the HTML content of the page
        xpath_str = '//*[@class="text-center"]' # The XPath expression for the blog's title
        name_index_num = dom.xpath(xpath_str)[0].text
        school = dom.xpath(xpath_str)[1].text
        mean_grade = dom.xpath(f"{xpath_str}/span[2]")[0].text

        resp_data = {
            "name":name_index_num,
            "school":school,
            "mean_grade":mean_grade
        }
    else:
        resp_data = f"Failed to fetch data"

    return resp_data


results = check_results("28500006081","ROONEY OKUTA")
print(results)