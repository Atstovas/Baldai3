from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, Product, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from .forms import UserUpdateForm, ProfileUpdateForm

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


class MyOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'my_orders_list.html'
    context_object_name = "my_orders"
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(client_name=self.request.user)

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')

@login_required()
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, 'Profilis atnaujintas')
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            "u_form": u_form,
            "p_form": p_form,
        }
        return render(request, template_name="profile.html", context=context)