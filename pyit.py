from pyperclip import *
import re,os
import pandas as pd
from excel_module import *
import base64
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from abstract_utilities import *
import os,json
from os.path import join,isfile,isdir,exists
import clipboard
import requests
from bs4 import BeautifulSoup
def get_abs_dir():
    return os.path.dirname(os.path.abspath(__file__))
def make_businesses_dir():
    business_dir =  os.path.join(get_abs_dir(),'businesses')
    os.makedirs(business_dir,exist_ok=True)
    return business_dir
def get_spec_business_dir(business_name):
    business_dir =os.path.join(make_businesses_dir(),business_name.replace(' ','_'))
    os.makedirs(business_dir,exist_ok=True)
    return business_dir
# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def get_repo_itter(key,value):
    for i,repo in enumerate(get_repository_data()):
        if repo.get(key) == value:
            return i

def extract_urls(text):
    # Initialize BeautifulSoup object with the content of the web page
    soup = BeautifulSoup(text, 'lxml')
    
    # Find all 'a' tags, then extract the 'href' attribute
    urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
    
    return urls
def get_url(url,business_name):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    def main():
        # Setup Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        try:
          # Initialize WebDriver
            

            # Open the webpage
            driver.get(url)

            # Get page source
            page_source = driver.page_source
            write_to_file(contents=str(page_source),file_path=get_html_data_file_path(business_name))
            # Print the page source
        
        finally:
            # Close the browser
            driver.quit()
    main()
    
def get_repository_file_path(business_name):
    return os.path.join(get_spec_business_dir(business_name),'repository.json')
def get_html_data_file_path(business_name):
    return os.path.join(get_spec_business_dir(business_name),'source_code.json')
def get_html_data(business_name):
    file_path = get_html_data_file_path(business_name)
    if not os.path.isfile(file_path):
        write_to_file(contents="",file_path=file_path)
    return read_from_file(file_path)
def get_repository_data(business_name):
    file_path = get_repository_file_path(business_name)
    if not os.path.isfile(file_path):
        safe_dump_to_file(data={},file_path=file_path)
    return safe_read_from_json(file_path)
def save_repository_data(repo_data,business_name):
    safe_read_from_json(get_repository_file_path(business_name))
    safe_dump_to_file(data=repo_data,file_path=get_repository_file_path(business_name))

def get_csv_path():
    return "/home/gamook/Documents/catalyst/solar/CSLBSearchData_092626200.xlsx"
def get_row(df,i):
    df = get_df(df)
    return df.iloc[i]

def get_all_links(domain):
    href_list = set([domain])  # Use a set to avoid duplicates
    to_visit = set([domain])
    
    while to_visit:
        current_url = to_visit.pop()
        try:
            #response = requests.get(current_url, timeout=5)  # Add timeout
            
            soup = BeautifulSoup(get_source(url), 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith('/'):
                    href = f"{domain.rstrip('/')}/{href.lstrip('/')}"
                if href.startswith(domain) and href not in href_list:
                    href_list.add(href)
                    to_visit.add(href)  # Add new URLs to visit
        except requests.RequestException as e:
            print(f"Error fetching {current_url}: {e}")
    
    return list(href_list)
def extract_emails(text, pattern):
    """
    Extracts email addresses from provided text using a list of regex patterns.
    """


    emails = re.findall(pattern, text, re.IGNORECASE)
    if emails:
        return emails  # Returns list of emails as soon as any valid pattern matches
    
    return []  # Return an empty list if no patterns match
def list_and_set(list_obj):
    return list(set(list_obj))
def get_all_contact_info(string,dicts):
    info_types={"email":[r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',r'^\S+@\S+\.\S+$'],
    "phones":[r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'],
    "city":[r'([A-Z\s]+)\s\d{5}(?:[-\s,]*\d{5})*']}
    #"urls":[r'\b(?:http|https):\/\/(?:www\.)?[a-zA-Z0-9\-_]+(?:\.[a-zA-Z]{2,})+(?::\d{2,5})?(?:\/[^\s]*)?\b']}
    for info_type,patterns in info_types.items():
        if info_type not in dicts:
            dicts[info_type]=[]
        for pattern in patterns:
            pat= extract_emails(string, pattern)
            dicts[info_type]+=pat
    if "urls" not in dicts:
        dicts["urls"]=[]   
    dicts["urls"] = list_and_set(dicts["urls"]+extract_urls(string))
    return dicts
def await_copy(print_str,company):
        clipboard.copy(print_str)
        spam = clipboard.paste()
        while True:
                if clipboard.paste() != spam:
                       return  get_all_contact_info(clipboard.paste(),company)
        return clipboard.paste()

df = get_df(get_csv_path())
dicts = read_excel_as_dicts(get_csv_path())
page_data = get_url("https://www.yelp.com/biz/catalyst-mortgage-roseville","yelp")
input(page_data)
dicts=[{"BusinessName":"Matt Matsuda"}]
for dict_ in dicts:
    
        business_name = dict_['BusinessName']
        business_dir = get_spec_business_dir(business_name)
        dict_ = safe_json_loads(get_repository_data(business_name) or dict_)
        
        for each in ["email address","phone number","cell pone","linkedin","resume"]:
            search = business_name+' '+each
            url = f"https://www.google.com/search?q={search.replace(' ','+')}"
            get_url(url,business_name)
            dict_ = get_all_contact_info(get_html_data(business_name),dict_)
           
  
            

         
