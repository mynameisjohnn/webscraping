# Dependencies
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver


def init_browser():
    return Browser("chrome", headless=False)


def scrape():
    browser = init_browser()
    # Create mission_to_mars dict to insert into mongo
    mission_to_mars = {}

    # Visit mars nasa site
    mars_news_site = 'https://mars.nasa.gov/news/'
    response = requests.get(mars_news_site)
    browser.visit(mars_news_site)
    
    # Create soup object
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Append Mars news to mission_to_mars dict
    title = soup.find('div',class_='content_title').text
    
    # Append news headline to the mission_to_mars dict
    mission_to_mars["headline"] = title
   
    paragraph = soup.find('div', class_='rollover_description_inner').text

    # Append news artical mission_to_mars dict
    mission_to_mars["article"] = paragraph

    # Use Splinter to scrape.
    browser = Browser('chrome')
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    html = browser.html
    soup_div = BeautifulSoup(html,'html.parser')
    image_results = soup_div.find('img', class_='thumb')
    image_src = image_results['src']
    featured_image = 'https://www.jpl.nasa.gov/' + image_src

    # Append the featured image to the mission_to_mars dict
    mission_to_mars['featured_image'] = featured_image

    # Scrape Mars Twitter feed
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(tweet_url)
    soup_tweet = BeautifulSoup(response.text,'html.parser')
    recent_tweet = soup_tweet.find('p',class_='TweetTextSize').text
   
    # Append tweet to the mission_to_mars dict
    mission_to_mars['weather_tweet'] = recent_tweet

    # Scrape the space facts website
    url_table = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url_table)
   
    # Create Mars Data Frame
    mars_table_df = mars_table[0]
    mars_table_df.columns = ['Fact','Data']
   
    # Convert the Mars Data Frame to HTML
    mars_table_html = mars_table_df.to_html(header=True, index=False)
   
    # Append the table to the mission_to_mars dict
    mission_to_mars['mars_facts_table'] = mars_table_html
    url_mh = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_mh)
    html = browser.html
    mars_soup = BeautifulSoup(html,'html.parser')
    hemisphere = mars_soup.find('div',class_='collapsible results')
    results = hemisphere.find('a')
    hemisphere_list = []
    for result in results:
        if result.h3:
            title = result.h3
            link = 'https://astrogeology.usgs.gov'
            print(title,link)    
            browser.visit(link)
            time.sleep(5)
            image_html = browser.html
            soup_scrape = BeautifulSoup(image_html,'html.parser') + result['href']
            soup_image = soup_scrape.find('div', class_='downloads').find('li').a['href']
            print(soup_image)
            mars_images = {'title':title, 'img_url':soup_image}
            hemisphere_list.append(mars_images)
           
            # Get image link for each hemisphere
            print(hemisphere_list)
           
            # Append image links to the mission_to_mars dict
            cerberus = hemisphere_list[0]['img_url']
            mission_to_mars['cerberus'] = cerberus_hemisphere
           
            schiaparelli = hemisphere_list[1]['img_url']
            mission_to_mars['schiaparelli'] = schiaparelli_hemisphere
           
            syrtis_major = hemisphere_list[2]['img_url']
            mission_to_mars['syrtis_major'] = syrtis_major_hemisphere

            valles_marineris = hemisphere_list[3]['img_url']
            mission_to_mars['valles_marineris'] = valles_marineris_hemisphere
    return mission_to_mars    