from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import shutil
import re
import os
import random
import string

from arba.settings import BASE_DIR
from arba_app.models import products, usermember,cart1,categories
# Create your views here.

def first(request):
    return render(request,'login.html')

def login_fun(request):
    return render(request,'login.html')

def user_fun(request):
    us=request.user
    print(us.id)
    user = usermember.objects.get(user_id=us.id)
    prod = products.objects.filter(user_id=us.id)
    prod_num = products.objects.filter(user_id=us.id).count()
    number=cart1.objects.filter(user_id=us.id).count()
    return render(request,'home.html',{'det':user,'products':prod,'pro_num':prod_num,'number':number})

def admin_fun(request):
    return render(request,'adminpage.html')
def signup_fun(request):
    return render(request, 'signup.html')

def forgot_password(request):
    return render(request, 'forgetpass.html')


def user_login(request):
    try:
        if request.method == 'POST':
            try:
                username = request.POST['uname']
                password = request.POST['upass']
                
                user = auth.authenticate(username=username, password=password)
                
                
                if user is not None:
                    if user.is_superuser:
                        print('hello')
                        auth.login(request, user)
                        return redirect('admin_fun')
                    else:
                        auth.login(request, user)
                        return redirect('user_fun')
                else:
                    messages.info(request, 'Invalid username or password')
                    return redirect('login_fun')
            except:
                messages.info(request, 'Invalid username or password')
                return redirect('login_fun')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login_fun')
        
    except:
        return redirect('login_fun')
    

def user_create(request):
    if request.method == 'POST':
        username=request.POST.get('uname')
        name=request.POST.get('fname')
        email=request.POST.get('email')
        password=request.POST.get('upass')
        cpassword=request.POST.get('ucpass')
        image='/static/image/default.png'
        
        
        a,b,c,d,i= 0,0,0,0,0
        capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        smallalphabets="abcdefghijklmnopqrstuvwxyz"
        specialchar="!#$%&()@*+,-./:;<=>?@[\]^_`{|}~"
        digits="0123456789"

        if (len(password) >= 6):
            for i in password:
                if (i in smallalphabets):
                    a+=1
                if (i in capitalalphabets):
                    b+=1
                if (i in digits):
                    c+=1
                if(i in specialchar):
                    d+=1
            if (a>=1 and b>=1 and c>=1 and d>=1 and a+b+c+d==len(password)):
                if password==cpassword:
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'This Username already exists')
                        return redirect('signup_fun')
                    else:
                        target = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[COM|com]{2,3})+')
                        if re.fullmatch(target, email):
                            user = User.objects.create_user(
                                first_name=name,
                                username=username,
                                password=password,
                                email=email
                            )
                            user.save()
                        else:
                                messages.info(request, 'This email is invalid')
                                return redirect('signup_fun')
                else:
                    messages.info(request, 'Password not matching')
                    return redirect('signup_fun')
            else:
                messages.info(request, 'Password Parmeters were not met')
                return redirect('signup_fun')
        else:
            messages.info(request, 'Password must have atleast 6 characters')
            return redirect('signup_fun')
        
        u = User.objects.get(id=user.id)
        userprofile = usermember(user=u,user_image=image)
        userprofile.save()
        subject = 'WE-STORE Welcome aboard'
        body = 'HI this is a automated mail. WE-STORE welcomes you to its new e-Platform for online purchasing goods. \n \n---Username---> '+ username  +' \n \n You can change your profile in your login.'    
        send_mail(subject,body, settings.EMAIL_HOST_USER, [email])
        return redirect('login_fun')
    return render(request, 'signup.html')
        

def forget_pass_fun(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        if User.objects.filter(username=username,email=email).exists():
            
            u = User.objects.get(username=username,email=email)
            print(u)
            characters = string.ascii_letters + string.digits +string.punctuation
            password = ''.join(random.choice(characters) for i in range(8))
            u.set_password(password)
            u.save()
            
            subject = 'WE-STORE Support'
            body = 'HI this is an automated mail. We noticed you initialized password generation. New password is as follow: \n \n---Password---> '+ password  +' \n \n You can change your profile in your login.'    
            send_mail(subject,body, settings.EMAIL_HOST_USER, [email])
            messages.info(request, 'Password Changed')
            return redirect('login_fun')
        else:
            messages.info(request, 'This Username mail does not exist')
            return redirect('forgot_password')
        
        

def accept(request):
    us=request.user
    a = usermember.objects.get(user_id=us.id)
    a.user_accepter=1
    a.save()
    return redirect('user_fun')

def cancel_profile_pop(request):
    return redirect('profile_fun')

def select_profile_pop(request):
    if request.method == 'POST':
        us=request.user
        image=request.POST.get('img')
        existing_directory="D:/django/arba/static"
        source=existing_directory+image
        tobe_directory="D:/django/arba/media"
        destination=tobe_directory+image
        a="True"
        if(os.path.exists(destination)==a):
            user=usermember.objects.get(user_id=us.id)
            user.user_image=image
            user.save()
        else:
            shutil.copy(source,destination)
            user=usermember.objects.get(user_id=us.id)
            user.user_image=image
            user.save()
        
        
        return redirect('profile_fun')


def allproduct_fun(request):
    us=request.user
    print(us)
    user = usermember.objects.get(user_id=us.id)
    prod = products.objects.all()
    number=cart1.objects.filter(user_id=us.id).count()
    return render(request,'allpro.html',{'det':user,'products':prod,'number':number})

def profile_fun(request):
    us=request.user
    user = usermember.objects.get(user_id=us.id)
    number=cart1.objects.filter(user_id=us.id).count()
    return render(request,'user_profile.html',{'det':user,'number':number})

def edit_profile(request,id):
    name = request.POST.get('fname')
    user=User.objects.get(id=id)
    user.first_name=name
    user.save()
    return redirect('profile_fun')

def password_change_fun(request):
    u=request.user
    user=usermember.objects.get(user_id=u.id)
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request,'password_change.html',{'det':user,'number':number})

def edit_password(request,id):
    if request.method=='POST':
        print('hi')
        us=request.user
        u=User.objects.get(id=id)
        oldp=request.POST.get('opass')
        newp=request.POST.get('npass')
        confirmp=request.POST.get('cpass')
        
        try:
            if us.check_password(oldp):
                if newp==confirmp:
                    a,b,c,d,i= 0,0,0,0,0
                    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    smallalphabets="abcdefghijklmnopqrstuvwxyz"
                    specialchar="!#$%&()@*+,-./:;<=>?@[\]^_`{|}~"
                    digits="0123456789"

                    if (len(newp) >= 6):
                        for i in newp:
                            if (i in smallalphabets):
                                a+=1
                            if (i in capitalalphabets):
                                b+=1
                            if (i in digits):
                                c+=1
                            if(i in specialchar):
                                d+=1
                        if (a>=1 and b>=1 and c>=1 and d>=1 and a+b+c+d==len(newp)):
                            us.set_password(newp)
                            us.save()
                            messages.info(request, 'Password is changed successfully')
                            return redirect('login_fun')
                        else:
                            messages.info(request, 'Password Parmeters were not met')
                            return redirect('profile_fun')
                    else:
                            messages.info(request, 'Password must be at least 6 digits')
                            return redirect('profile_fun')
                else:
                    messages.info(request, 'Password confirmed are not equal')
                    return redirect('profile_fun')
            else:
                messages.info(request, 'Old Password is not matching')
                return redirect('profile_fun')
        except:
            pass
        return redirect('profile_fun')
    
    
def adding_product_fun(request,slug):
    u=request.user
    user=usermember.objects.get(user_id=u.id)
    product=products.objects.get(pro_slug=slug)
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request,'add_product.html',{'product':product,'det':user,'number':number})

def add_to_cart(request,id):
    u=request.user
    qty=request.POST.get('qty')
    pro = products.objects.get(id=id)
    crt=cart1()
    crt.product=pro
    crt.user=u
    crt.qty=qty
    crt.save()
    return redirect('user_fun')

def prod_cart(request):
    u=request.user
    user=usermember.objects.get(user_id=u.id)
    car=cart1.objects.filter(user_id=u.id)
    car_off=cart1.objects.all()
    number=cart1.objects.filter(user_id=u.id).count()
    total=0
    for x in car:
        price=products.objects.get(id=x.product_id)
        a=x.qty
        xtotal=(price.price)*a
        total+=xtotal
    
    return render(request,'cart.html',{'det':user,'cart':car,'number':number,'total':total})


def update_qty1(request,id):
    u=request.user
    car=cart1.objects.get(id=id,user_id=u.id)
    if car.qty == 1:
        car.qty = 1
        car.save()
        return redirect('prod_cart')
    else:
        car.qty=car.qty-1
        car.save()
        return redirect('prod_cart')

def update_qty2(request,id):
    u=request.user
    car=cart1.objects.get(id=id,user_id=u.id)
    car.qty=car.qty+1
    car.save()
    return redirect('prod_cart')
    
    
def delete_cart(request,id):
    cart=cart1.objects.get(id=id)
    cart.delete()
    return redirect('prod_cart')
    
def store_fun1(request):
    u=request.user
    user = usermember.objects.get(user_id=u.id)
    cat = categories.objects.filter(user_id=u.id)
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request,'my_store_category.html',{'det':user,'category':cat,'number':number})

def store_fun2(request):
    u=request.user
    user = usermember.objects.get(user_id=u.id)
    prod = products.objects.filter(user_id=u.id)
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request,'my_store_product.html',{'det':user,'products':prod,'number':number})


def edit_category_fun(request,slug):
    u=request.user
    user = usermember.objects.get(user_id=u.id)
    cat=categories.objects.get(cat_slug=slug)
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request,'edit_category.html',{'det':user,'cat':cat,'number':number})

def edit_product_fun(request,slug):
    u=request.user
    user = usermember.objects.get(user_id=u.id)
    pro=products.objects.get(pro_slug=slug)
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request,'edit_product.html',{'det':user,'pro':pro,'number':number})





def edit_category(request,id):
    if request.method == 'POST':
        cat=categories.objects.get(id=id)
        cat_name=request.POST.get('cname')
        photo=request.FILES.get('img')
        
        cat.cat_name=cat_name
        if photo is not None:
            file=cat.image.path
            path=os.path.join("D:/django/arba/",file)
            os.remove(path)
            cat.image=photo
        else:
            pass
        cat.save()
        return redirect('store_fun1')
    return redirect('store_fun1')

def edit_product(request,id):
    if request.method == 'POST':
        pro=products.objects.get(id=id)
        title=request.POST.get('title')
        desc=request.POST.get('desc')
        price=request.POST.get('price')
        photo=request.FILES.get('image12')
        
        pro.title=title
        pro.description=desc
        pro.price=price
        if photo is not None:
            file=pro.pro_image.path
            path=os.path.join("D:/django/arba/",file)
            os.remove(path)
            pro.pro_image=photo
        else:
            pass
        pro.save()
        return redirect('store_fun2')
    return redirect('store_fun2')



def delete_category_fun(request,id):
    cat=categories.objects.get(id=id)
    if cat.image == '/static/image/default.png':
        pro=products.objects.filter(cat_id=id)
        pro.delete()
        cat.delete()
        return redirect('store_fun1')
        
    else:
        file1=cat.image.path
        path=os.path.join("D:/django/arba/",file1)
        os.remove(path)
        pro=products.objects.filter(cat_id=id)
        for p in pro:
            file2=p.pro_image.path
            path=os.path.join("D:/django/arba/",file2)
            os.remove(path)
        pro.delete()
        cat.delete()
        return redirect('store_fun1')
    
def delete_product_fun(request,id):
    pro=products.objects.get(id=id)
    if pro.pro_image == '/static/image/default.png':
        pro.delete()
        return redirect('store_fun2')
        
    else:
        file=pro.pro_image.path
        path=os.path.join("D:/django/arba/",file)
        os.remove(path)
        pro.delete()
        return redirect('store_fun2')
    
    
def category_add_fun(request):
    u=request.user
    user=usermember.objects.get(user_id=u.id)
    cat=categories.objects.all()
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request,'category_add.html',{'det':user,'category':cat,'number':number})

def add_category(request):
    if request.method == 'POST':
        u=request.user
        user=usermember.objects.get(user_id=u.id)
        name=request.POST.get('cname')
        
        if (request.FILES.get('image')) is not None:
            photo=request.FILES.get('image')
        else:
            photo='/static/image/default.png'
        
        cati=categories()
        cati.cat_name=name
        cati.image=photo
        cati.user=u
        cati.save()
        return redirect('store_fun1')
    return redirect('store_fun1')
            
            
def product_add_fun(request):
    u=request.user
    user=usermember.objects.get(user_id=u.id)
    cat=categories.objects.all()
    number=cart1.objects.filter(user_id=u.id).count()
    return render(request, 'product_add.html',{'det':user,'category':cat,'number':number})

def add_product(request):
    if request.method == 'POST':
        u=request.user
        title=request.POST.get('title')
        cat_id=request.POST.get('category')
        cat=categories.objects.get(id=cat_id)
        price=request.POST.get('price')
        if cat_id=="":
            messages.info(request, 'No Category Option Selected')
            return redirect('store_fun2')
        else:
            desc=request.POST.get('desc')
            if (request.FILES.get('image')) is not None:
                photo=request.FILES.get('image')
                pro=products()
                pro.title=title
                pro.description=desc
                pro.pro_image=photo
                pro.user=u
                pro.cat=cat
                pro.price=price
                pro.save()
                return redirect('store_fun2')
            else:
                photo='/static/image/default.png'
                pro=products()
                pro.title=title
                pro.description=desc
                pro.pro_image=photo
                pro.user=u
                pro.cat=cat
                pro.price=price
                pro.save()
                return redirect('store_fun2')
    return redirect('store_fun2')
                
        
        
    
    
    


        
    





def logout(request):
    auth.logout(request)
    return redirect('login_fun')
        
def test(request):
    email_d = 'jtom'
    u = User.objects.all()
    old='jerry'
    print(u)
    return redirect('login_fun')
    