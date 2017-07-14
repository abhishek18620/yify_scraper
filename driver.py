#------------------------------------imports--------------------------------------------------------#
import sys,subprocess,json,getopt,os,re
try:
    from urllib import request as request_module
    from urllib.request import URLError
except ImportError:
#    print("Couldn't find urllib.Request, will use urllib2")
    import urllib2 as request_module
    from urllib2 import URLError


import json
import urllib.request as req
import requests
from lxml import html   
from bs4 import BeautifulSoup
from data import genre
import csv
import pandas as pd

num=1
url=" https://yts.ag/api/v2/list_movies.json?"
mov_url="https://yts.ag/movie/"
#imdb_url="http://www.omdbapi.com/?apikey=f52fc50f&i=tt4776998"
#tmdb_url="http://api.rottentomatoes.com/api/public/v1.0.json?apikey=ddjx9e9kenwzp5ggmb5bapt2"
#comm_url="https://yts.ag/api/v2/movie_comments.json?movie_id=6612"
#resp=req.urlopen("http://api.rottentomatoes.com/api/public/v1.0.json?apikey=ddjx9e9kenwzp5ggmb5bapt2")
#prereq = req.Request(url,data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
df_list=list()
dict={'review' : "something" , 'rating' : 9.2 , 'year' : 2017 , 'runtime': 122 , 'genre_score' : 1.22}
df=pd.DataFrame(columns=('review','rating','year','runtime','genre_score'))

def scraper(page):
    global num
    new_url="{0}page={1}&limit=50".format(url,page)
    #print(new_url)
    prereq=request_module.Request(new_url,None,headers={'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'})
    #print(prereq)
    req=request_module.urlopen(prereq)
    resp=req.read().decode() # read, decode and json.load it
    jsondict=json.loads(resp)
    
    #jsondict=scrape("https://yts.ag/api/v2/movie_reviews.json?movie_id=6624")
    #print(jsondict)
    #print(genre)
    for attr in jsondict['data']['movies']:
        #print(attr['rating'],' ',attr['year'],' ',attr['runtime'], ' ', attr['genres'])
        dict['rating']=attr['rating']
        dict['year']=attr['year']
        dict['runtime']=attr['runtime']
    
        #GENRE SCORE CALCULATOR
        score=0.0
        ctr=0
        for j in attr['genres']:
            score=score+genre[str.lower(j)]
            ctr=ctr+1
        score=score/ctr
        dict['genre_score']=score

        #SCRAPE YIFY REVIEWS 
        page=requests.get(mov_url+attr['slug'])
        soup = BeautifulSoup(page.content, 'html.parser')
        ps=soup.findAll(id="movie-reviews")
        if ps:
            first=ps[0]
            ids=first.findAll('p')
            if ids:
                rev=ids[0].get_text()
                print('success    {0}'.format(num))
                num=num+1
                dict['review']=rev
            else:
                dict['review']="no reviews"
        else:
            dict['review']='nothing'
        df_list.append(dict.copy())
    #for ids in first.findAll('p'):
        #print(ids.get_text())
    ##print(first.find(id='p'))
    ##print(first.findAll('p'))
    #if ctr==1:
        #break

    #print(num)
    #for y in attr:
        #print(y ,' ---> {0}'.format(attr[y]))
    
    #mov_id=attr['id']
    #print(mov_id)
    #comm_new_url=comm_url + "?movie_id="+str(mov_id)
    #print(comm_new_url)
    #comm_dict=scrape(comm_new_url)
    #print(comm_dict)
    #print (' : {0}'.format(jsondict[x]))
if __name__=='__main__':
    for ind in range(1,20):
        scraper(ind)
    df = pd.DataFrame(df_list)
    df.to_csv("my.csv", sep=',')    
#data = json.load(req.urlopen(url))
#print(data)