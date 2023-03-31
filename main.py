from typing import List
import os
import csv
import importlib
import subprocess
import logging
import shutil
from typing import List
import urllib.request, urllib.parse, urllib.error
import sys
import time
from sre_constants import SUCCESS

# List of required libraries
required_libraries = ['bs4', 'requests', 'numpy', 'pandas', 'google-search-results']

# Function to install a library if it is not already installed
def install_library(library):
    try:
        # Try importing the library
        importlib.import_module(library)
        print(f"{library} is already installed.")
    except:
        # If the library is not installed, use subprocess.check_call() to run pip install command
        print(f"Installing {library}...")
        subprocess.check_call(["pip", "install", library])
        print(f"{library} has been installed.")

# Check each library in the required_libraries list, and install it if necessary
for library in required_libraries:
    install_library(library)

from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import numpy as np
import requests
import pandas as pd
import pubmed
import pmc
import google_scholar

logging.basicConfig(
    filename='Log.txt',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Set save folder
save = input("Enter save folder(Pressing enter saves in the current directory): ")
number = 0
if save == "":
    while True:
        save = f'Search results {number}'
        try:
            os.mkdir(save)
            print(f"Save folder: Search results {number}")
            break
        except:
            number += 1

else:
    print(f"Save folder: {save}")

check = os.path.exists(save)
if check == False:
    print("Folder dose not exit")
    sys.exit()

while True:
    search_platform = input("Enter platform -- PMC, PubMed(pm), Google Scholar(gs): ")

    # Pubmed gov
    if str.lower(search_platform) == "pubmed" or str.lower(search_platform) == "pm" or str.lower(search_platform) == "pubmed(pm)":
        while True:
            path = input("Enter directory for keyword list CSV file: ")
            if os.path.isfile(path):
                with open(path, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    List = ['+'.join(row) for row in reader]
                    print(f"Search list: {List}")
                    break
            else:
                print("No such file")
        os.chdir(save)
        pubmed.search(List)
        break

    # Pubmed Central
    elif str.lower(search_platform) == "pmc":
        while True:
            path = input("Enter directory for keyword list CSV file: ")
            if os.path.isfile(path):
                with open(path, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    List = ['+'.join(row) for row in reader]
                    print(f"Search list: {List}")
                    break
            else:
                print("No such file")
        os.chdir(save)
        pmc.search(List)
        break

    # google scholar
    elif str.lower(search_platform) == "google scholar" or str.lower(search_platform) == "gs" or str.lower(search_platform) == "google scholar(gs)" or str.lower(search_platform) == "googlescholar":
        while True:
            path = input("Enter directory for keyword list CSV file: ")
            if os.path.isfile(path):
                with open(path, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    List = [' '.join(row) for row in reader]
                    print(f"Search list: {List}")
                    break
            else:
                print("No such file")
        os.chdir(save)
        google_scholar.search(List)
        break
    else:
        print("Invalid input, please try again.")

# Return to the original directory
os.chdir("..")

# Move the log file to the save folder
try:
    os.makedirs(f"{save}", exist_ok=True)
    logging.shutdown()
    time.sleep(0.1)
    shutil.move("Log.txt", f"{save}/Log.txt")
except FileNotFoundError as e:
    print(e)
    logging.error(e)
