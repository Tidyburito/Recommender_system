import pandas as pd
import pymongo,json,csv,pickle
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
s=0
def Sort(li):
    li.sort(key=lambda t:t[1])
    li=li[::-1]
    return li
books_list=[]
books_rating=[]
books_genre=[]
book=[]
for i in bookinfo.find():
    
    books_list.append(i['b_name'])
for i in bookrating.find():
    books_rating.append(i['b_rating'])
for i in bookgenre.find():
    books_genre.append([i['b_genre_p'],i['b_genre_s']])
for i in range(0,len(books_list)):
    book.append([books_list[i],books_rating[i],books_genre[i]])
    
print(Sort(book)[:5])
