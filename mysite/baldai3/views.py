from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, Product, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    num_orders = Order.objects.all().count()

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'num_orders': num_orders,

    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)


def products(request):
    products = Product.objects.all()

    paginator = Paginator(products, per_page=4)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    context = {
        'products': paged_products,

    }
    return render(request, 'products.html', context=context)


def product(request, product_id):
    single_product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': single_product})


class OrderLineListView(generic.ListView):
    model = OrderLine
    template_name = 'order_line_list.html'
    context_object_name = "orderline_list"
    paginate_by = 5


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'


def search(request):
    query = request.GET.get('query')
    orders_search_results = Product.objects.filter(Q(decor__icontains=query))


    context = {
        "query": query,
        "orders_no_search": orders_search_results,
    }
    return render(request, template_name='search.html', context=context)
