from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import  Customer, Product, Cart, OrderPlaced, BCart, Designer, DesignerPlaced, TempDesignerPlaced, DesignerWorks, Profile
from .forms import CustomerRegistrationForm, CustomerProfileForm, DesignerWorksForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse
import re
from django.contrib.auth.models import User






# def home(request):
#     return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        totalitem = 0
        blazers = Product.objects.filter(category="MB")
        topwear = Product.objects.filter(category="TW")
        boy = Product.objects.filter(category="B")
        mshirt = Product.objects.filter(category="MST")
        mshoes = Product.objects.filter(category="MS")
        mhats = Product.objects.filter(category="MH")
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/home.html",{"blazers":blazers, "topwear":topwear, "boy":boy, "mshirt":mshirt, "mshoes":mshoes, "mhats":mhats, 'totalitem':totalitem })


# def product_detail(request):
#     return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, "app/productdetail.html", {"product":product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})


class DesignerDetailView(View):
    def get(self,request,pk):
        designer = Designer.objects.get(pk=pk)
        already_exist = DesignerPlaced.objects.filter(user=request.user, designer=designer)
        if already_exist:
            return redirect('designer_orders')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        works = designer.works.all()
        return render(request, "app/designerdetail.html", {"designer":designer, "totalitem":totalitem, "works":works})





@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        carts = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+= tempamount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':carts, 'totalamount':total_amount, 'amount':amount, 'totalitem':totalitem} )
        else:
            return render(request,'app/emptycart.html')



@login_required      
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    if op:
        return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':totalitem})        
    else:
        return render(request,'app/emptyorder.html')
        

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)
    

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)
    

def delete_item(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = OrderPlaced.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
    return redirect('orders')


def delete_profile(request):
    if request.method == 'GET':
        add_id = request.GET['add_id']
        c = Customer.objects.get(Q(id=add_id)& Q(user=request.user))
        c.delete()
    return redirect('address')
    



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)
    

    




@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

# def profile(request):
#     return render(request, 'app/profile.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    totalitem = 0
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, phone=phone, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!!! Profile updated successfully')
            form = CustomerProfileForm()
            return redirect('address')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


@login_required
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})




    

# def change_password(request):
#     return render(request, 'app/changepassword.html')



# def login(request):
#     return render(request, 'app/login.html')



# def customerregistration(request):
#     return render(request, 'app/customerregistration.html')



# from allauth.account.utils import send_email_confirmation

# class CustomerRegistrationView(View):
#     def get(self, request):
#         form = CustomerRegistrationForm()
#         return render(request, 'app/customerregistration.html', {'form':form})
    
#     def post(self, request):
#         form = CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             send_email_confirmation(request, user)
#             messages.success(request, "Congratulations! Please check your email to verify your account.")
#             return redirect("login")

#         return render(request, 'app/customerregistration.html', {'form': form})
    
# class CustomerRegistrationView(View):
#     def get(self, request):
#         form = CustomerRegistrationForm()
#         return render(request, 'app/customerregistration.html', {'form':form})
#     def post(self, request):
#         form = CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             messages.success(request, "Congratulations!! Registered Successfully")
#             form.save()
#             return redirect("login")
#         return render(request, 'app/customerregistration.html', {'form':form})
import uuid
from django.core.mail import send_mail
from django.conf import settings

def send_mail_after_registration(email, token):
    subject = "Verify Your Email"
    messages = f'click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, messages, from_email, recipient_list)
    print(messages)


def account_verify(request, token):
    pf = Profile.objects.filter(token=token).first()
    pf.verify = True
    pf.save()
    messages.success(request, 'Your Account Verified Succefully, You Can Login Now')
    return redirect('sign-in')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            token = uuid.uuid4()
            pro_obj = Profile(user=new_user, token=token)
            pro_obj.save()

            send_mail_after_registration(new_user.email, token)
            messages.success(request, 'Your Account Created Succefully, To Verify Your Account Please Check Your Email' )
            return redirect('customerregistration')
        return render(request, 'app/customerregistration.html', {'form':form})


from django.contrib.auth import authenticate, login

class SignInView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'app/login.html', {'form':form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                designer = Designer.objects.filter(username=user)
                if designer:
                    login(request, user)
                    return redirect('profile')
                else:
                    pro = Profile.objects.get(user=user)
                    if pro.verify:
                        login(request, user)
                        return redirect('profile')
                    else:
                        messages.warning(request, 'Your Account Not Verified Yet, Please Check Your Mail and Verify it.')
        
        return render(request, 'app/login.html', {'form':form})




@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount =70
    totalamount = 0.0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if add:
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+= tempamount
            totalamount = amount + shipping_amount
            dlr = int(totalamount/82.35)
        return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'dlr':dlr, 'totalitem':totalitem})
    else:
        return redirect('profile')


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def buynow_checkout(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    pro_duct = Product.objects.get(id=product_id)
    BCart(user=user, product=pro_duct).save()
    add = Customer.objects.filter(user=user)
    amount = 0.0
    shipping_amount =70
    totalamount = 0.0
    # cart_product = [p for p in Product.objects.all() if p.user == user]
    if add:
        if pro_duct:
            amount = pro_duct.discounted_price
            image = pro_duct.product_image
            totalamount = amount + shipping_amount
        dlr = int(totalamount/82.35)
        return render(request, 'app/buynow_checkout.html', {'add':add,"amount":amount,"image":image, 'totalamount':totalamount, 'pro_duct':pro_duct, 'dlr':dlr})
    else:
        return redirect('profile')
        



def send_mail_after_payment(email):
    subject = "Order Successfull"
    messages = "Thanks for using Chic Choice, Your order confirmed successfully"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, messages, from_email, recipient_list)


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
        send_mail_after_payment(user.email)
    return redirect("orders")






@login_required
def about(request):
    return render(request, "app/about.html")

@login_required
def contact(request):
    return render(request, "app/contact_page.html")

@login_required
def help(request):
    return render(request, "app/chatbot.html")


#men
@login_required
def mshirts(request, data=None):
    if data == None:
        mshirts = Product.objects.filter(category="MST")
    elif data == "Nap_Chief" or data == "Ben_Martin" or data == "Park_Avenue":
        mshirts = Product.objects.filter(category="MST").filter(brand=data)
    return render(request, 'app/mshirts.html', {"mshirts":mshirts})
    
@login_required
def mblazers(request, data=None):
    if data == None:
        mblazers = Product.objects.filter(category="MB")
    elif data == "Park_Avenue" or data == "Raymond" or data == "Peter_England":
        mblazers = Product.objects.filter(category="MB").filter(brand=data)
    
    return render(request, 'app/mblazers.html', {"mblazers":mblazers})

@login_required
def mshoes(request, data=None):

    if data == None:
        mshoes = Product.objects.filter(category="MS")
    elif data == "BATA" or data == "NIKE":
        mshoes = Product.objects.filter(category="MS").filter(brand=data)

    return render(request, 'app/mshoes.html', {"mshoes":mshoes})


@login_required
def mpants(request, data=None):
    if data == None:
        mpants = Product.objects.filter(category="MP")
    elif data == "Aatman" or data == "McHenry" or data == "Hanes":
        mpants = Product.objects.filter(category="MP").filter(brand=data)

    return render(request, 'app/mpants.html', {"mpants":mpants})


@login_required
def mhats(request, data=None):
    if data == None:
        mhats = Product.objects.filter(category="MH")
    elif data == "Missby" or data == "GUSTAVE" or data == "CLOTHERA" or data == "INFISPACE":
        mhats = Product.objects.filter(category="MH").filter(brand=data)

    return render(request, 'app/mhats.html', {"mhats":mhats})


@login_required
def meyewear(request, data=None):
    if data == None:
        meyewear = Product.objects.filter(category="MEW")
    elif data == "Lenskart" or data == "Glasskart":
        meyewear = Product.objects.filter(category="MEW").filter(brand=data)

    return render(request, 'app/meyewear.html', {"meyewear":meyewear})

#women
@login_required
def topwear(request, data=None):
    if data == None:
        topwear = Product.objects.filter(category="TW")
    elif data == "Park_Avenue" or data == "Generic" or data == "HIGHEK" :
        topwear = Product.objects.filter(category="TW").filter(brand=data)

    return render(request, 'app/topwear.html',{"topwear":topwear})

@login_required
def Chudidar(request, data=None):
    if data == None:
        Chudidar = Product.objects.filter(category="C")
    elif data == "Park_Avenue" or data == "Generic" or data == "HIGHEK" :
        Chudidar = Product.objects.filter(category="C").filter(brand=data)

    return render(request, 'app/Chudidar.html',{"Chudidar":Chudidar})


@login_required
def bottomwear(request,data=None):
    if data == None:
        bottomwear = Product.objects.filter(category="BW")
    elif data == "Lyra" or data == "V-GIRL" or data == "BlackBuck" :
        bottomwear = Product.objects.filter(category="BW").filter(brand=data)
        
    return render(request, 'app/bottomwear.html', {"bottomwear":bottomwear})

@login_required
def wshoes(request, data=None):
    if data == None:
        wshoes = Product.objects.filter(category="WS")
    elif data == "Campus" or data == "Duosoft" or data == "FLITE" :
        wshoes = Product.objects.filter(category="WS").filter(brand=data)

    return render(request, 'app/wshoes.html', {"wshoes":wshoes})


@login_required
def jewellery(request, data=None):
    if data == None:
        jewellery = Product.objects.filter(category="J")
    elif data == "Sukkhi" or data == "YouBella" or data == "ZENEME" :
        jewellery = Product.objects.filter(category="J").filter(brand=data)

    return render(request, 'app/jewellery.html', {"jewellery":jewellery})


@login_required
def saree(request, data=None):
    if data == None:
        saree = Product.objects.filter(category="S")
    elif data == "Half_Saree" or data == "Saree" or data == "Daily_Use" or data == "Lehenga" :
        saree = Product.objects.filter(category="S").filter(brand=data)

    return render(request, 'app/saree.html', {"saree":saree})


#kids
@login_required
def boy(request, data=None):
    if data == None:
        boy = Product.objects.filter(category="B")
    elif data == "Clothes" or data == "Footwears" or data == "Hats" or data == "Glasses" or data == "Watches" :
        boy = Product.objects.filter(category="B").filter(brand=data)

    return render(request, 'app/boy.html',{"boy":boy})


@login_required
def girl(request, data = None):
    if data == None:
        girl = Product.objects.filter(category="G")
    elif data == "Clothes" or data == "Footwears" or data == "Hats" or data == "Glasses" or data == "Hairbands" :
        girl = Product.objects.filter(category="G").filter(brand=data)

    return render(request, 'app/girl.html', {"girl":girl})



#search
def search(request):
    query = request.GET.get('query')
    results = []
    if query:
        query1 = query.title()
        results = Product.objects.filter(title=query1) or Product.objects.filter(brand=query1)
    context = {
        'query1': query1,
        'results': results,
    }
    return render(request, 'app/search.html', context)




from django.contrib.auth import authenticate
from django.contrib.auth import login

def designer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        designer_code = request.POST.get("designer_code")
        user = authenticate(request, username = username, password = password)
        temp = Designer.objects.filter(designer_code=designer_code)
        if user and temp:
            login(request, user)
            designer = Designer.objects.filter(username=request.user, designer_code=designer_code)
            if designer:
                return redirect( 'designer_home')
            else:
                messages.error(request,"Invalid Username or Password or Designer code")
        else:
            messages.error(request,"Invalid Username or Password or Designer code")
    return render(request, 'app/designer_login.html')



def designer_home(request):
    # designer = Designer.objects.filter(username=request.user)
    designer = get_object_or_404(Designer, username=request.user)
    # designer = Designer.objects.get(username=request.user)
    works = designer.works.all()
    if request.method == 'POST':
        form = DesignerWorksForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.designer = designer
            work.save()
            return redirect('designer_home')
        else:
            form = DesignerWorksForm()

    else:
        form = DesignerWorksForm()
    
    return render(request, 'app/designer_home.html', {'designer':designer, "works":works, "form":form})






@login_required
def designers(request, data = None):
    if data == None:
        designers = Designer.objects.all()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/designers.html', {"designers":designers, "totalitem":totalitem})





@login_required
def designer_checkout(request):
    user = request.user
    designer_id = request.GET.get('designer_id')
    designer = Designer.objects.get(id=designer_id)
    add = Customer.objects.filter(user=user)
    TempDesignerPlaced(user=user, designer=designer).save()
    already_exist = DesignerPlaced.objects.filter(user=user, designer=designer)
    totalitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    if add:
        if designer:
            return render(request, 'app/designer_checkout.html', {'add':add,'designer':designer, "totalitem":totalitem})
    else:
        return redirect('profile')


def send_mail_after_designer_booking1(email):
    subject1 = "Fashion Designer Booked Successfully"
    messages1 = "Successfully booked designers, designers will contact you through our website."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject1, messages1, from_email, recipient_list)

def send_mail_after_designer_booking2(email):
    subject2 = "You Have Received an Order."
    messages2 = "Great news! You've just received a new order for your fashion designs. Keep up the fantastic work!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject2, messages2, from_email, recipient_list)


@login_required
def payment_done_designer(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    tdp = TempDesignerPlaced.objects.filter(user=user)
    loop_executed = False
    for c in tdp:
        if not loop_executed:
            DesignerPlaced(user=user, customer=customer, designer=c.designer).save()
            TempDesignerPlaced.objects.all().delete()
            loop_executed = True
            send_mail_after_designer_booking1(user.email)
            send_mail_after_designer_booking2(c.designer.email)
    return redirect("designer_orders")


@login_required
def payment_done_buynow(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    bcart = BCart.objects.filter(user=user)
    loop_executed = False
    for c in bcart:
        if not loop_executed:   
                OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
                BCart.objects.all().delete()
                loop_executed = True
                send_mail_after_payment(user.email)
    return redirect("orders")


@login_required      
def designer_orders(request):
    op = DesignerPlaced.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        
    if op:
        return render(request, 'app/designer_orders.html', {'order_placed':op, "totalitem":totalitem})      
    else:
        return render(request,'app/emptyorder.html')


def delete_designer(request):
    if request.method == 'GET':
        des_id = request.GET['des_id']
        c = DesignerPlaced.objects.get(Q(designer=des_id)& Q(user=request.user))
        c.delete()
    return redirect('designer_orders')



@login_required      
def view_orders_designer(request):
    designer = Designer.objects.get(username=request.user)
    op = DesignerPlaced.objects.filter(designer=designer)
    if op:
        return render(request, 'app/view_orders_designer.html', {'order_placed':op})       
    else:
        return render(request,'app/designer_emptyorder.html')






from django.shortcuts import get_object_or_404
from .models import DesignerPlaced
from .forms import StatusUpdateForm

def update_status(request, designer_placed_id):
    designer_placed = get_object_or_404(DesignerPlaced, id=designer_placed_id)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            designer_placed.status = form.cleaned_data['status']
            designer_placed.save()
            return redirect('view_orders_designer')
    else:
        form = StatusUpdateForm(initial={'status': designer_placed.status})
    return render(request, 'app/update_status.html', {'form': form})

def designer_about(request):
    return render(request, "app/designer_about.html")

@login_required
def designer_contact_page(request):
    return render(request, "app/designer_contact_page.html")



# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import DesignerWorksForm
from .models import DesignerWorks

def edit_work(request, work_id):
    work = get_object_or_404(DesignerWorks, id=work_id)

    if request.method == 'POST':
        form = DesignerWorksForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            return redirect('designer_home')
    else:
        form = DesignerWorksForm(instance=work)

    return render(request, 'app/edit_work.html', {'form': form})


def delete_work(request):
    if request.method == 'GET':
        work_id = request.GET['work_id']
        c = DesignerWorks.objects.get(Q(id=work_id))
        c.delete()
    return redirect('designer_home')




# app/views.py

from django.shortcuts import render, redirect
from .forms import DesignerProfileForm

def edit_profile(request):
    designer = get_object_or_404(Designer, username=request.user)

    if request.method == 'POST':
        form = DesignerProfileForm(request.POST, request.FILES, instance=designer)
        if form.is_valid():
            form.save()
            return redirect('designer_home')

    else:
        form = DesignerProfileForm(instance=designer)

    return render(request, 'app/edit_profile.html', {'form': form})



def add_work(request):
    # designer = Designer.objects.filter(username=request.user)
    designer = get_object_or_404(Designer, username=request.user)
    # designer = Designer.objects.get(username=request.user)
    works = designer.works.all()
    if request.method == 'POST':
        form = DesignerWorksForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.designer = designer
            work.save()
            return redirect('designer_home')
        else:
            form = DesignerWorksForm()

    else:
        form = DesignerWorksForm()
    
    return render(request, 'app/add_work.html', {"form":form})


def con_adm(request):
    return render(request, 'app/con_adm.html')

