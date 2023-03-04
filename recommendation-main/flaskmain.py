from collections import UserDict
import pandas as pd
from flask import Flask, render_template,request,redirect
import pymongo,json,csv,pickle
app = Flask(__name__, template_folder='templatefiles', static_folder='staticfiles')
processed_text=''
us=''
valueee='yo'
uid=0
user_dict={}
working_count=0
@app.route('/')
def index():
    return render_template('index.html',value='yo')

@app.route('/menu', methods=['GET','POST'])
def my_home():
    global us
    global uid
    global user_dict
    global working_count
    if(request.method == "POST" and working_count==0):
            
        # getting input with name = fname in HTML form
        us = request.form.get("us")
        # getting input with name = lname in HTML form
        pd = request.form.get("pd")
    if  len(us)>1:
        
        working_count+=1
        #client = pymongo.MongoClient("mongodb+srv://admin:putin@cluster0.iy4of14.mongodb.net/?retryWrites=true&w=majority")
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=client["booksdatabase"]
        mydb1=client["moviesdatabase"]
        mydb2=client["usersdatabse"]
        bookinfo=mydb["book_info"]
        bookgenre=mydb["book_genre"]
        bookrating=mydb["book_info"]
        moviegenre=mydb1["movie_genre"]
        movieinfo=mydb1["movie_info"]
        userinfo=mydb2["user_info"]
        usergenre=mydb2["user_genre"]
        userhistory=mydb2["user_history"]
        l={}
        print()
        new_user=False
        for i in userinfo.find():
            print(us)
            new_uid=i["u_id"]
            if(us==i['username']):
                
                print("AAya hain d d")
                new_user=False
                break
            else:
                new_user=True
            new_uid=new_uid+1
        if(new_user==True):
            u_info={
                    "u_id": new_uid,
                    "username": us,
                    "password": pd,
                    }
            u_genre={ "u_id": new_uid,
            "liked_genre": ["nothing"], "dislike_genre": ["nothing"]}
            u_history={
                "u_id": new_uid,
                "history": [
                "nothing"]}
            y = userinfo.insert_one(u_info)
            y = usergenre.insert_one(u_genre)
            y = userhistory.insert_one(u_history)
        for i in userinfo.find():
            print(us)
            new_uid=i["u_id"]
            if(us==i['username']):
                uid=i['u_id']
                print(us)
                # hist=userhistory.find({},{"u_id":i["u_id"]})
                # gen=usergenre.find({},{"u_id":i["u_id"]})
                for k in usergenre.find():
                    if(k['u_id']==i['u_id']):
                        ly=str([k['liked_genre']])
                        dy=str([k['dislike_genre']])
                user_history=[]
               
                for j in userhistory.find():
                    if(j['u_id']==i['u_id']):
                        hy=str([j['history']])
                lg=[]
                ug=[]
                # for j in gen:
                    # lg=j['liked_genre']
                    # ug=j['dislike_genre']
                    # lg.append(j)
                #print(lg[new_uid]['liked_genre'])
                #mycol.find({},{ "address": 0 })
                #hy=str(user_history[0]['history'])
                print(lg)
                # ly=str(lg[0]['liked_genre'])
                # hy=str(user_history[0]['history'])
                # dy=str(lg[0]['dislike_genre'])
                l={"username":i['username'],"u_id":i["u_id"],"history":hy[1:-1],"lg": ly[1:-1],"ug": dy[1:-1]}
                print(l)  
                user_dict=l
                break
                    #print(l)
        
        return render_template('main.html',user_dict=user_dict)
    return render_template("index.html")


# @app.route('/addhistory', methods=['GET','POST'])
# def add_history_temp():
#     return render_template()
    
# @app.route('/addhistory', methods=['GET','POST'])
# def add_history():
#     if request.method == "POST":
#         client = pymongo.MongoClient("mongodb://localhost:27017/")
#         mydb2=client["usersdatabase"]
#         userhistory=mydb2["user_history"]
    
@app.route('/addlikedgenretemp',  methods=['GET','POST'])    
def add_liked_genre_temp():
    global user_dict
    return render_template('ALG.html',user_dict=user_dict)
@app.route('/addlikedgenre', methods=['GET','POST'])
def add_liked_genre():
    global user_dict
    if request.method == "POST":
        alg = request.form.get("alg")
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=client["booksdatabase"]
        mydb1=client["moviesdatabase"]
        mydb2=client["usersdatabse"]
        bookinfo=mydb["book_info"]
        bookgenre=mydb["book_genre"]
        bookrating=mydb["book_info"]
        moviegenre=mydb1["movie_genre"]
        movieinfo=mydb1["movie_info"]
        userinfo=mydb2["user_info"]
        usergenre=mydb2["user_genre"]
        userhistory=mydb2["user_history"]
        mydb2=client["usersdatabase"]
        for i in userinfo.find():
            temp_uid=0
            if(us==i['username']):
                temp_uid=i['u_id']
                break
        for i in usergenre.find():
            if(i['u_id']==temp_uid):
                if(i['liked_genre'][0]=='nothing'):
                    myquery = { "u_id": temp_uid }
                    newvalues = { "$set": { "liked_genre": [alg] } }
                    usergenre.update_one(myquery, newvalues)
                else:
                    if(alg not in i['liked_genre']):
                        myquery = { "u_id": temp_uid }
                        alg_list=[]
                        alg_list=i['liked_genre']
                        alg_list.append(alg)
                        newvalues = { "$set": { "liked_genre": alg_list }}
                        usergenre.update_one(myquery, newvalues)
        #return render_template('index.html')  
        return redirect("http://127.0.0.1:5000/menu", code=302)  
            
@app.route('/adddislikegenretemp',  methods=['GET','POST'])    
def add_disliked_genre_temp():
    global user_dict
    return render_template('ADG.html',user_dict=user_dict)

@app.route('/adddislikegenre', methods=['GET','POST'])
def add_disliked_genre():
    if request.method == "POST":
        adg = request.form.get("adg")
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=client["booksdatabase"]
        mydb1=client["moviesdatabase"]
        mydb2=client["usersdatabse"]
        bookinfo=mydb["book_info"]
        bookgenre=mydb["book_genre"]
        bookrating=mydb["book_info"]
        moviegenre=mydb1["movie_genre"]
        movieinfo=mydb1["movie_info"]
        userinfo=mydb2["user_info"]
        usergenre=mydb2["user_genre"]
        userhistory=mydb2["user_history"]
        mydb2=client["usersdatabase"]
        for i in userinfo.find():
            temp_uid=0
            if(us==i['username']):
                temp_uid=i['u_id']
                break
        for i in usergenre.find():
            if(i['u_id']==temp_uid):
                if(i['dislike_genre'][0]=='nothing'):
                    myquery = { "u_id": temp_uid }
                    newvalues = { "$set": { "dislike_genre": [adg] } }
                    usergenre.update_one(myquery, newvalues)
                else:
                    myquery = { "u_id": temp_uid }
                    adg_list=[]
                    adg_list=i['dislike_genre']
                    adg_list.append(adg)
                    newvalues = { "$set": { "dislike_genre": adg_list}}
                    userhistory.update_one(myquery, newvalues)
                    
        return redirect("http://127.0.0.1:5000/menu", code=302)    
@app.route('/addbooktemp', methods=['GET','POST'])    
def add_book_temp():
    global user_dict
    return render_template('AB.html',user_dict=user_dict)

@app.route('/addbook', methods=['GET','POST'])
def add_book(): 
    if request.method == "POST":
        global us
        adb = request.form.get("adb")
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=client["booksdatabase"]
        mydb1=client["moviesdatabase"]
        mydb2=client["usersdatabse"]
        bookinfo=mydb["book_info"]
        bookgenre=mydb["book_genre"]
        bookrating=mydb["book_rating"]
        moviegenre=mydb1["movie_genre"]
        movieinfo=mydb1["movie_info"]
        userinfo=mydb2["user_info"]
        usergenre=mydb2["user_genre"]
        userhistory=mydb2["user_history"]
        for i in userinfo.find():
            temp_uid=0
            if(us==i['username']):
                temp_uid=i['u_id']
                break
        book_read_list=[]
        for i in bookinfo.find():
            if(adb==i['b_name']):
                new_book=adb
                for j in userhistory.find():
                    book_read_list=j['history']
                book_read_list.append(new_book)
                myquery = { "u_id": temp_uid }
                adb_list=book_read_list
                newvalues = { "$set": { "history": adb_list }}
                userhistory.update_one(myquery, newvalues)
            
        return redirect("http://127.0.0.1:5000/menu", code=302)
            
@app.route('/searchgenre', methods=['GET','POST'])      
def search_genre():
    if request.method == "POST":
        global user_dict
        global us
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        sg = request.form.get("search")
        print(sg)
        mydb=client["booksdatabase"]
        mydb1=client["moviesdatabase"]
        mydb2=client["usersdatabse"]
        bookinfo=mydb["book_info"]
        bookgenre=mydb["book_genre"]
        bookrating=mydb["book_rating"]
        moviegenre=mydb1["movie_genre"]
        movieinfo=mydb1["movie_info"]
        userinfo=mydb2["user_info"]
        usergenre=mydb2["user_genre"]
        userhistory=mydb2["user_history"]
        search_genre_list=[]
        genre_bid=[]
        for i in bookgenre.find():
            #print(i['b_genre_p'])
            if(sg==i['b_genre_p'] or sg==i['b_genre_s']):
                genre_bid.append([i['b_id'],i['b_genre_p'],i['b_genre_s']])
        print(genre_bid)
        for i in bookinfo.find():
            for j in genre_bid:
                if(i['b_id']==j[0]):
                    search_genre_list.append([i['b_name'],0,[j[1],j[2]]])
        print(search_genre_list[:10])
        
        return render_template('index2.html',wanted=search_genre_list[:10],user_dict=user_dict)
                    
@app.route('/searchbook', methods=['GET','POST'])      
def search_book():
    if request.method == "POST":
        global user_dict
        global us
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        sb = request.form.get("search")
        print(sb)
        mydb=client["booksdatabase"]
        mydb2=client["usersdatabse"]
        bookinfo=mydb["book_info"]
        bookgenre=mydb["book_genre"]
        bookrating=mydb["book_rating"]
        userinfo=mydb2["user_info"]
        usergenre=mydb2["user_genre"]
        userhistory=mydb2["user_history"]
        search_book_list=[]
        for i in bookinfo.find():
            if(sb in i['b_name']):
                search_book_list.append([i['b_name'],0,i['b_id']])
        
        return render_template('index2.html',wanted=search_book_list[:10],user_dict=user_dict)

                    
@app.route('/searchmovie', methods=['GET','POST'])      
def search_movie():
    if request.method == "POST":
        global user_dict
        global us
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        sm = request.form.get("search")
        print(sm)
        mydb=client["booksdatabase"]
        mydb2=client["usersdatabse"]
        mydb1=client["moviesdatabase"]
       
        moviegenre=mydb1["movie_genre"]
        movieinfo=mydb1["movie_info"]
        search_movie_list=[]
        for i in movieinfo.find():
            if(sm in i['m_name']):
                search_movie_list.append([i['m_name'],0,i['m_id']])
        
        return render_template('index4.html',wanted=search_movie_list[:10],user_dict=user_dict)

            
@app.route('/searchmoviegenre', methods=['GET','POST'])      
def search_moviegenre():
    if request.method == "POST":
        global user_dict
        global us
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        sgm = request.form.get("search")
        print(sgm)
        mydb=client["booksdatabase"]
        mydb1=client["moviesdatabase"]
        mydb2=client["usersdatabse"]
        bookinfo=mydb["book_info"]
        bookgenre=mydb["book_genre"]
        bookrating=mydb["book_rating"]
        moviegenre=mydb1["movie_genre"]
        movieinfo=mydb1["movie_info"]
        userinfo=mydb2["user_info"]
        usergenre=mydb2["user_genre"]
        userhistory=mydb2["user_history"]
        search_genre_list=[]
        genre_bid=[]
        for i in moviegenre.find():
            #print(i['b_genre_p'])
            for j in i['m_genre']:
                if(j.lower()==sgm.lower()):
                    genre_bid.append([i['m_id'],i['m_genre']])
        print(genre_bid)
        movie_names=[]
        for i in movieinfo.find():
            for j in genre_bid:
                if(i['m_id']==j[0] and (i["m_name"] not in movie_names)):
                    movie_names.append(i['m_name'])
                    search_genre_list.append([i['m_name'],0,j[1]])
        print(search_genre_list[:10])

        return render_template('index4.html',wanted=search_genre_list[:10],user_dict=user_dict)
 

@app.route('/rec', methods=['GET','POST'])
def rec_book():
    global us
    global uid
    
    global user_dict
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=client["booksdatabase"]
    mydb1=client["moviesdatabase"]
    mydb2=client["usersdatabse"]
    bookinfo=mydb["book_info"]
    bookgenre=mydb["book_genre"]
    bookrating=mydb["book_rating"]
    moviegenre=mydb1["movie_genre"]
    movieinfo=mydb1["movie_info"]
    userinfo=mydb2["user_info"]
    usergenre=mydb2["user_genre"]
    userhistory=mydb2["user_history"]
    books_read=[]
    lg=[]
    ug=[]
    fav_authors=[]
    the_mighty_counter=0
    wanted = []
    #us='chetu11'
    bookavail=[]
    user_history=[]
    print
    print("This is ",us)
    for i in userinfo.find():
        print(us)
        new_uid=i["u_id"]
        if(us==i['username']):
            print(us)
            hist=userhistory.find({},{"u_id":i["u_id"]})
            gen=usergenre.find({},{"u_id":i["u_id"]})
            
            for j in hist:
                user_history.append(j)
            print(user_history[0]['history'])
            books_read=user_history[0]['history']
            lg=[]
            ug=[]
            for j in gen:
                # lg=j['liked_genre']
                # ug=j['dislike_genre']
                lg.append(j)
                ug.append(j)
            break
            #print(lg[new_uid]['liked_genre'])
            #mycol.find({},{ "address": 0 })
            # hy=str(user_history[0]['history'])
            # ly=str(lg[new_uid]['liked_genre'])
            # dy=str(lg[new_uid]['dislike_genre'])
    #print(user_history[0]['history'])
    
    b_author_list=[]
    b_pg_list=[]
    b_sg_list=[]
    b_rating_list=[]
    b_name_list=[]
    lg=lg[new_uid]['liked_genre']
    ug=ug[new_uid]['dislike_genre']
    for i in bookinfo.find():
        b_author_list.append(i['b_author'])
        b_name_list.append(i['b_name'])
        if(i['b_name'] in books_read):
            fav_authors.append(i['b_author'])
            # if(',' in i['Author']):
            #     yo=i['Author'].split(',')
            #     #print(yo)
            #     for j in yo:
            #         fav_authors.append(j)
            # else:
            #     fav_authors.append(i['Author'])

    
    #print(username,books_read,lg,ug,fav_authors)
    def Sort(li):
        li.sort(key=lambda t:t[1])
        li=li[::-1]
        return li
    #print("Favourite Authors of user : ",fav_authors)
    for i in bookgenre.find():
        b_pg_list.append(i['b_genre_p'])
        b_sg_list.append(i['b_genre_s'])
    for i in bookrating.find():
        b_rating_list.append(i['b_rating'])
    for i in range(0,len(b_pg_list)):
        
        bookavail.append({'Book_name':b_name_list[i],'Book_genre_p':b_pg_list[i],"Author":b_author_list[i],'Book_genre_s':b_sg_list[i] ,'Ratings_fivee' :b_rating_list[i]})
    for i in bookavail:
        #print(the_mighty_counter)
        the_mighty_counter=0
        remarks=[]
        #print(i['Book_genre_p'])
        # if(i['Book_genre_p'] =='NA' or  i['Book_genre_s']=='NA' or i['Book_name'].lower()=='untitled' ):
        #     continue
        if(i['Book_genre_p'].lower() in lg):
            #print(i['Book_genre_p'])
            the_mighty_counter+=4
            
            remarks.append("Similar Primary Genre")
        if(i['Book_genre_s'].lower() in lg):
            #print(i['Book_genre_s'])
            remarks.append("Similar Secondary Genre")
            the_mighty_counter+=2
        if(i['Book_genre_p'].lower() in ug):
            the_mighty_counter-=1.5
        if(i['Book_genre_s'].lower() in ug):
            the_mighty_counter-=1
        if(i['Author'] in fav_authors):
            the_mighty_counter+=3
            remarks.append("Similar Author")
        
        the_mighty_counter+=float(i['Ratings_fivee'])/2
        gt=str(the_mighty_counter)[:5]
        the_mighty_counter=float(gt)
        
        wanted.append([i['Book_name'],the_mighty_counter,i['Book_genre_p'].lower()+','+i['Book_genre_s'].lower(),remarks])
    wanted = Sort(wanted)
    print(" ||| BOOKS RECOMENDED FOR YOU ||")
    #for jij in range(0,10):
        #print(wanted[jij][0],"   Remarks :",wanted[jij][2], " Score :",wanted[jij][1])
    return render_template('index2.html',user_dict=user_dict,wanted=wanted[:10])

@app.route('/movrec', methods=['GET','POST'])      
def rec_movie():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
   
    mydb1=client["moviesdatabase"]
    mydb2=client["usersdatabse"]
    moviegenre=mydb1["movie_genre"]
    movieinfo=mydb1["movie_info"]
    userinfo=mydb2["user_info"]
    usergenre=mydb2["user_genre"]
    userhistory=mydb2["user_history"]
    mydb=client["booksdb"]
    user=mydb["userdb"]
    books_read=[]
    lg=[]
    ug=[]
    the_mighty_counter=0
    wanted = []
    
    global us
    global user_dict
    for i in userinfo.find():
        print(us)
        new_uid=i["u_id"]
        if(us==i['username']):
            gen=usergenre.find({},{"u_id":i["u_id"]})
            lg=[]
            ug=[]
            for j in gen:
                # lg=j['liked_genre']
                # ug=j['dislike_genre']
                lg.append(j)
                ug.append(j)
            break
    lg=lg[new_uid]['liked_genre']
    ug=ug[new_uid]['dislike_genre']
    print(lg,ug)
    def Sort(li):
        li.sort(key=lambda t:t[1])
        li=li[::-1]
        return li
    movie_data=[]
    # with open("movie.csv", "r", encoding="utf8") as f:
    #     reader = csv.DictReader(f)
    #     movie_data = list(reader)
    m_name_list=[]
    m_genre_list=[]
    for i in movieinfo.find():
        m_name_list.append(i['m_name'])
    for i in moviegenre.find():
        
        temp_list=[]
        for j in i['m_genre']:
            temp_list.append(j)
        m_genre_list.append(temp_list)
    for i in range(0,len(m_name_list)):
        movie_data.append({'genres':m_genre_list[i],'movie_name':m_name_list[i]})
    the_mighty_counter=0
    remarks=[]
    wanted=[]
    #print(movie_data)
    for i in movie_data:
        the_mighty_counter=0
        gen=[]
        for j in i['genres']:
            if(j in lg):
                the_mighty_counter+=1.5
                gen.append(j)
            if(j in ug):
                the_mighty_counter-=0.5
        #print(gen)
                
        wanted.append([i['movie_name'],the_mighty_counter,str(gen)[1:-1]])
    wanted = Sort(wanted)
    print(" ||| MOVIES RECOMENDED FOR YOU ||")
    #for jij in range(0,10):
        #print(wanted[jij][0],"   Remarks :",wanted[jij][2], " Score :",wanted[jij][1])
    return render_template('index3.html',user_dict=user_dict,wanted=wanted[:10])
@app.route('/suminp', methods=['GET','POST'])
def sum_inp():
    
    return render_template('index4.html')
    
sumi=''

@app.route('/sumrectemp', methods=['GET','POST'])
def sum_rectemp():
    global user_dict
    return render_template('RMT.html',user_dict=user_dict)

@app.route('/sumrec', methods=['GET','POST'])
def sum_rec():
    if request.method == "POST":
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=client["booksdb"]
        user=mydb["userdb"]
        books_read=[]
        lg=[]
        ug=[]
        the_mighty_counter=0
        wanted = []
        #us='chetu11'
        global us
        global user_dict
        
        for i in user.find():
            if(us==i['username']):
                for j in i['history']:
                    books_read.append(j)
                for j in i['liked_genre']:
                    lg.append(j)
                for j in i['dislike_genre']:
                    ug.append(j)
                user_dict=i
                break
        global sumi
        # getting input with name = fname in HTML form
        sumi = request.form.get("sumi")
        header=['id','summary']
        data=['1',sumi]
        print(sumi)
        with open('movie1.csv', 'w', encoding='UTF8', newline='' ) as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerow(data)
        model=pickle.load(open('movie_text_classifier.pkl','rb'))
        tfidf_vectorizer=pickle.load(open('movie_text_vectorizer.pkl','rb'))
        label_encounter=pickle.load(open('movie_text_encoder.pkl','rb'))
        #'movie1.csv','movie_output.csv'
        input_df=pd.read_csv('movie1.csv',encoding='ANSI')
        # To vectorize the data
        features=tfidf_vectorizer.transform(input_df['summary'])
        # predict the classes
        predictions=model.predict(features)
        # convert output labels to categories
        input_df['genres']=label_encounter.inverse_transform(predictions)
        #print(input_df['genres'].split(','))
        # save results to csv
        output_df=input_df[['id','genres']]
        #print(output_df['genres'])
        output_df.to_csv('movie_output.csv',index=False)
        with open('movie_output.csv', "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            a = list(reader)
        for i in a:
            probable_genres=i['genres'].split(',')
            break
        def Sort(li):
            li.sort(key=lambda t:t[1])
            li=li[::-1]
            return li
        with open("movie.csv", "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            movie_data = list(reader)
        the_mighty_counter=0
        remarks=[]
        wanted=[]
        for i in movie_data:
            movie_genre_list=[]
            gen=i['genres'].split(',')
            for j in gen:
                if(j in probable_genres):
                    the_mighty_counter+=1
                
                    
            wanted.append([i['movie_name'],the_mighty_counter,i['genres']])
        wanted = Sort(wanted)
        return render_template('index5.html',user_dict=user_dict,wanted=wanted[:8])
if __name__=='__main__':
    app.run(debug = True)