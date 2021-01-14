from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from dateutil import parser
import time, os
import pandas as pd
import json

import configparser
from urllib import request
import numpy as np

from random import randint

import urllib.request 

from getDataFromGoogleSheets import gsheet2df

df = gsheet2df('1zwg9eMpN2-32pIZSobA_JAoybogB5um9iehUT05amOk', 'ALL!A:R')

df.replace(np.nan, '', regex=True, inplace=True)

#get the data from pandas
class donation(object):
    def __init__(self, row):
        self.title = row['Title']
        self.subtitle = ""
        self.description = row['Description']
        self.category = row['Item or exp.']
        self.fariMarketValue = row['Value']
        self.startingBid = row['Min.bid']
        self.minBidIncrement = row['Bid increment']
        self.donorInformation = row['Name']
        self.image = row['Picture']
        
        
def commit(row):
    
    # initialize the class
    don = donation(row)
    driver = webdriver.Chrome('/Users/usmanrizwan/PycharmProjects/RPA_PS_Corrity/chromedriver')
    driver.get("https://www.32auctions.com/login")#put here the adress of your page
    
    #Login
    driver.find_element_by_id("email").send_keys("ADD YOUR EMAIL ADDRESS")
    driver.find_element_by_id("password").send_keys("ADD PASSWORD")
    
    driver.find_elements_by_name("commit")[0].click()
    
    #Click on the current Auction
    driver.find_elements_by_xpath("//*[contains(text(), 'COE Employees United Way Online Auction 2019')]")[0].click()
    
    #Click on the plus sign to add an auction
    driver.find_element_by_xpath("//a[@class='btn btn-pink no-brnd fixed-add-item-btn']").click()
    
    #Add title
    driver.find_element_by_id("auction_item_title").send_keys(don.title)
    time.sleep(2)
    
    # Add description
    driver.find_element_by_id("auction_item_description").send_keys(don.description)
    
    #Click on the plus sign to add a category
    driver.find_element_by_xpath("//i[@class='fa fa-plus']").click()
    
    time.sleep(2)
    
    #Add category
    driver.find_element_by_id("category-name").send_keys(don.category)
    
    #Click on the submit button
    driver.find_element_by_xpath("//button[@class='btn btn-block btn-primary btn-submit']").click()
    
    time.sleep(2)
    
    driver.find_element_by_id("auction_item_fair_market_value").send_keys(don.fariMarketValue)
    
    #Clear the bid line and add the value
    driver.find_element_by_id("auction_item_starting_bid").clear()
    driver.find_element_by_id("auction_item_starting_bid").send_keys(don.startingBid)
    
    #Clear the min bid line and add the value
    driver.find_element_by_id("auction_item_bid_increment").clear()
    driver.find_element_by_id("auction_item_bid_increment").send_keys(don.minBidIncrement)
    
    driver.execute_script("window.scrollTo(0, 1180)")
    
    #Click on the plus sign to add a donor
    driver.find_element_by_xpath("//a[@class='btn btn-secondary btn-create-donor']").click()
    time.sleep(2)
    driver.find_element_by_id("donor-name").send_keys(don.donorInformation)
    #Click on the create category btn
    driver.find_element_by_xpath("//button[@class='btn btn-block btn-primary btn-submit']").click()
    time.sleep(2)
    
    #Check if the pop up comes and select "Add As A New Donor"
    try:
        driver.find_elements_by_xpath("//*[contains(text(), 'Add As A New Donor')]")[0].click()
    except:
        pass
    
    time.sleep(2)
    
    #Click on the Add Auction Item button
    driver.find_element_by_xpath("//input[@value='Add Auction Item']").click()
    
    time.sleep(3)
    
    if don.image != "":
        name = don.title.replace("/", "")
        f = open('images/' + name + '.jpg', 'wb')
        if 'id=' in don.image:
            f.write(request.urlopen("https://drive.google.com/a/edmonton.ca/uc?authuser=1&id=" 
                                    + don.image.split('=')[1] + "&export=download").read())
            f.close()
        elif '/d/' in don.image:
            f.write(request.urlopen("https://drive.google.com/a/edmonton.ca/uc?authuser=1&id=" 
                                    + don.image.split('/d/')[1].split('/')[0] + "&export=download").read())
            f.close()

        driver.find_element_by_xpath("//input[@name='pic_files[]']").send_keys('/Users/usmanrizwan/workspace/32Auctions/images/' + name + '.jpg')
    
        time.sleep(2)
        #upload image
        driver.find_element_by_xpath("//input[@class='btn btn-block btn-primary']").click()

    time.sleep(2)
    #Click on Done With Images
    driver.find_element_by_xpath("//a[@class='btn btn-lg btn-block btn-primary done-btn']").click()
    
    driver.close()
    
    return True
