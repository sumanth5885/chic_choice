from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from .views import update_status




urlpatterns = [
    # path('', views.home,name="home"),

    path("",views.ProductView.as_view(),name="home"),


    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/', views.plus_cart, name='pluscart'),

    path('minuscart/', views.minus_cart, name='minuscart'),

    path('removecart/', views.remove_cart, name='removecart'),

    path('delete_item/', views.delete_item, name='delete_item'),

    path('delete_profile/', views.delete_profile, name='delete_profile'),


    

    path('checkout/', views.checkout, name='checkout'),

    path('buynow_checkout/', views.buynow_checkout, name='buynow_checkout'),



    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('payment_done_buynow/', views.payment_done_buynow, name='payment_done_buynow'),








    path('buy/', views.buy_now, name='buy-now'),

    path('profile/', views.ProfileView.as_view(), name='profile'),


    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    
    # path('login/', views.login, name='login'),

    
    path('logout/', auth_views.LogoutView.as_view(next_page='sign-in'), name='logout'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name="app/passwordchange.html", form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name ="passwordchange" ),

    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name="app/passwordchangedone.html"),name="passwordchangedone"),


    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),



    # path('registration/', views.customerregistration, name='customerregistration'),
    path("registration/", views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('account-verify/<slug:token>', views.account_verify, name='account-verify'),
    
    # path('accounts/login/', auth_views.LoginView.as_view(next_page='home', template_name='app/login.html', authentication_form=LoginForm), name="login"),
    # path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('accounts/login/', views.SignInView.as_view(), name='sign-in'),

    

    

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('help/', views.help, name='help'),



    #men
    path('mblazers/', views.mblazers, name='mblazers'),
    path('mblazers/<slug:data>', views.mblazers, name='mblazersdata'),

    path('mshirts/', views.mshirts, name='mshirts'),
    path('mshirts/<slug:data>', views.mshirts, name='mshirtsdata'),

    path('mpants/', views.mpants, name='mpants'),
    path('mpants/<slug:data>', views.mpants, name='mpantsdata'),


    path('mshoes/', views.mshoes, name='mshoes'),
    path('mshoes/<slug:data>', views.mshoes, name='mshoesdata'),

    path('mhats/', views.mhats, name='mhats'),
    path('mhats/<slug:data>', views.mhats, name='mhatsdata'),

    path('meyewear/', views.meyewear, name='meyewear'),
    path('meyewear/<slug:data>', views.meyewear, name='meyeweardata'),


    #women
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),

    path('Chudidar/', views.Chudidar, name='Chudidar'),
    path('Chudidar/<slug:data>', views.Chudidar, name='Chudidardata'),

    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),

    path('wshoes/', views.wshoes, name='wshoes'),
    path('wshoes/<slug:data>', views.wshoes, name='wshoesdata'),



    path('jewellery/', views.jewellery, name='jewellery'),
    path('jewellery/<slug:data>', views.jewellery, name='jewellerydata'),

    path('saree/', views.saree, name='saree'),
    path('saree/<slug:data>', views.saree, name='sareedata'),


    #kids
    path('boy/', views.boy, name='boy'),
    path('boy/<slug:data>', views.boy, name='boydata'),

    path('girl/', views.girl, name='girl'),
    path('girl/<slug:data>', views.girl, name='girldata'),

    #search
    path('search/', views.search, name='search'),
   
    path('con_adm/', views.con_adm, name='con_adm'),


    #designer
    path('designer_login/',views.designer_login, name='designer_login'),
    path('designer_home/',views.designer_home, name='designer_home'),

    path('des_passwordchange/', auth_views.PasswordChangeView.as_view(template_name="app/des_passwordchange.html", form_class=MyPasswordChangeForm, success_url='/des_passwordchangedone/'), name ="des_passwordchange" ),
    path('des_passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name="app/des_passwordchangedone.html"),name="des_passwordchangedone"),

    path('designers/', views.designers, name='designers'),
    # path('designers/<slug:data>', views.designers, name='designersdata'),


    path('designer-detail/<int:pk>', views.DesignerDetailView.as_view(), name='designer-detail'),
    path('designer_checkout/', views.designer_checkout, name='designer_checkout'),
    path('payment_done_designer/', views.payment_done_designer, name='payment_done_designer'),
    path('designer_orders/', views.designer_orders, name='designer_orders'),
    path('delete_designer/', views.delete_designer, name='delete_designer'),
    path('view_orders_designer/', views.view_orders_designer, name='view_orders_designer'),
    path('designer_placed/<int:designer_placed_id>/update_status/', update_status, name='update_status'),
    path('designer_about/', views.designer_about, name='designer_about'),
    path('designer_contact_page/', views.designer_contact_page, name='designer_contact_page'),
    path('edit_work/<int:work_id>/', views.edit_work, name='edit_work'),
    path('delete_work/', views.delete_work, name='delete_work'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_work/',views.add_work, name='add_work'),
    

#
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
