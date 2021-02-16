from sys import builtin_module_names
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search


BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/d/services/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home ( request ) :
    return render ( request , 'base.html' )


def new_search( request) :
    # save searches in datebase
    search = request.POST.get ( 'search' )
    Search.objects.create ( search = search )

    #getting craigslist
    final_url = BASE_CRAIGLIST_URL.format ( quote_plus ( search ) )
    response = requests.get ( final_url )
    data  = response.text

    #getting list
    soup = BeautifulSoup( data , features = 'html.parser' )
    post_listing = soup.find_all( 'li' , { 'class' : 'result-row' } )

    new_post = []
    
    for post in post_listing :
        post_title = post.find ('a' , class_ = 'result-title').text
        post_url  = post.find ('a').get('href')
        # Post Price
        if post.find ( class_ = 'post-price' ) :
            post_price = post.find ( class_ =  'result-price' )

        else : 
            post_price = "Price not Found"

        #Post Image
        if post.find (class_= 'result-image').get('data-ids') :
            post_id =  post.find (class_= 'result-image').get('data-ids').split ( ',' )[0].split(':')[1]
            post_image = BASE_IMAGE_URL.format ( post_id )

        else : 
            post_image = 'https://www.iobsl.org/wp-content/themes/consultix/images/no-image-found-360x250.png'


        new_post.append ( ( post_title , post_url , post_price , post_image) )
    
    context = {
        'search' : search ,
        'new_post' : new_post
    }

    return render (request , 'my_app/new_search.html' , context )




   