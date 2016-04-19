from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Category,Page
from .form import CategoryForm,PageForm,UserForm,UserProfileForm
from datetime import datetime 
# Create your views here.
def index(request):
    #return HttpResponse( "Tango says hey the world!")
    #context_dict={'boldmessage':"I am bold font from the context"}
    #return render(request,'tango/index.html',context_dict) 
    category_list=Category.objects.all()
    page_list=Page.objects.order_by('-view')[:5]
    context_dict={'categories':category_list,'pages':page_list}

    #Get the number of visits to the site.
    #We use the COOKIES.get() function to obtain the visits cookie.
    #If the cookie exists,the value returned is casted to an integer.
    #If the cookie doesn't exist,we default to zero and cast that.
    visits=int(request.COOKIES.get('visits','1'))
    #print visits 
    reset_last_visit_time=False
    context_dict['visits']=visits
    response = render(request,'tango/index.html',context_dict)

    #request.session.set_test_cookie()
    if 'last_visit' in request.COOKIES:
        #Yes it does! Get the cookie's value.
        last_visit =request.COOKIES['last_visit']
        print last_visit[:19]
        #Cast the value to a Python date/time object.
        last_visit_time=datetime.strptime(last_visit[:19],"%Y-%m-%d %H:%M:%S")
        print 'a'

        #If it's been more than a day since the last visit...
        if(datetime.now()-last_visit_time).seconds >5:
            visits=visits+1
            #...and flagthat the cookie last visit needs to be updated
            reset_last_visit_time= True 
            print 'b visits+1' 
            context_dict['visits']=visits
        response= render(request,'tango/index.html',context_dict)
    else:
        #Cookie last_visit doesn't exist,so flag that it should be set.
        reset_last_visit_time = True 
        print 'c'

        #Obtain our Response object early so we can add cookie information.
        response= render(request,'tango/index.html',context_dict)

    if reset_last_visit_time:
        response.set_cookie('last_visit',datetime.now())
        response.set_cookie('visits',visits)
        print 'd'
    
     
    #print context_dict['visits']
    #liucheng:   a  /  a b d / c d 
    #Return response back to the user,updating any cookies that need changed. 
    return response 


def about(request):
    #return render(request,'tango/index.html','Hello,I\'m tango.')
    return HttpResponse('Tango says:Here is the about page. <a href="/tango/">Index</a>')

def category(request,category_name_slug):
    #Create a context dictionary which we can pass to the template rendering engine.
    context_dict={}
    try:
        #Can we find a category name slug with the given name?
        #If we can't,the .get() method raises a DoesNotExist exception.
        #So the .get() method returns one model instance or raises an exception.
        category=Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        #Retrieve all of the associated pages.
        #Note that filter returns >=1 model instance.
        pages=Page.objects.filter(category=category) 
        #Adds our results list to the template context under name pages .
        context_dict['pages']=pages
        #We also add the category object from  the databse to the context dictionary.
        #We'll use this in the template to verify that the category exists.
        context_dict['category']=category
    except Category.DoesNotExist:
    #We get here if we didn't find the specified category.
    #Don't do anything -  the template displays the "no category" massage for us.
        pass

    #Go render the response and return it to the client.
    return render(request,'tango/category.html',context_dict)
@login_required
def add_category(request):
    #A HTTP POST?
    if request.method =='POST':
        form = CategoryForm(request.POST)

        #Have we been provided with a valid form?
        if form.is_valid():
            #Save the new category to the database.
            form.save(commit=True)

            #Now call the index() view.
            #The user will be shown the homepage.
            return index(request)
        else:
            #The supplied  form contained errors -just print them to the terminal.
            print form.errors
    else:
        #If the request war not a POST, display the form to enter details.
        form=CategoryForm()

    #Bad form (or form details),no form supplied...
    #Render the form with error messages (if any).
    return render(request,'tango/add_category.html',{'form':form})
@login_required
def add_page(request, category_name_slug):
    #context = RequestContext(request)
    #cat_list = get_category_list()
    context_dict = {}
    try:
        cat=Category.objects.get(slug=category_name_slug)
        print cat 
    except Category.DoesNotExist:
        cat=None
 
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.save()
                #probably better to use a redirect here.
                return category(request,category_name_slug)
            else:
                print form.errors
        else:
            form = PageForm()
    else:
        form = PageForm()
    context_dict['category_name_url']=category_name_slug
    context_dict['form']=form 

    return render(request,'tango/add_page.html',context_dict)

def register(request):
    
    if request.session.test_cookie_worked():
        print ">>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()
    #Aboolean value for telling the template whether the registration was successful.
    #Set to False initially.Code changes value to True when retgistration succeeds.
    registered =False

    #If it's a HTTP POST, we're interested in processing form data.
    if request.method =='POST':
        #Attempt to grab information from the raw form information.
        #Note that we make use of both UserForm and UserProfileForm.
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)

        #If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #Now we hash the password with the set_password method.
            #Once hashed,we can update the user object.
            user.set_password(user.password)
            user.save()

            #Now sort out the UserProfiles instance 
            #Since we need to set the user attribute ourselves,we set commit=False.
            #This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user 

            #Did the user provide a profile picture?
            #If so,we need to  get it from the input form and put it in the UserProfiles model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #Now we save the UserProfile model instance.
            profile.save()

            #Update our variable to tell the template registration was successful.
            registered = True
        #Invalid form or forms - mistakes or something else?
        #Print problems to  the terminal.
        #They'll also be shown to the user.
        else:
            print user_form.errors,profile_form.errors
    else:
        user_form = UserForm()
        profile_form=UserProfileForm()

    #Render the template depending  on the context.
    return render(request,
        'tango/register.html',
        {'user_form':user_form,'profile_form':profile_form,'registered':registered})
def user_login(request):
    #If the request is a http POST,try to pull out the relevant information.
    if request.method=='POST':
        #Gather the username and password provided by the user.
        #This information is obtained from the login form.
        username = request.POST.get('username')
        password = request.POST.get('password') 
        #Use Django's machinery to attempt to see if the username/password
        #combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        print user
        #If we have a User object,the details are correct.
        #If None,no user
        #with matching credentials was found.
        if user:
            #Is the account active? It could have been disabled.
            if user.is_active:
                #If the account is valid and active,we can log the user in.
                #We'll send the user back to the homepage.
                login(request,user)
                return HttpResponseRedirect('/tango/')
            else:
                #An inactive account was used - no logging in!
                return HttpResponse("Your Tango account is disabled.")
        else:
            #Bad Login details were provided.So we can't log the user in.
            print "Invalid login details:{0},{1}".format(username,password)
            return HttpResponse("Invalid login details supplied.") 
            #return render(request,'/tango/login.html',{'warn':'User or Password is wrong!'})
    #The request is not a HTTP POST,so display the login form.
    #This scenario would most likely be a HTTP GET.
    else:
        #No context variable to pass to  the template system,hence t he 
        #blank dictionary object...
        return render(request,'tango/login.html',{})
# def some_view(request):
#     if not request.user.is_authenticated():
#         return HttpResponse("You are logged in.")
#     else:
#         return HttpResponse("You are not logged in.")
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in,you can see this text!")

@login_required
def user_logout(request):
    #Since we know the user is logged in,we can now just log them out.
    logout(request)

    #Take the user back to the homepage.
    return HttpResponseRedirect('/tango')
