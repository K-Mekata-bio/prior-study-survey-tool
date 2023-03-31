from typing import List
from sre_constants import SUCCESS
from serpapi import GoogleSearch
import pandas as pd

def search(keywords: List[str]):
    qapi = input("Do you have private API Key(SerpApi)? 'yes' or 'no': ")
    if qapi.lower() == "yes" or qapi.lower() == "y":
        pass
    else:
        print("SerpApi private API key is required.")
    yapi_key = input("Enter your private API Key(SerpApi): ")

    num_article = int(input("How many articles would you like to retrieve?: " ))
    if num_article <= 0 or num_article == None:
        print("Please enter an accurate value.")

    for keyword in keywords:
        params = {
            "engine": "google_scholar",
            "q": keyword,
            "api_key": yapi_key,
            "num": num_article
        }
        print(keyword)

        def serpapi(organic_results):
            # Extract information for each organic search result and append to the corresponding list
            results = []
            for i in organic_results:
                result = []

                title = i['title']
                result.append(title)

                publication_info = i['publication_info']['summary']
                result.append(publication_info)

                link = i['link']
                result.append(link)

                snippet = i['snippet']
                result.append(snippet)
                results.append(result)
            return results

        search = GoogleSearch(params)
        results_all = search.get_dict()
        organic_results = results_all['organic_results']
        article = serpapi(organic_results)

        df = pd.DataFrame(article)

        try:
            df.columns = ['title', 'publication_info', 'link', 'snippet']
        except ValueError:
            print('no research')

        file_name = keyword + '_' + str(num_article) + '.csv'
        df.to_csv(file_name)

    print('Finish')
