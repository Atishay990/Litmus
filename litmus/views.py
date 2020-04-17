from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
#from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.urls import reverse
from django.contrib.auth.decorators import login_required

from friendship.models import Friend,Follow,Block
from friendship.models import FriendshipRequest

@login_required(login_url='/litmus/login/')
def home_view(request):
    return render(request,'litmus/home.html')

def index(request):
    #return render(request,'litmus/front-page.html')
    return render(request, 'litmus/index.html', {'signup_form': SignUpForm()})


@login_required(login_url ='/litmus/login/')
def logout_view(request):
    logout(request)
    return render(request,'litmus/logout.html')

def activation_sent_view(request):
    return render(request,'litmus/activation_sent.html')

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request,user)
        return redirect('home')
    else:
        return render(request,'litmus/activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.nick_name = form.cleaned_data.get('nick_name')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('e_mail')
            #user.profile.email = form.cleaned_data.get('email')
            #user.profile.password1 = form.cleaned_data.get('password1')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template()
            # and calls its render() method immediately.
            message = render_to_string('litmus/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('e_mail')
            email = EmailMessage(subject,message,to=[to_email])
            email.send()

            #user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'litmus/front-page.html', {'signup_form': SignUpForm()})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
                #return redirect('home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            #print("They used email: {} and password: {}".format(email,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'litmus/login.html', {})

def send_friend_request(request):

    if request.method == 'POST':
        friend_email = request.POST.get('email')
        usid = User.objects.get(email=friend_email).id
        other_user = User.objects.get(pk=usid)
        Friend.objects.add_friend(
        request.user,other_user,message='Hi!! Wanna hang in.')
        return HttpResponse("Friend request sent")

    else:
        return render(request,'litmus/send_friend_request.html')

def receive_friend_request(request):
    usid = User.objects.get(email=request.user.email).id
    friend_request = FriendshipRequest.objects.get(to_user=usid)
    friend_request.accept();
    return HttpResponse("Friend request accepted")

def incoming_friend_request(request):
    return render(request,'litmus/friend_request.html')

def show_friends(request):
    list = Friend.objects.friends(request.user)
    return render(request,'litmus/show_friends.html',{'list':list})
