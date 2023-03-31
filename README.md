# prior-study-survey-tool (SENKOkenkyuHakkutsu-kun)
### video Demo: [SENKOkenkyuHakkutsu-kun](https://youtu.be/TLPz2ekeP5k)
### Description:
This is my first submission.
This Python program serves as a tool to search research literature using various platforms, such as PubMed, PubMed Central (PMC), and Google Scholar. Additionally, it can automatically install any required libraries if they are not already installed.

The program functions through the following steps:
1. Install necessary libraries.
2. Designate the folder for saving search results.
3. Choose the search platform (PubMed, PMC, Google Scholar).
4. Input the directory containing the CSV file with the keyword list.
5. Conduct keyword searches on the chosen platform and store the results in the designated folder.
6. Transfer the log file to the designated folder.

## main.py
The program first checks and installs required libraries before performing keyword searches on the user-selected platform. It reads keywords from the CSV file and generates a search query based on the chosen platform. Upon completing the search, the results are stored in the designated folder, and the log file is relocated to the same folder.A DeprecationWarning occurre; however, the use of "SUCCESS" is necessary for stable operation. Despite the warning, it must be utilized for the system to function properly.

## pubmed.py
This program searches the PubMed database for article information based on the provided keywords and saves the results in a CSV file.

The program operates as follows:
1. Accepts a list of keywords.
2. Generates a search query using the keywords and retrieves search results from the PubMed database.
3. Extracts information (title, journal name, publication date, PubMed ID, and abstract) for each article.
4. Stores the obtained article information in a data frame and saves it as a CSV file.

## pmc.py
The basic operation is the same as pubmed.py.

## google_scholar.py
I chose to use [SerpApi](https://serpapi.com/) because Google Scholar may ban users for making too many search queries. Therefore, it is necessary to sign in to SerpApi and obtain a private API key. Please note that with a free account, you can only retrieve up to 100 references per month.

This program searches for article information based on the provided keywords using Google Scholar and saves the results in a CSV file.

The program functions as follows:
1. Accepts a list of keywords and a private API key for SerpApi.
2. Generates a search query using the keywords in Google Scholar and retrieves the search results.
3. Extracts information (title, publication information, links, snippets) for each article.
4. Stores the retrieved article information in a data frame and saves it in a CSV file.


## Acknowledgment
I have referred to PhilippeCodes' Scrape_PubMed.py when creating a scraping program for PubMed. Thank you very much.
[Scrape_PubMed.py](https://github.com/PhilippeCodes/Web-Scraping-PubMed/blob/master/Scrape_PubMed.py)
VOICEVOX:ずんだもん
