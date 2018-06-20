from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from .models import SearchForm
from .constants import Constants
import requests

constants = None
# Create your views here.

# Search news articles by some specific search term

def topic(request):
    global constants
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data['search_term'])
            search_term = form.cleaned_data['search_term']
            constants = Constants()
            constants.setSearchTerm(search_term)

    url = settings.NEWS_API_BASE_URL
    url += "/everything?q="+constants.getSearchTerm()+"&"
    url += str(timezone.datetime.now().date())+"&"
    url += "sortBy=relevancy&"
    url += "pageSize=100&apiKey="+settings.NEWS_API_KEY
    #print(timezone.datetime.now().date())
    article_list = requests.get(url)
    errorStatus = False
    if article_list.json()['status'] == 'error':
        errorStatus = True
    else:
        article_list = article_list.json()['articles']
    #print("Total Results = ",article_list.json()['totalResults'])
    #article_list = article_list.json()['articles']
    is_paginated = True
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
            
    return render(request, 'news/index.html', {'article_list':articles, 'status': errorStatus} )


def category(request):
    template_name = 'news/index.html'
    context_object_name = 'article_list'
    is_paginated = True
    paginate_by = 5

    selected_category = request.GET.get('c')
    url = settings.NEWS_API_BASE_URL
    url += "/top-headlines?"
    url += "language=en&"
    url += "country=us&"
    if selected_category:
        url += "category="+selected_category+"&"
    url += "apiKey="+settings.NEWS_API_KEY

    response = requests.get(url)
    articles = response.json()['articles']
    # pagination
    paginator = Paginator(articles, paginate_by)
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)

    return render(request, template_name, {'article_list': article_list})

def source(request):
    template_name = 'news/index.html'
    context_object_name = 'article_list'
    is_paginated = True
    paginate_by = 5
    
    selectedSource = request.GET.get('source')
    url = settings.NEWS_API_BASE_URL
    url += "/top-headlines?"
    url += "country=us&"

    print(selectedSource)
    if selectedSource:
        url += "source="+selectedSource+"&"
    
    url += "apiKey="+settings.NEWS_API_KEY
    print(url)
    response = requests.get(url)
    articles = response.json()['articles']
    # pagination
    paginator = Paginator(articles, paginate_by)
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)

    return render(request, template_name, {'article_list': article_list})

class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'article_list'
    is_paginated = True
    paginate_by = 5
    """
    News API usage.
    """
    #print(settings.NEWS_API_KEY)

    url = settings.NEWS_API_BASE_URL+"/top-headlines?country=us&apiKey="+settings.NEWS_API_KEY

    response = requests.get(url)
    print("Total Results = ",response.json()['totalResults'])
    #print(response.json()['articles'])
    #print(response.json())

    def get_queryset(self):
        """Return the last five published questions."""
        return self.response.json()['articles']