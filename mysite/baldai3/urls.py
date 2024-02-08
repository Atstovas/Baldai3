from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('products', views.products, name="products"),#Baldinių plokščių sąrašas
    path('products/<int:product_id>', views.product, name='product'), #plokštė iš sąrašo su 100x100
    path('order_line/', views.OrderLineListView.as_view(), name='order_line'),#užsakymo eilutė
    path('order_line/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('search/', views.search, name="search"),
]

# urlpatterns = [
#     path("", views.index, name="index"),
#     path('authors/', views.authors, name="authors"),
#     path('authors/<int:author_id>', views.author, name="author"),
#     path('books/', views.BookListView.as_view(), name='books'),
#     path("books/<int:pk>", views.BookDetailView.as_view(), name="book"),
#     path("search/", views.search, name="search"),
#     path("mybooks/", views.MyBookInstanceListView.as_view(), name="mybooks"),
# ]