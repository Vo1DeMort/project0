from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import RegisterForm, LoginForm
from . models import Profile

# i am gonna show the posts of the followed users here
def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return redirect('login')



'''
authentication failed , only the super user is authenticated
registeration fialed, i gott write my own ,this snippet is from bookmarks,which user settings.authuser instead of User

the issuse is setting user name ,space is not allowed ,eg ,test_user is allowed but not test user
How do i solve this ??

logic is working expected ,except that underscored thing

!! dear god i need a rubber duck

i could use a message to tell registration fialed and why or success ,with django message
'''
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # do the password hashing
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # create a profile for the registered user
            new_profile= Profile(user=new_user)
            new_profile.save()
            auth_user = authenticate(
                request,
                username= new_user.username,
                # used the  hashed password
                password= form.cleaned_data['password'] 
            )
            if auth_user:
                login(request,auth_user)
        return redirect('home')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})


def login_user(request):
    if request.method == 'POST':
        # instantiated from forms, this form is form ,not model form
        # means manual data processing and persistance is required
        form = LoginForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['username'],pasthe sword

            # both username and password is stored in cd
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            # means if the user exists
            if user is not None:
                # check if the user is active and allowed to login and perform certain actions with the system 
                if user.is_active:
                    # simply login the user
                    login(request, user)
                    messages.success(request,('login success'))
                    return redirect('home')
                else:
                    return redirect('login')
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
	logout(request)
	messages.success(request, ("logout success"))
	return redirect('home')


def profile(request):
    # retirieve profile infos 
    #profile = Profile.objects.get(user=request.user)
    profile = get_object_or_404(Profile, user=request.user)
    # retrieve posts
    posts = profile.post_set.all()
    # comments need to be retrieved !!

    return render (request,'profile.html',{'profile':profile,'posts':posts})

def make_post(request):
    pass

def edit_profile(request):
    pass

def send_message(request):
    pass

def start_group_chat(request):
    pass


