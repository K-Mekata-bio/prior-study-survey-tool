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
        url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&retmode=json&retmax=NUM&sort=relevance&term=KEYWORD"
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
            article = soup.find('article-meta')
            ArticleTitle = ''
            if article.find('article-title'):
                    # title style "Title"
                    ArticleTitle = '"'
                    title = article.find('article-title').text
                    title = remove_brackets(title)
                    ArticleTitle += title
                    if ArticleTitle[-1] == '.':
                        ArticleTitle += '", '
                    else:
                        ArticleTitle += '," '

            journal = soup.find('journal-meta')
            journal_title = ''
            if journal.find('journal-title'):
                journal_title = journal.find('journal-title').text
                journal_title += ' '

            publish = article.find('pub-date')
            month = publish.find('month')
            date = ''
            if month:
                month = publish.find('month').text
                if len(month)<3:
                    month_int = int(str(month))
                    month = calendar.month_abbr[month_int]
                year = publish.find('year').text
                date = '('
                date += month
                date += '. '
                date += year
                date += '). '
            elif publish.find('year'):
                date = '('
                date+= publish.find('year').text
                date += '). '

            pubmed = ''
            if soup.find('article-meta'):
                pubmed = 'PMID: '
                pubmed += soup.find('article-id', attrs={'pub-id-type': 'pmid'}).text

            abstract = ''
            if article.find('abstract'):
                abstract = article.find('p').text

            result = []
            result.append(ArticleTitle)
            result.append(journal_title)
            result.append(date)
            result.append(pubmed)
            result.append(abstract)
            return result

        articles_list = []

        for link in idlist:
            urlp = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&retmode=xml&id=idlist"
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
