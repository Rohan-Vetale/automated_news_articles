"""
@Author: Rohan Vetale

@Date: 2024-4-30 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-4-30 19:22

@Title : This module is used to check the user's query in DB or to generate the html page using fetch_content module
"""
import os
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from Home.models import SearchQ
from utils.fetch_content import get_content
from newsapi import NewsApiClient

def get_page(query):
    """
    Check if the query already exists in the database.
    If not, fetch content using fetch_content and render HTML template.
    Save the rendered HTML content to a file.
    """

    # Check if the query already exists in the database
    if SearchQ.objects.filter(query=query).exists():
        # Query already exists, handle accordingly
        print("Query exists")
        return "Exists, Done"
    else:
        print("Query {} does not exist".format(query))
        title, img_url, content = get_content(query=query)
        if content == "No Articles found, try searching with other keywords":
            return "No Articles"
        
        # Render the HTML template with the content variable
        html_content = render_to_string('search.html', {
            'Content': content,
            'csrff': "{% csrf_token %}",
            'Queried': query,
            'titlez': title,
            'imgUrl': img_url
        })

        # Choose a filename based on the query
        filename = "{}.html".format(query)  

        # Save the rendered HTML content to the file
        file_path = os.path.join('G:\\Company\\Django\\ANA\\automated_news_articles\\templates', filename)
        with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(html_content)
        print("Done")
        return "Successful, Done"

# Optionally, create a database entry with the query and file path
# ... (Code to save the query and file path to the database)
