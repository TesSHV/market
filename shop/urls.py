from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('categories/<str:slug>', views.category_products_page, name='category_products_page'),
    path('product_details/<str:slug>', views.product_details_page, name='product_details_page'),
    path('order_product/<str:slug>', views.order_product_page, name='order_product_page'),
    path(r'^user_profile/$', views.user_profile_page, name='user_profile_page'),
    path(r'^order_history/$', views.order_history_page, name='order_history_page'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('login_user/', views.login_user, name='login_user_page'),
    path('signup_user/', views.signup_user, name='signup_user_page'),
    path('about_us/', views.about_us_page, name='about_us_page'),
    path('delete_feedback/<int:feedback_id>/<str:product_slug>/<int:user_id>/', views.delete_feedback, name='delete_feedback'),
]
