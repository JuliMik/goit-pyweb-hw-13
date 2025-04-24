from django.urls import path
from . import views

app_name = 'app_quotes'

urlpatterns = [
    path('', views.main, name='main'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('about_author/<int:author_id>', views.about_author, name='about_author'),
    path('tag/', views.tag, name='tag'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete')
]
