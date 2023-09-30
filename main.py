import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import pandas as pd

from sqlalchemy import create_engine

import socketserver
from http.server import SimpleHTTPRequestHandler

import os.path

SCRAPED_PAGES_COUNT = 25

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

def show_page():
    """
    This function displays the page with saved advertisements at the required address.
    """
    class MyRequestHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/sreality_page.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    handler = MyRequestHandler
    server = socketserver.TCPServer((SERVER_HOST, SERVER_PORT), handler)
    server.serve_forever()

def get_advertisements_count(df):
    """
    This function returns the number of advertisements stored in the database.
    """
    return df.count()['Titles']

def create_row(soup, title, image):
    """
    This function creates an HTML tag with the row
    containing title and image  of the current advertisement.
    """
    row = soup.new_tag('tr')
    row.append(title)
    row.append(image)
    return row

def get_image_column_tag(soup, df, idx):
    """
    This function creates an HTML tag
    with the image of the current advertisement.
    """
    image_tag = soup.new_tag('img', src=df['Images URL'][idx])
    image_column_tag = soup.new_tag('td')
    image_column_tag.append(image_tag)
    return image_column_tag

def get_title_tag(soup, df, idx):
    """
    This function creates an HTML tag
    with the title of the current advertisement.
    """
    title_tag = soup.new_tag('td')
    title_tag.string = df['Titles'][idx]
    return title_tag

def get_advertisements():
    """
    This function retrieves the information
    about advertisements stored in the database.
    """
    return pd.read_sql_query('select * from sreality', engine)

def create_page_source():
    """
    This function reads the page template
    for displaying the saved advertisements from the database.
    """
    base = os.path.dirname(os.path.abspath(__file__))
    html = open(os.path.join(base, 'template.html'))
    return BeautifulSoup(html, 'html.parser')

def prepare_page():
    """
    This function prepares the page with saved advertisements
    for showing at the required address.
    """
    soup = create_page_source()
    df = get_advertisements()

    table = soup.find('table', attrs={'class':'sRealityTable'})

    # Go through the saved advertisements
    for idx in df.index:
        title_tag = get_title_tag(soup, df, idx)
        image_column_tag = get_image_column_tag(soup, df, idx)
        row = create_row(soup, title_tag, image_column_tag)
        table.append(row)

    # Write information about saved advertisements count
    items_count_tag = soup.find('span', attrs={'class':'itemsCount'})
    items_count = get_advertisements_count(df)
    items_count_tag.replace_with(str(items_count))

    # Save a file with the HTML source code
    with open("sreality_page.html", "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))

def save_to_database(titles, images_url):
    """
    This function saves read titles and images URLs to the PostgreSQL database.
    """
    df_insert = pd.DataFrame({'Titles': titles, 'Images URL': images_url})
    df_insert.to_sql('sreality', engine, if_exists='replace', index=False)

def get_image_url(div):
    """
    This function returns the first image URL of the current advertisement.
    """
    return div.find('img', attrs={}).attrs['src']

def get_title(div):
    """
    This function returns the title of the current advertisement.
    """
    return div.find('span', attrs={'class':'name ng-binding'}).text

def get_page_source(driver, page):
    """
    This function returns the HTML code of the page with advertisements.
    """
    driver.get("https://www.sreality.cz/en/search/for-sale/apartments?page=" + str(page))
    time.sleep(1)
    page_content = driver.page_source
    return BeautifulSoup(page_content, "html.parser")
def scrape_advertisements():
    """
    This function scrolls through pages of real estate advertisements
    and saves the required number of titles and images URLs.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    titles = []
    images_url = []

    # Scroll through pages with advertisements
    for page in range (SCRAPED_PAGES_COUNT):
        sreality_soup = get_page_source(driver, page)
        for div in sreality_soup.findAll('div', attrs={'class':'property ng-scope'}):
            titles.append(get_title(div))
            images_url.append(get_image_url(div))

    # Save advertisements to the PostrgeSQL database
    save_to_database(titles, images_url)

if __name__ == '__main__':
    # Connect to the PostgreSQL database
    postgres_db = f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
    engine = create_engine(postgres_db)

    scrape_advertisements()
    prepare_page()
    show_page()
