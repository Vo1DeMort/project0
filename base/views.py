from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import RegisterForm, LoginForm, PostForm
from . models import Profile,  Post, Comment

# i am gonna show the posts of the followed users here
def home(request):
    if request.user.is_authenticated:
    # import the posts of follow users ,then render
        # fitst find out the users that the requested user follows
        # and then retrieves the posts of those users

        # retrieve the profile of requested user
        profile = request.user.profile
        # retrieve the profiles that the login user follows
        followed_profiles = profile.follow.all()
        # their posts
        posts = Post.objects.filter(owner__in=followed_profiles)

        # handle the post formif request.method == 'POST':
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                # Process the form data and create a new post
                story = form.cleaned_data['story']
                pictures = form.cleaned_data['pictures']
                new_post = Post.objects.create(
                    owner = profile,
                    story = story,
                    pictures = pictures
                )
                return redirect('home')
        else:
            form = PostForm()

        return render(request,'home.html',{'posts':posts,'form':form})
    else:
        return redirect('login')


'''
working properly, sort of ajex things will improve user experience , need to learn django channel
need to study these codes
'''
@login_required
def like_comment(request,post_id):
    # post like thing
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    # comment thing
    '''
    this might stops working, coz i am gonna change the comment and post models
    '''
    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            new_comment = Comment.objects.create(post=post, writer=request.user,comment=comment)
    comments = Comment.objects.filter(post=post).order_by('-created')

    return redirect('home') 

        

    


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


def edit_profile(request):
    # make a form and handle from this view
    pass

def send_message(request):
    pass

def start_group_chat(request):
    pass


