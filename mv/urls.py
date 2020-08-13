from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'mv'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('mv/<slug:the_slug>/', views.detail_mv.as_view(), name='detail_mv'),
    path('mv/<slug:the_slug>/frontview/', views.mv_detail_frontview.as_view(), name='mv_detail_frontview'),
    path('mv/<slug:the_slug>/update/', views.UpdateMV.as_view(), name='update'),
    path('upload/', login_required(views.CreateMV.as_view()), name='upload'),
    path('autosearch/', views.autosearch, name='autosearch'),
    path('search/', views.search.as_view(), name='search'),
    path('like/<slug:the_slug>/', views.Like_MV, name='like_mv'),
    path('v-pop/', views.lst_Vpop.as_view(), name='v-pop'),
    path('k-pop/', views.lst_Kpop.as_view(), name='k-pop'),
    path('us-uk/', views.lst_UsUk.as_view(), name='us-uk'),
    path('api/<slug:the_slug>/', views.mv_api.as_view(), name='api-getall'),
]
