#coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Category,Page
from .form import CategoryForm,PageForm,UserForm,UserProfileForm
from datetime import datetime 
from tango.bing_search import run_query 
# Create your views here.
@login_required
def index(request): 

    category_list=Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]
    context_dict={'categories':category_list,'pages':page_list}

    #print   category_list 
    #print   page_list 

    #Get the number of visits to the site. 
    visits= request.session.get('visits')

    if not visits:
        visits = 1 
    reset_last_visit_time=False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time =datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")


        if(datetime.now()-last_visit_time).seconds >5:
            visits=visits+1 
            reset_last_visit_time= True  
            context_dict['visits']=visits
    else:
        #Cookie last_visit doesn't exist,so create it to the current date/time.
        reset_last_visit_time = True 
 
        #Obtain our Response object early so we can add cookie information.
        response= render(request,'tango/index.html',context_dict)

    if reset_last_visit_time: 
        request.session['last_visit']=str(datetime.now())
        request.session['visits']=visits
    context_dict['visits']=visits

    return render(request,'tango/index.html',context_dict ) 


def about(request):  
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        count =request.session.get('visits')
    else:
        count = 0 

    # Return and render the response, ensuring the count is passed to the template engine.
    return render(request,'tango/about.html', {'visits':count})
@login_required
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
        pages=Page.objects.filter(category=category).order_by('-views')
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
        #print ">>> TEST COOKIE WORKED!"
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
        #print user
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
    return HttpResponseRedirect('/tango/login')

@login_required
def search(request):
    result_list=[]

    if request.method =='POST':
        query= request.POST['query'].strip()

        if query:
            #Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request,'tango/search.html',{'result_list':result_list})


@login_required 
def track_url(request):
    page_id=None 
    url='/tango'

    if request.method=='GET': 
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            #之前不能成功是因为 objects写成了object
            try:
                page=Page.objects.get(id=page_id)
                print page
                page.views=page.views+1
                page.save()
                url=page.url
            except: 
                pass
             
    return redirect(url)


