from datetime import datetime
import os

from django.shortcuts import render, HttpResponse
from Home.models import SearchQ
from fetch_content import get_content
from check_db import get_page
from django.conf import settings  # Import settings for accessing static file paths

def home(request):
    """Render the home page."""
    return render(request, 'home.html')


def about(request):
    """Render the about page."""
    return render(request, 'abt.html')


def search(request):
    """Handle search functionality."""
    if request.method == "POST":
        query = request.POST.get('queryText', '')
        print("Received query is:", query)

        if query.lower() == "search" or not query:
            # Render default content or search page when query is empty or "search"
            context = {
                "titlez": "Search for a topic",
                "Content": "Get an AI generated article according to the search",
                "imgUrl": settings.STATIC_URL + "type.jpg"  # Use settings for static file path
            }
            return render(request, 'search.html', context)

        if query:
            content_status = get_page(query=query)
            print("Content status:", content_status)

            if content_status != "No Articles":
                date_time1 = datetime.today()
                id1 = datetime.now()
                id2 = int(id1.timestamp())
                info = SearchQ(id2, query, date_time1)
                info.save()
                print(content_status)
                go_to = query + ".html"
                context = {"Queried": query}
                return render(request, go_to, context)
            else:
                print(content_status)
                context = {
                "titlez": "No Articles found, try searching with other keywords",
                "Content": "Kindly search again!",
                "imgUrl": settings.STATIC_URL + "type.jpg" 
                }
                return render(request, 'search.html', context)
        else:
            context = {
                "titlez": "Search for a topic",
                "Content": "Get an AI-generated article according to the search",
                "imgUrl": settings.STATIC_URL + "type.jpg" 
            }
            return render(request, 'search.html', context)

    else:
        context = {
            "titlez": "Search for a topic",
            "Content": "Get an AI-generated article according to the search",
            "imgUrl": "/static/type.jpg"
        }
        return render(request, 'search.html', context)

   