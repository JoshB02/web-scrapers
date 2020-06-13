# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:18:33 2020

@author: anite
"""

from selenium import webdriver                      
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def Amazon_Scrape():
    products_list = ['Car','Baseball Bat'] #this list should contain all the products, as strings, which you would like to scrape reviews for
    reviews_list = [] #list where all the reviews scraped will be added
    browser = webdriver.Chrome() #this creates the chrome browser
    wait = WebDriverWait(browser, 5) #explicit wait time
    browser.get('https://www.amazon.com/ref=nav_logo') #tells the browser to go to the Amazon home page
    for product in products_list: #for loops through each product in order to scrape each product's reviews
        searchBarLocation = wait.until(EC.element_to_be_clickable((By.ID, 'twotabsearchtextbox'))) #determines the location of the search bar on the Amazon home page
        searchBarLocation.send_keys(product) #enters each product name into the seach bar
        time.sleep(2)
        enter_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nav-search-submit.nav-sprite'))).click() #clicks enter on the search bar to view all results for a given product
        time.sleep(2)
        onlyProductsWithReviews_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-icon.a-icon-star-medium.a-star-medium-1'))).click() #ensures that the product selected will actually contain reviews 
        time.sleep(2)
        firstProduct_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-size-base-plus.a-color-base.a-text-normal'))).click() #selects the first product on the page
        time.sleep(2)
        seeAllReviews_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-link-emphasis.a-text-bold'))).click() #takes the browser to the webpage where you can access all the reviews for a given product
        time.sleep(2)
        totalReviewsLocation = wait.until(EC.element_to_be_clickable((By.ID, 'filter-info-section'))) #determines the location of the text stating the total number of reviews
        totalReviewsPhrase = totalReviewsLocation.text #turns the totalReviewsLocation into text
        totalReviewsNumber = str(totalReviewsPhrase)[str(totalReviewsPhrase).find("of")+3:str(totalReviewsPhrase).find("reviews")-1] #splits the text to to remove the phrase "Showing x-y of"
        if(totalReviewsNumber.find(",")>-1): #accounts for products with over 1,000 reviews
            totalReviewsNumber = totalReviewsNumber.replace(',','') #replaces comma in numbers like 1,000 to 1000 which can be read an an integer
        numberOfNextClicks = int((int(totalReviewsNumber)/10)) #calculates the total number of clicks of the next page button needed to access all reviews
        numberOfNextClicks_list = list(range(1,numberOfNextClicks+2)) #creates a list from 1 to the required number of next page clicks
        time.sleep(2)
        for nextClick in numberOfNextClicks_list: #creates a for loop for each page containig reviews
            reviewsLocation_list = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'a-size-base.review-text.review-text-content'))) #determines the location of all the reviews on each page
            for review in reviewsLocation_list: #creates a for loop for all the reviews being scraped on a page
                reviews_list.append(review.text) #adds each reviews to a list as text
            if(len(numberOfNextClicks_list)>1): #checkes whether a product only has one page of reviews to prevent throwing an error with the next page button
                nextPageButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-last'))).click() #clicks on the next page button after all the reviews on each page have been scraped
                time.sleep(2)
        amazonHomeButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nav-logo-link'))).click() #returns to the Amazon home page after scraping the reviews for each product
        time.sleep(2)

Amazon_Scrape() #calls the Amazon_Scrape method