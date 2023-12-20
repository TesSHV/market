from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Category, Product, Order, Feedback
from shop.forms import OrderForm, NewUserForm, FeedbackForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.contrib.auth.models import User


def main_page(request):
    category_tuple_list = [(category, category.product_set.all()[0].image) for category in Category.objects.all() if len(category.product_set.all()) > 0]
    return render(request, "shop/main_page.html", context={"categories": category_tuple_list})


def category_products_page(request, slug):
    specified_category = Category.objects.get(slug=slug)

    products_by_category = specified_category.product_set.all()
    context = {
        "products": products_by_category,
        "category_name": specified_category.name,
    }
    return render(request, "shop/category_products_page.html", context=context)


def product_details_page(request, slug):

    specified_product = Product.objects.get(slug=slug)
    product_feedbacks = specified_product.feedback_set.all()

    context = {}

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('login_user_page')
        if form.is_valid():
            new_feedback = Feedback(user=request.user, product=specified_product, feedback_text=form.cleaned_data['feedback_text'])
            new_feedback.save()
            messages.success(request, f"Thank you, {request.user.username}! We appreciate your feedback!")
            return redirect(f'/product_details/{slug}')
    else:
        form = FeedbackForm()
        context = {
            "form": form,
            "feedbacks": product_feedbacks,
            "product": specified_product,
        }

    return render(request, "shop/product_details.html", context=context)


def order_product_page(request, slug):

    if not request.user.is_authenticated:
        return redirect('login_user_page')

    form = None
    context = {}
    specified_product = Product.objects.get(slug=slug)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = Order(user=request.user, product=specified_product, deliveryAddress=form.cleaned_data['deliveryAddress'])
            new_order.save()
            messages.success(request, "Your order was successful. Check your Order History")
            return redirect('main_page')

    else:
        form = OrderForm()

        context = {
            "form": form,
            "product": specified_product,
        }

    return render(request, "shop/order_product.html", context=context)


def user_profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login_user_page')
    return render(request, 'shop/user_profile_page.html', context={"user": request.user})


def order_history_page(request):

    if not request.user.is_authenticated:
        return redirect('login_user_page')

    user_orders = request.user.order_set.all()
    user_products = []

    for order in user_orders:
        order_date = order.order_date
        delivery_address = order.deliveryAddress
        try:
            order_product = Product.objects.get(id=order.product_id)
        except Product.DoesNotExist:
            order_product = None
        user_products.append((order_product, order_date, delivery_address))

    return render(request, 'shop/order_history_page.html', context={"products": user_products})


def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect('main_page')


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "shop/user_login_page.html", context={"form": form})


def signup_user(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Successful registration! You are now logged in as {form.cleaned_data.get('username')}")
            return redirect("main_page")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "shop/user_signup_page.html", context={"form": form})


def about_us_page(request):
    return render(request, "shop/about_us_page.html")


def delete_feedback(request, feedback_id, product_slug, user_id):

    if not request.user.is_authenticated:
        return redirect(f'/product_details/{product_slug}')

    if user_id:
        if not request.user.is_staff:
            if not request.user.id == user_id:
                return redirect(f'/product_details/{product_slug}')

    # specified_product = Product.objects.get(slug=product_slug)

    feedback_to_delete = Feedback.objects.get(id=feedback_id)
    feedback_to_delete.delete()

    return redirect(f'/product_details/{product_slug}')