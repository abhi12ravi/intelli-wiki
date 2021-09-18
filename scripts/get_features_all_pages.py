import csv   
import os
import json
import pageviewapi
import random
import pandas as pd
import time
import sys

# from bs4 import BeautifulSoup
import requests

def fetch_details_from_info_page(title):
    url = "https://en.wikipedia.org/w/index.php?action=info&title=" + title

    html_content = requests.get(url)
    df_list = pd.read_html(html_content.text) # this parses all the tables in webpages to a list
    
    #Get Features from all tables

    #Basic info table
    try:
        display_title = df_list[1][1][0]
    except IndexError:
        print("IndexError for Basic info table, so skipping")
        return
    print("Display Title = ", display_title)

    # Process Table 1 - Basic Information
    dict_table1 = df_list[1].to_dict()
    
    #Declare vars
    page_length = ""
    page_id = ""
    number_page_watchers = ""
    number_page_watchers_recent_edits = ""
    page_views_past_30days = ""
    number_of_redirects = ""
    page_views_past_30days = ""
    total_edits = ""
    recent_number_of_edits = ""
    number_distinct_authors = ""
    number_categories = ""

    for key, value in dict_table1[0].items():  
        if value == 'Page length (in bytes)':        
            page_length = dict_table1[1][key]
            print("Page Length = ", page_length)
            
        elif (value == 'Page ID'):
            page_id = dict_table1[1][key]
            print("Scrapped Page ID = ", page_id)
            
        elif value == 'Number of page watchers':
            number_page_watchers = dict_table1[1][key]
            print("Number of Page Watchers = ", number_page_watchers)
        
        elif value == 'Number of page watchers who visited recent edits':
            number_page_watchers_recent_edits = dict_table1[1][key]
            print("Number of Page Watchers with recent edits = ", number_page_watchers_recent_edits)
        
        elif value == 'Number of redirects to this page':
            number_of_redirects = dict_table1[1][key]
            print("Number of redirects = ", number_of_redirects)
        
        elif value == 'Page views in the past 30 days':
            page_views_past_30days = dict_table1[1][key]
            print("Page views past 30 days = ", page_views_past_30days)
        
    #Process Table 3 - Edit History
    try:
        dict_table3 = df_list[3].to_dict()
        for key, value in dict_table3[0].items():  
            if value == 'Total number of edits':        
                total_edits = dict_table3[1][key]
                print("Total Edits = ", total_edits)
                
            elif value == 'Recent number of edits (within past 30 days)':
                recent_number_of_edits = dict_table3[1][key]
                print("Recent number of edits = ", recent_number_of_edits)
                
            elif value == 'Recent number of distinct authors':
                number_distinct_authors = dict_table3[1][key]
                print("Distinct authors =", number_distinct_authors)
    except IndexError:
        print("Couldn't find the Edit History Table, so skipping...")
        pass

    #Page properties Table
    try:
        categories_string = df_list[4][0][0]
        print(categories_string)
        number_categories = ""
        if  categories_string.startswith("Hidden categories"):         
            #Get number of categories
            for c in categories_string:
                if c.isdigit():
                    number_categories = number_categories + c     
            
            print("Total number of categories = ", number_categories)
    except IndexError:
        print("Couldn't find the Page Properties Table, so skipping...")
        pass

    print("============================================== EOP ======================================")

    features_dict = {   'page_length': page_length, 
                        'page_id': page_id, 
                        'number_page_watchers': number_page_watchers, 
                        'number_page_watchers_recent_edits': number_page_watchers_recent_edits, 
                        'number_of_redirects' : number_of_redirects, 
                        'page_views_past_30days' :page_views_past_30days, 
                        'total_edits': total_edits, 
                        'recent_number_of_edits': recent_number_of_edits, 
                        'number_distinct_authors': number_distinct_authors, 
                        'number_categories': number_categories }

    return features_dict

def write_header(filename):
    #Write line by line to file 
    row = ['page_id', 
            'page_title', 
            'protection_level', 
            'page_length', 
            'number_page_watchers', 
            'number_page_watchers_recent_edits',
            'number_of_redirects',
            'page_views_past_30days',
            'total_edits',
            'recent_number_of_edits',
            'number_distinct_authors',
            'number_categories'
            ]

    with open(filename, "a", encoding="UTF-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(row)
    

def main(input_file, output_file, num_skip_rows):

    df = pd.read_csv(input_file)
    start = time.time()

    # df = pd.read_csv(filepath)
    titles = df['page_title']

    write_header(output_file)

    counter = 0

    for title in titles:
        features_dict = fetch_details_from_info_page(title)

        index = titles[titles == title].index[0] # Adapted from https://stackoverflow.com/questions/18327624/find-elements-index-in-pandas-series
        
        #Map fetched fields to df fields
        df.loc[index,'page_length'] = features_dict['page_length']
        df.loc[index,'page_id_scrapped'] = features_dict['page_id']
        df.loc[index,'page_watchers'] = features_dict['number_page_watchers']
        df.loc[index,'page_watchers_recent_edits'] = features_dict['number_page_watchers_recent_edits']
        df.loc[index,'redirects'] = features_dict['number_of_redirects']
        df.loc[index,'page_views_past_30days'] = features_dict['page_views_past_30days']
        df.loc[index,'edit_count'] = features_dict['total_edits']
        df.loc[index,'recent_number_of_edits'] = features_dict['recent_number_of_edits']
        df.loc[index,'number_distinct_authors'] = features_dict['number_distinct_authors']
        df.loc[index,'number_categories'] = features_dict['number_categories']
        
        counter +=1
        print("~~ ", counter, "files completed successfully! ~~ Remaining articles = ", len(titles) - counter)

        #Write line by line to file 
        row = [features_dict['page_id'], 
                title, 
                features_dict['page_length'], 
                features_dict['number_page_watchers'], 
                features_dict['number_page_watchers_recent_edits'],
                features_dict['number_of_redirects'],
                features_dict['page_views_past_30days'],
                features_dict['total_edits'],
                features_dict['recent_number_of_edits'],
                features_dict['number_distinct_authors'],
                features_dict['number_categories']
                 ]

        with open("dataset/feature_dump_from_all_pages.csv", "a", encoding="UTF-8", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(row)

    # writing into the file
    try:
        df.to_csv(output_file, mode='a', index=False)
    except PermissionError:
        df.to_csv("dataset/all_protected_pages_2_features.csv", mode='a', index=False)

if __name__ == "__main__":

    #Get args from sys.argv and process them
    if(len(sys.argv)==4):
        input_file = sys.argv[1] 
        output_file = sys.argv[2] 
        num_skip_rows = int(sys.argv[3])
        main(input_file, output_file, num_skip_rows)
    else:
        print("Error in usage! Correct usage: $python fetch_page_views_protected.py <path_to_input_file> <path_to_output_file> num_rows_to_skip")
