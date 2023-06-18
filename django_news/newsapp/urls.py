from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from .views import *
import debug_toolbar


urlpatterns = [
    path('', home, name='home_url'),
    path('headlines', headlines, name='heaflines_url'),
    path('everything', everything, name='everything_url'),
    path('articles', ShowArticles.as_view(), name='articles_url'),
    path('headlines/results', HeadlineSerch.as_view(), name='results_headlines_url'),
    path('everything/results', EverythingSearch.as_view(), name='results_everything_url'),
    path('registration', RegUser.as_view(), name='registration_url'),
    path('login', LoginUser.as_view(), name='login_url'),
    path('logout', logout_user, name='logout_url'),
    path("__debug__/", include("debug_toolbar.urls")),
    #path('articles/<int:artcl_id>', home, name='artcl_url'),
]
