#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 21:18:14 2020

@author: manzars
"""

from bs4 import BeautifulSoup
#from selenium import webdriver
import requests
from urllib.parse import urljoin
import pandas as pd

RequiredLimit = 10000
isScrappingPossible = True

website_heading = "https://www.indeed.com/"
url = "https://www.indeed.com/jobs?q=Software+Engineer&l=98115&radius=100"

header = "CompanyName, Designation, Ratings, Address\n"
file = open("scrappedData.csv", "w")
file.write(header)
file.close()

data = pd.read_csv('scrappedData.csv')
while((data.shape[0] < RequiredLimit) and isScrappingPossible):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    divs = soup.findAll('div', {'class': 'jobsearch-SerpJobCard'})
    for div in divs:
        comp_name = div.findAll('span', {'class': 'company'})[0].text.lstrip().rstrip().replace(',', ' -')
        designation = div.findAll('div', {'class': 'title'})[0].text.lstrip().rstrip().replace(',', ' -')
        location = div.findAll('span', {'class': 'location'})[0].text.lstrip().rstrip().replace(',', ' -')
        try:
            rating = div.findAll('span', {'class': 'ratingsContent'})[0].text.lstrip().rstrip()
        except:
            rating = 'NaN'
        rows =  comp_name + ", " + designation + ", " + rating + ", " + location + "\n"
        file = open("scrappedData.csv", "a")
        file.write(rows)
        file.close()
        print(rows)
    
    data = pd.read_csv('scrappedData.csv')
    try:
        url = urljoin(website_heading, soup.findAll('div', {'class': 'pagination'})[0].findAll('a')[-1].attrs['href']) #clicking on next page
        scrappingPossible = True
    except:
        isScrappingPossible = False
        
if(data.shape[0] < RequiredLimit):
    print("Sorry No more data Available, only " + str(data.shape[0]) + " data are available")
else:
    print(str(data.shape[0]) + " Data Scrapped Successfully")
    
"""
wb = webdriver.Firefox(executable_path = "/path/to/geckodriver")
wb.get(url)
html = wb.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, "lxml")
"""
