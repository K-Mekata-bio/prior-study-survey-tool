from typing import List
from sre_constants import SUCCESS
from typing import List
import urllib.request, urllib.parse, urllib.error
import ssl
import json
import calendar
import time
from bs4 import BeautifulSoup
import numpy as np
import requests
import pandas as pd

def search(List: List[str]):
    for keyword in List:
        num = "30"
        url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=NUM&sort=relevance&term=KEYWORD"
        url = url.replace('NUM', str(num))
        url = url.replace('KEYWORD', keyword)
        print(f"Now fetching: {url}")

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        webpage = urllib.request.urlopen(url).read()
        while webpage == None:
            time.sleep(2)
        dict_page =json.loads(webpage)
        idlist = dict_page.get("esearchresult",{}).get("idlist",[])

        # remove brackets ex "[Breast cancer].", "[Breast cancer update in primary care: (V/V)]."
        def remove_brackets(title):
            nobra = ""
            brak = ['[',']']
            for i in title :
                if i not in brak:
                    nobra += i
            return nobra

        def get_bibliography(soup):
            article = soup.find('Article')
            ArticleTitle = ''
            if article.find('ArticleTitle'):
                    # title style "Title"
                    ArticleTitle = '"'
                    title = article.find('ArticleTitle').text
                    title = remove_brackets(title)
                    ArticleTitle += title
                    if ArticleTitle[-1] == '.':
                        ArticleTitle += '", '
                    else:
                        ArticleTitle += '," '

            journal = soup.find('Journal')
            journal_title = ''
            if journal.find('Title'):
                journal_title = journal.find('Title').text
                journal_title += ' '

            JournalIssue = journal.find('JournalIssue')
            month = JournalIssue.find('Month')
            date = ''
            if month:
                month = JournalIssue.find('Month').text
                if len(month)<3:
                    month_int = int(str(month))
                    month = calendar.month_abbr[month_int]
                year = JournalIssue.find('Year').text
                date = '('
                date += month
                date += '. '
                date += year
                date += '). '
            elif JournalIssue.find('Year'):
                date = '('
                date+= JournalIssue.find('Year').text
                date += '). '

            pubmed = ''
            if soup.find('ArticleIdList'):
                pubmed = 'PMID: '
                pubmed += soup.find('ArticleId', IdType="pubmed").text

            abstract = ''
            if article.find('AbstractText'):
                abstract = article.find('AbstractText').text

            result = []
            result.append(ArticleTitle)
            result.append(journal_title)
            result.append(date)
            result.append(pubmed)
            result.append(abstract)
            return result

        articles_list = []

        for link in idlist:
            urlp = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=idlist"
            url = urlp.replace('idlist', link)
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                # Legacy Python that doesn’t verify HTTPS certificates by default
                pass
            else:
                # Handle target environment that doesn’t support HTTPS verification
                ssl._create_default_https_context = _create_unverified_https_context

            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml-xml")
            article = get_bibliography(soup)
            articles_list.append(article)

        df = pd.DataFrame(articles_list)

        try:
            df.columns = ['ArticleTitle', 'journal_title', 'date', 'pubmed', 'abstract']
        except ValueError:
            print('no research')

        file_name = keyword + '_' + str(num) + '.csv'
        df.to_csv(file_name)

    print('Finish')
    