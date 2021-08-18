#!/usr/bin/python3
# Usage: python get_data.py <path_to_output_file>

import sys

def fetch_data(output_filename):
    """
    get_allpages.py

    MediaWiki API Demos
    Demo of `Allpages` module: Get all pages whose title contains the text
    "Jungle," in whole or part.

    MIT License

    Adapted from: https://www.mediawiki.org/wiki/API:Allpages
    """

    import requests
    import csv

    S = requests.Session()

    BASE_URL = "https://en.wikipedia.org/w/api.php"

    list_of_protected_articles = []

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "apprtype":"edit| move| upload", #different protection levels in Wikipedia
        "aplimit": 500
    }
        
    wiki_call = requests.get(BASE_URL, params=PARAMS)
    response = wiki_call.json()

    wikipedia_api_call_counter = 0

    while True:
        wiki_call = requests.get(BASE_URL, params=PARAMS)
        
        wikipedia_api_call_counter +=1
        print("Wikipedia call: ", wikipedia_api_call_counter)
        
        response = wiki_call.json()
        
        PAGES = response["query"]["allpages"]
        
        for page in PAGES:
            print(page["title"])
            list_of_protected_articles.append(page["title"])
            
            title = page["title"]
            row = [title]
            with open(output_filename, "a", encoding="UTF-8", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(row)              

        if 'continue' in response:
            PARAMS['continue'] = response['continue']['continue']
            PARAMS['apcontinue'] = response['continue']['apcontinue']

        else:
            break        
        print("===========================================================")

if __name__=='__main__':
    if(len(sys.argv)==2):
        output_filename = sys.argv[1]
        fetch_data(output_filename)
        
    else:
        print("Error! Usage: python get_data.py <path_to_output_file>")