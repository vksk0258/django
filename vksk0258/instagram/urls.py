from .import views
from django.urls import path,re_path,register_converter
from .converters import DayConverter, MonthConverter, YearConverter


register_converter(YearConverter, 'year')
register_converter(MonthConverter, 'month')
register_converter(DayConverter, 'day')

app_name = 'instagram' # URL Reverse에서 namespace역할을 하게 됩니다.

urlpatterns = [
    path('new/', views.post_new, name='post_new'),
    path('<int:pk>/edit', views.post_edit, name='post_edit'),
    path('<int:pk>/delete', views.post_delete, name='post_delete'),
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    #re_path(r'(?P<pk>)\d+/$', views.post_detail), # path('<int:pk>/', views.post_detail)와 기능적으로 같다
    # path('archives/<year:year>/', views.archives_year), # register_converter를 이용한 url
    #re_path(r'archives/(?P<year>\d{4})/', views.archives_year),

    path('archive/', views.post_archive, name='post_archive'),
    path('archive/<year:year>/', views.post_archive_year, name='post+year_archive_year'),
    # path('archive/<year:year>/<month:month>', views.post_archive_month, name='post+year_archive_month'),
    # path('archive/<year:year>/<month:month>/<day:day>', views.post_archive_day, name='post+year_archive_day'),
]