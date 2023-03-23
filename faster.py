import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your bot token and chat ID
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
YOUR_CHAT_ID = os.environ['YOUR_CHAT_ID']


def send_to_telegram(message):

    apiURL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

    try:
        response = requests.post(
            apiURL, json={'chat_id': YOUR_CHAT_ID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def login(session):
    login_url = "https://www.tesmanian.com/account/login"

    payload = {
        'email': os.environ['EMAIL'],
        'password': os.environ['PASSWORD'],
    }

    session.post(login_url, data=payload)


def get_titles_and_links(session):
    url = "https://www.tesmanian.com/"
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

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
    with requests.Session() as session:
        login(session)
        sent_links = set()

        while True:
            titles_links = get_titles_and_links(session)[::-1]

            # Filter out already sent articles
            new_titles_links = [
                item for item in titles_links if item[1] not in sent_links]

            for title, link in new_titles_links:
                message = f"{title}\n{link}"
                send_to_telegram(message)

            # Update the set of sent links
            sent_links.update([link for _, link in new_titles_links])

            time.sleep(15)  # Scrape every 15 seconds


if __name__ == "__main__":
    main()
