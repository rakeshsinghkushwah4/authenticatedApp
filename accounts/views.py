from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.form import RegisterForm ,UserLogin
from django.contrib.auth.models import User
from accounts.models import MyProfile
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from accounts.token_generator import account_activation_token


def register(req):
    form = RegisterForm()
    if req.method == "POST":
        form = RegisterForm(req.POST,req.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=req.POST.get('username'),password=req.POST.get('password'),email=req.POST.get('username'))
            # Here user is save but not active therefore user not login
            user.is_active = False
            print(req.POST.get('name'))
            user.myprofile.name= req.POST.get('name')
            user.myprofile.gender= req.POST.get('gender')
            user.myprofile.phone= req.POST.get('phone')
            user.myprofile.register_type= req.POST.get('register_type')
            user.myprofile.profile_pic= req.FILES.get('profile_pic')
            user.save()
            # we get the current site from the request. it return domain name like www.rakesh.com
            current_site = get_current_site(req)
            email_subject = 'Activate Your Account'
            # here we create message in the html form in the we pass user,domain,uid,token
            message = render_to_string('accounts/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('username')
            # to_email = form.POST.get('username')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
            print('rake',current_site)
    return render(req,'accounts/register.html',{'form':form})

# Here we check the given token is vaild or not if valid so user is activate
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

def user_login(req):
    form = UserLogin()
    if req.method == 'POST':
        print(req.POST)
        form = UserLogin(req.POST)
        if form.is_valid():
            # Here we check user is available in the database or not if available then is authenticate the user
            # But not set in session so because of this we can't get the info of authenticate user
            user=authenticate(username = req.POST.get('username'),password=req.POST.get('password'))
            if user is not None:
                # Here login is set the user in session. Now we get whole info of user
                login(req,user)
                return redirect('home')
            else:
                return HttpResponse('You are not authenticated')
    return render(req,'accounts/login.html',{'form':form})

def user_logout(req):
    if req.user.is_authenticated:
        logout(req)
        return redirect('home')



