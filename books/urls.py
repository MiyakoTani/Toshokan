from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path('place_make/', views.Place_make_View.as_view(), name="place_make"),
    path('place_delete/<int:page>', views.PlaceDelete, name='place_delete'), 
    path('place_change/<int:pk>', views.PlaceDeleteView.as_view(), name='place_change'), 
    path('book_create/', views.BookCreateView1.as_view(), name="book_create"),
    path('bookdata', views.ISBNAPIGet, name='bookdata'), 
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),  # 詳細ページのURL
    path('book_manage/<int:page>', views.book_manage, name="book_manage"),
    path('book_delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
    path('book_update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),
    path('book_search/<int:page>', views.book_search, name="book_search"),
    path('book_shelf/<int:page>', views.book_shelf, name="book_shelf"),
]