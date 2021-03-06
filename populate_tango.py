#coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django 
django.setup()
from tango.models import Category, Page
#以上声明不要放在name空间下  不起作用
def populate():
    python_cat=add_cat(name='Python',
        views=120,
        likes=30)

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/Tutorial/")

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    django_cat=add_cat(name="Django",
        views=122,
        likes=2
        )

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    frame_cat=add_cat(name="Other Frameworks",
        views=30,
        likes=1)

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org")

    #Print out what we have added to the user 
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat,title,url,views=0):
    p=Page.objects.get_or_create(category=cat,title=title,url=url,views=views)[0]
    #print "create page  : %s" (str(title)
    return p

def add_cat(name,views=0,likes=0):
    c=Category.objects.get_or_create(name=name)[0]
    #print "create category  : %s" (name)
    return c

#start execution here !
if __name__=='__main__':
    print "Starting Rango population script..."
    populate()