from .import views
from django.urls import path,re_path,register_converter

class YearConverter:
    regex = r"20\d{2}"
    
    def to_python(self, value): #문자열으 정수로 변경해서 넘겨줌
        return int(value)
    
    def to_url(self, value): #url 리버스할때 잘 리버싱 되도록 해주는 함수
        return "%04d" % value

register_converter(YearConverter, 'year')

app_name = 'inatagram' # URL Reverse에서 namespace역할을 하게 됩니다.

urlpatterns = [
    path('', views.post_list),
    path('<int:pk>/', views.post_detail),
    #re_path(r'(?P<pk>)\d+/$', views.post_detail), # path('<int:pk>/', views.post_detail)와 기능적으로 같다
    # path('archives/<year:year>/', views.archives_year), # register_converter를 이용한 url
    #re_path(r'archives/(?P<year>\d{4})/', views.archives_year),

    path('archive/', views.post_archive, name='post_archive'),
]