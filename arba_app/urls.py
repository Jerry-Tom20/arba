from django.contrib import admin
from django.urls import path,include
from arba_app import views

urlpatterns = [
    path('',views.first,name='first'),
    path('login_fun',views.login_fun,name='login_fun'),
    path('user_login',views.user_login,name='user_login'),
    path('user_fun',views.user_fun,name='user_fun'),
    path('admin_fun',views.admin_fun,name='admin_fun'),
    path('signup_fun',views.signup_fun,name='signup_fun'),
    path('user_create',views.user_create,name='user_create'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('forgot_password_fun',views.forget_pass_fun,name='forget_pass_fun'),
    path('accept',views.accept,name='accept'),
    path('allproduct_fun',views.allproduct_fun,name='allproduct_fun'),
    path('profile_fun',views.profile_fun,name='profile_fun'),
    path('logout',views.logout,name='logout'),
    path('cancel_profile_pop',views.cancel_profile_pop,name='cancel_profile_pop'),
    path('select_profile_pop',views.select_profile_pop,name='select_profile_pop'),
    path('edit_profile/<int:id>',views.edit_profile,name='edit_profile'),
    path('adding_product_fun/<slug>',views.adding_product_fun,name='adding_product_fun'),
    path('password_change_fun',views.password_change_fun,name='password_change_fun'),
    path('edit_password/<int:id>',views.edit_password,name='edit_password'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('prod_cart',views.prod_cart,name='prod_cart'),
    path('update_qty1/<int:id>',views.update_qty1,name='update_qty1'),
    path('update_qty2/<int:id>',views.update_qty2,name='update_qty2'),
    path('delete_cart/<int:id>',views.delete_cart,name='delete_cart'),
    path('store_fun1',views.store_fun1,name='store_fun1'),
    path('store_fun2',views.store_fun2,name='store_fun2'),
    path('edit_category_fun/<slug>',views.edit_category_fun,name='edit_category_fun'),
    path('edit_product_fun/<slug>',views.edit_product_fun,name='edit_product_fun'),
    path('delete_category_fun/<int:id>',views.delete_category_fun,name='delete_category_fun'),
    path('delete_product_fun/<int:id>',views.delete_product_fun,name='delete_product_fun'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('category_add_fun',views.category_add_fun,name='category_add_fun'),
    path('add_category',views.add_category,name='add_category'),
    path('product_add_fun',views.product_add_fun,name='product_add_fun'),
    path('add_product',views.add_product,name='add_product'),
    path('test',views.test,name='test'),
]