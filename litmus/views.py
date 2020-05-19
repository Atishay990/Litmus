from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text

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

from .graphMap import friendGraph
f  = friendGraph()

from. models import Notes ,Profile
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


""" decorators for pages that requires login of authorised user """

@login_required(login_url='/litmus/signup/')
def home_view(request):
    friendDict={}
    my_email = request.user.email
    email_list = f.pendingFriendRequest(my_email)
    name_list=[]
    for friend in email_list:
        name_list.append(User.objects.get(email=friend).profile.first_name)
    
    friendDict = dict(zip(name_list,email_list))

    #return render(request,'litmus/notes2.html')
    return render(request,'litmus/notes2.html',{'friendDict':friendDict})


def add(request):
    # Saving newly added notes from the homepage 
    title = request.GET.get('title')
    newnote = request.GET.get('newnote')
    Public = request.GET.get('view')
    date = timezone.now()
    user_id = User.objects.get(email=request.user.email).id
    user_profile = get_object_or_404(Profile, pk = user_id)
    n = Notes()
    n.user_profile = user_profile
    n.note_title = title
    n.note_body = newnote
    n.create_time = date
    if(Public=="True"):
        n.is_public = True

    n.save()
    #latestnote = n.diary_notes
    return HttpResponse("successful")
    #return redirect('/litmus/homepagedemo/' + str(user_id) + '/')

def show_notes(request):
    try:
        # Selecting the latest note
        user_id = User.objects.get(email=request.user.email).id
        all_notes = Notes.objects.filter(user_profile = user_id)
        all_notes = list(all_notes)
        first_name = User.objects.get(email=request.user.email).profile.first_name
        last_name = User.objects.get(email=request.user.email).profile.last_name
        name = first_name+" "+last_name
        #if len(all_notes) == 0:
        #    return redirect('litmus/homepagedemo/errors/400/')
        all_notes.sort(key = lambda x : datetime.strptime(str(x.create_time), '%Y-%m-%d %H:%M:%S.%f%z'), reverse = True)
        #latestnote = all_notes[0].diary_notes
        #print(latestnote)
        f_list = f.friend_list(request.user.email)
        name_list=[]
        for friend in f_list:
            name_list.append(User.objects.get(email=friend).profile.first_name)

        return render(request, 'litmus/posts.html', 
                     {'all_notes': all_notes,'name':name,'f_list':name_list})
    except(KeyError, Notes.DoesNotExist):
        latestnote = 'No notes yet! Go ahead and create your first note !'
        
    else:
        # Passing selected note tobe displayed on basic HTML page
        return HttpResponse("No notes to show")


def errors(request, error_code):
    print("Hey here\n\n")
    return render(request, 'homepage/homepageerror.html', 
                 {'error_code' : error_code,})   

def index(request):
    #return render(request,'litmus/front-page.html')
    return render(request, 'litmus/index.html', {'signup_form': SignUpForm()})


def friend_posts(request):
    friends = f.friend_list(request.user.email)
    posts = []
    #user_id = User.objects.get(email=friend).id
    #user_profile = get_object_or_404(Profile, pk = user_id)
    for friend in friends:
        #name = User.objects.get(email=friend).profile.first_name
        #names.append(name)
        user_id = User.objects.get(email=friend).id
        user_profile = get_object_or_404(Profile, pk = user_id)
        models = Notes.objects.filter(user_profile = user_profile)
        for model in models:
           if(model.is_public== True):
              # posts.append(model.note_title)
              #author.append(name)
              posts.append(model)
        
    #post_dict = [[post for post in posts]  for name in names]
   # print(author)
   # print(posts)
    #print(names)
    #print(post_dict)
    return render(request,"litmus/all_posts.html",{'posts':posts})


@login_required(login_url ='/litmus/login/')
def logout_view(request):
    logout(request)
    #return render(request,'litmus/logout.html')
    return redirect('home')
    #return HttpResponse("logged out")

def activation_sent_view(request):
    return render(request,'litmus/activation_sent.html')

""" function that is called when user clicks on the links that is generated in the mail for final registraion"""

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

""" This function is called when user clicks on sign up button"""

#@csrf_exempt
def signup_view (request):
    if request.method  == 'POST':
        if request.POST.get('submit')=='register':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('e_mail')
               
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
                #method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
             })
                to_email = form.cleaned_data.get('e_mail')
                email = EmailMessage(subject,message,to=[to_email])
                email.send()

                #user.email_user(subject, message)
                return redirect('activation_sent')
            
        elif request.POST.get('submit') == 'login':
            print("login ka mudda")
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
        form = SignUpForm()
        return render(request, 'litmus/front-page.html', {'signup_form': SignUpForm()})

        


def send_friend_request(request):

    #if request.method == 'POST':
    friend_email = request.GET.get('email') # gets email entered by user to whom friend request has to be send
    my_email  = request.user.email
    f.sendFriendRequest(my_email,friend_email)
    print(friend_email)
    return render(request,'litmus/send_friend_request.html')
    #return HttpResponse("Friend request sent")   #Sends friends request

    #else:
    #    return render(request,'litmus/send_friend_request.html')

def accept_friend_request(request): 
    if request.method == 'GET':
        friend_email = request.GET.get('friend_email')
        my_email = request.user.email
        print(friend_email)
        f.acceptFriendRequest(friend_email,my_email)
        return HttpResponse("friend request accepted")
        


def incoming_friend_request(request):
    friendDict={}
    my_email = request.user.email
    email_list = f.pendingFriendRequest(my_email)
    name_list=[]
    for friend in email_list:
        name_list.append(User.objects.get(email=friend).profile.first_name)
    
    friendDict = dict(zip(name_list,email_list))

    
    #print(name)
    #list = Friend.objects.unrejected_requests(request.user.email)
    return render(request,'litmus/notes2.html',{'friendDict':friendDict}) #Rendering friend requests yet to be accepted

def show_friends(request):
    list = f.friend_list(request.user.email)
    return render(request,'litmus/show_friends.html',{'list':list}) # rendering template for showing list of friend
