from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('products', views.products, name="products"),#Baldinių plokščių sąrašas
    path('products/<int:product_id>', views.product, name='product'), #plokštė iš sąrašo su 100x100
    path('order_line/', views.OrderLineListView.as_view(), name='order_line'),#užsakymo eilutė
    path('order_line/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('search/', views.search, name="search"),
    path('personal_orders/', views.MyOrderListView.as_view(), name="my_orders_list"),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path('orders/', views.order_list, name='order_list'),
    path('order/create/', views.order_create, name='order_create'),
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