#------------------------------------imports--------------------------------------------------------#
try:
    from urllib import request as request_module
    from urllib.request import URLError
except ImportError:
    print("Couldn't find urllib.Request, will use urllib2")
    import urllib2 as request_module
    from urllib2 import URLError


import json
import urllib.request as req
import requests
from lxml import html   
from bs4 import BeautifulSoup as bsp        #HOW CAN A SOUP BE BEAUTIFUL...WEIRD NAME !!!
from data import genre
import csv
import time
import pandas as pd

df_list=list()
class scraper():
    #imdb_url="http://www.omdbapi.com/?apikey=f52fc50f&i=tt4776998"
    #tmdb_url="http://api.rottentomatoes.com/api/public/v1.0.json?apikey=ddjx9e9kenwzp5ggmb5bapt2"
    #comm_url="https://yts.ag/api/v2/movie_comments.json?movie_id=6612"
    #resp=req.urlopen("http://api.rottentomatoes.com/api/public/v1.0.json?apikey=ddjx9e9kenwzp5ggmb5bapt2")
    #prereq = req.Request(url,data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    
    #LAME YIFY REVIEW SCRAPER
    global df_list
    def lame_scraping(self , slug, title):
        page=requests.get(self.mov_url+slug)
        soup = bsp(page.content, 'html.parser')
        ps=soup.findAll(id="movie-reviews")
        if ps:
            review_class=ps[0]
            #all reviews are in p tags
            #open a browser and just inspect the review element
            ids=review_class.findAll('p')
            if ids:
                rev=ids[0].get_text()
                print('success    {0} with {1}'.format(self.num , title))
                self.num=self.num+1
                self.dict['review']=rev
            else:   # SHOULD BE LEFT FOR R AND ITS SHITTY STUDIO
                self.dict['review']="no reviews"
        else:
            self.dict['review']='nothing'  
        
    def genre_score_calc(self,genres):
        score=0.0
        ctr=0
        for j in genres:
            score=score+genre[str.lower(j)]
            ctr=ctr+1
        score=score/ctr
        self.dict['genre_score']=score        
        
    def heart(self , page , limit):
        #appending not working here
        ind=0
        new_url="{0}page={1}&limit={2}".format(self.url,page,limit)
        #print(new_url)
        prereq=request_module.Request(new_url,None,headers={'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'})
        #print(prereq)
        req=request_module.urlopen(prereq)
        resp=req.read().decode() # read, decode and json.load it
        #GOTTA TAKE JSON IN
        jsondict=json.loads(resp)
        
        #-------------------------------->debug<---------------------------
        #for attr in jsondict['data']['movies']:
            #for y in attr:
                #print('{0} ---> {1}'.format(y,attr[y]))
        #------------------------------------------------------------------
        
        for attr in jsondict['data']['movies']:
            #print(attr['rating'],' ',attr['year'],' ',attr['runtime'], ' ', attr['genres'])
            self.dict['rating']=attr['rating']
            self.dict['year']=attr['year']
            self.dict['runtime']=attr['runtime']
        
            #GENRE SCORE CALCULATOR
            self.genre_score_calc(attr['genres'])
    
            #SCRAPE YIFY REVIEWS 
            self.lame_scraping(attr['slug'] , attr['title'])
            #print(self.dict)
            #IRONY OF THE DAY
            # 12-13 HRS OF CODING GROOVE n THIS IS THE ONLY USEFUL THING I've LEARNT
            #POINTER BEHAVIOUR OF DICTIONARIES
            df_list.append(self.dict.copy())
        #--------------------->debug<---------------------------------
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
        #--------------------------------------------------------------    
    def looper(self , pages, limit):
        for ind in range(1,pages):
            self.heart(ind,limit)
        return self.num
    def __init__(self):
        self.num=1
        self.url="https://yts.ag/api/v2/list_movies.json?"
        self.mov_url="https://yts.ag/movie/"
        self.dict={'review' : "something" , 
                   'rating' : 9.2 , 
                   'year' : 2017 , 
                   'runtime': 122 , 
                   'genre_score' : 1.22}    
    
    
if __name__=='__main__':
    start=time.time()
    myweb=scraper()
    limit=50
    pages=40
    num=myweb.looper(pages,limit)
    end=time.time()
    time_elapsed=end-start
    print('{0} results fetched in {1}s'.format(num,time_elapsed))
    #for i in df_list:
        #print(i)
    #print(df_list)
    df=pd.DataFrame(columns=('review','rating','year','runtime','genre_score'))
    df = pd.DataFrame(df_list)
    df.to_csv("my1.csv", sep=',')
#data = json.load(req.urlopen(url))
#print(data)