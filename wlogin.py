import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your bot token and chat ID
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
YOUR_CHAT_ID = os.environ['YOUR_CHAT_ID']

LOGIN_URL = "https://www.tesmanian.com/account/login"

# Replace with your email and password
EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']


def send_to_telegram(message):

    apiURL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

    try:
        response = requests.post(
            apiURL, json={'chat_id': YOUR_CHAT_ID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def login(driver):
    driver.get(LOGIN_URL)

    email_input = driver.find_element('name', "customer[email]")
    password_input = driver.find_element('name', "customer[password]")
    submit_button = driver.find_element('xpath', "//button[@type='submit']")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    submit_button.click()


def get_titles_and_links(driver):
    url = "https://www.tesmanian.com/"
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'blog-post-card')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('blog-post-card')

    titles_links = []

    for article in articles:
        title_element = article.find('p')
        link_element = title_element.find('a')
        title = title_element.text
        link = url + link_element['href']
        titles_links.append((title, link))

    return titles_links


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sent_links = set()

        while True:
            try:
                titles_links = get_titles_and_links(driver)[::-1]

                # Filter out already sent articles
                new_titles_links = [
                    item for item in titles_links if item[1] not in sent_links]

                for title, link in new_titles_links:
                    message = f"{title}\n{link}"
                    send_to_telegram(message)

                # Update the set of sent links
                sent_links.update([link for _, link in new_titles_links])

                time.sleep(15)  # Scrape every 15 seconds

            except NoSuchElementException:
                print("Unauthorized error encountered. Re-logging in.")
                login(driver)


if __name__ == "__main__":
    main()
