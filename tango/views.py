from django.shortcuts import render
from django.http import HttpResponse
from .models import Category,Page
from .form import CategoryForm
# Create your views here.
def index(request):
    #return HttpResponse( "Tango says hey the world!")
    #context_dict={'boldmessage':"I am bold font from the context"}
    #return render(request,'tango/index.html',context_dict)
    category_list=Category.objects.order_by('-likes')[:5]
    context_dict={'categories':category_list}
    return render(request,'tango/index.html',context_dict)

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
    