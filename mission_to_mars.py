import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

from selenium import webdriver
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}
    
#********************************************************************************************************************************************************************************************************************************************************
    # ## Mars News

    nasa_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_news_url)
    nasa_news_html = browser.html

    nasa_news_soup = bs(nasa_news_html, 'html.parser')
    console.log(nasa_news_soup)

    nasa_news_results = nasa_news_soup.find_all('li', class_="slide")

    for nasa_news_result in nasa_news_results:
    
        title = []
        teaser = []
        # Error handling
        try:
            # Identify and return title of the articles
            title = nasa_news_result.find('div',class_="content_title").text
            # Identify and return teaser text of the articles
            teaser = nasa_news_result.find('div', class_="article_teaser_body").text
            
        mars_news_dict = {"title": title, "teaser": teaser}
        mars_news_report = mars_news_report.append(mars_news_dict)
        mars_data["news"] = build_report(mars_news_report)
            
#********************************************************************************************************************************************************************************************************************************************************
    # ## JPL Mars Space Images - Featured Image


    featured_image_url = "/?search=&category=Mars"
    nasa_img_url = 'https://www.jpl.nasa.gov/spaceimages'+featured_image_url
    browser.visit(nasa_img_url)
    nasa_img_html = browser.html

    nasa_img_soup = bs(nasa_img_html, 'html.parser')
    img=nasa_img_soup.find_all('a',class_="fancybox")[1]
    img_url = img['data-thumbnail']
    img_url = "https://www.jpl.nasa.gov" + img_url
    console.log(img_url)
    
    mars_data["image"] = build_report(img_url)

#********************************************************************************************************************************************************************************************************************************************************
    # ## Mars Weather


    twi_MarsWxReport_url = "/marswxreport?lang=en" 
    nasa_twi_url = 'https://twitter.com'+twi_MarsWxReport_url
    browser.visit(nasa_twi_url)

    tweet_text = browser.find_by_xpath('.//p[@class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"]')[0].text
    console.log(tweet_text)
    
    mars_data["tweet_forecast"] = build_report(tweet_text)

#********************************************************************************************************************************************************************************************************************************************************
    # ## Mars Facts

    marsFactext_url = "/mars/" 
    marsFact_url = 'https://space-facts.com'+marsFactext_url
    browser.visit(marsFact_url)
    marsFacts_table = browser.find_by_xpath('.//table[@class="tablepress tablepress-id-mars"]').text
    console.log(marsFacts_table)
    
    mars_data["MarsFact_table"] = build_report(marsFacts_table)

        # https://stackoverflow.com/questions/22604564/how-to-create-a-pandas-dataframe-from-a-string
    #     import sys
    #     if sys.version_info[0] < 3: 
    #         from StringIO import StringIO
    #     else:
    #         from io import StringIO

    #     TESTDATA = StringIO(marsFacts_table)

    #     df = pd.read_csv(TESTDATA, sep=":", header=None)    

    #     df.to_html('facts_table.html',index=False, header=None)

#********************************************************************************************************************************************************************************************************************************************************
    # ## Mars Hemisperes

    marsHemsExt_url = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars" 
    marsHems_url = 'https://astrogeology.usgs.gov'+marsHemsExt_url
    marsHems_rooturl = 'https://astrogeology.usgs.gov'
    browser.visit(marsHems_url)
    marsHems_html = browser.html

    marsHems_soup = bs(html, 'html.parser')
    results_itemLink = soup.find_all('a', class_="itemLink product-item")


    for result in results_itemLink:
        try:
            img_url = []
            title = []

            title = result.find("h3")
            print(title)
            img_url = result.find("img", class_="thumb").get('src')
            print(img_url)
        except AttributeError:
            pass

        marsHems_dict = {"title": title, "img_url": marsHems_rooturl+img_url}
        marsHems_report = mars_news_report.append(marsHems_dict)
        mars_data["Hemispheres"] = build_report(marsHems_report)
        
        
        
    return mars_data

#********************************************************************************************************************************************************************************************************************************************************       
def build_report(mars_report):
    final_report = ""
    for p in mars_report:
        final_report += " " + p.get_text()
        print(final_report)
    return final_report