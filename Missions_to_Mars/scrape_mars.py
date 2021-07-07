from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars News Site page
    page_url = "https://redplanetscience.com/"
    browser.visit(page_url)
    time.sleep(1)

    # Create HTML object and parse with BeautifulSoup.
    html = browser.html
    soup = bs(html, "html.parser")
    first_li = soup.find("div", class_="list_text")

    # Define elements to scrape
    news_title = first_li.find("div", class_="content_title").text
    news_p = first_li.find("div", class_="article_teaser_body").text

    # Visit JPL Mars Space Images page
    page_url = "https://spaceimages-mars.com/"
    browser.visit(page_url)
    time.sleep(1)

    # Create HTML object and parse with BeautifulSoup.
    html = browser.html
    soup = bs(html, "html.parser")

    # Pull image
    featured_image_url = page_url + soup.find("img", class_="headerimage fade-in")["src"]

    # Visit Mars Facts page
    page_url = "https://galaxyfacts-mars.com/"
    browser.visit(page_url)
    html = browser.html

    # Pandas read table from page
    dfs = pd.read_html(page_url)
    df = dfs[1]
    df.columns = ["Description", "Mars"]

    # Convert to HTML table string
    table = df.to_html

    # Visit Mars Hemisphere page
    page_url = "https://marshemispheres.com/"
    browser.visit(page_url)
    time.sleep(1)

    # Create HTML object and parse with BeautifulSoup.
    html = browser.html
    soup = bs(html, "html.parser")

    # Pull image div tags
    hem_divs = soup.find_all("div", class_="description")
    hemisphere_image_url = []

    # Loop to pull title and urls each image
    for i in hem_divs:
        
        title = i.find('h3').text
        img_href = i.find('a', class_='itemLink product-item')['href']
        browser.visit(page_url + img_href)
        mars_html = browser.html
        soup_par = bs(mars_html, 'html.parser')
        image_url = page_url + soup_par.find('img', class_='wide-image')['src']
        hemisphere_image_url.append({"title": title, "img_url": image_url})
        
    hemisphere_image_url

    browser.quit()

    return mars_dict