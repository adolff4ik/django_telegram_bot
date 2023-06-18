from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from .get_articles import *
from django.contrib.sessions.backends.db import SessionStore
from newsapp.models import *
from .parser import *
from .results import *


class SearchView(ListView):
    context_object_name = 'results'
    paginate_by = 4
    api_url =''

    def post(self, request):
        keyword = self.request.POST.get('q','')
        user = request.user

        post_data = request.POST.dict()

        del post_data['csrfmiddlewaretoken']
        
        articles_json = get_articles(self.api_url,post_data)
        queryset = results(articles_json, keyword, user)
        
        self.object_list = queryset

        request.session['object_list'] = self.object_list

        for key, value in post_data.items():
            request.session[key] = value

        return self.get(request)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        session_dict = dict(self.request.session.items())
        del session_dict['object_list']

        for key, value in session_dict.items():
            context[key] = value

        return context
    
    def get_queryset(self):
        return self.request.session['object_list']