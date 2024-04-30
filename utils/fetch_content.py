"""
@Author: Rohan Vetale

@Date: 2024-4-30 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-4-30 19:22

@Title : This module is used to fetch the content from the NewsAPI and GPT-4
"""

from os import getenv
from newsapi import NewsApiClient
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API clients
client = OpenAI(api_key=getenv('LLM_API_KEY'))
newsapi = NewsApiClient(api_key=getenv('NEWS_API_KEY'))

def get_content(query):
    """
    Fetch content using NewsAPI and OpenAI's GPT-4 model.
    :param query: The search query.
    :return: A tuple containing title, image URL, and final content.
    """

    try:
        print("Getting headlines for " + query)
        # Fetch top headlines
        top_headlines = newsapi.get_top_headlines(query)
        
        # Extract relevant information from the top headlines
        img_url = top_headlines['articles'][0]['urlToImage']
        title = str(top_headlines['articles'][0]['title'])
        descriptions = [article['description'] for article in top_headlines['articles']][:8]
        
        # Generate content using OpenAI's GPT-4 model
        if descriptions:
            news_content = "\n".join([f"Article {i + 1}: {description}" for i, description in enumerate(descriptions)])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You have to only generate and reply a news blog of 2 page content body. The title, related articles, some content is provided by the user from trusted sources. Skip the title part, start with introduction"},
                    {"role": "user", "content": "Here it is " + news_content}
                ]
            )
            final_content = response.choices[0].message.content
            return title, img_url, final_content
        else:
            raise Exception('No headlines found!')
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        try:
            print("No headlines found, using everything now")
            # Fetch everything
            top_everything = newsapi.get_everything(query)
            
            # Extract relevant information from the everything response
            img_url = top_everything['articles'][0]['urlToImage']
            title = str(top_everything['articles'][0]['title'])
            descriptions = [article['description'] for article in top_everything['articles']][:3]
            
            # Generate content using OpenAI's GPT-4 model
            if descriptions:
              print(f"Description is found {descriptions}")
              news_content = "\n".join([f"Article {i + 1}: {description}" for i, description in enumerate(descriptions)])
              response = client.chat.completions.create(
                  model="gpt-4",
                  messages=[
                      {"role": "system", "content": "The title, related articles, some content is provided by the user from trusted sources. You have to only generate and reply a news blog of 1 page content body only.Your reply will be pasted directly inside the body of article. Skip the title part and start with introduction directly"},
                      {"role": "user", "content": "Here it is " + news_content}
                  ]
              )
              final_content = response.choices[0].message.content
              return title, img_url, final_content
            else:
              title = ""
              img_url = ""
              final_content = "No Articles found, try searching with other keywords"
              return title, img_url, final_content
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
            title = ""
            img_url = ""
            final_content = "No Articles found, try searching with other keywords"
            return title, img_url, final_content
