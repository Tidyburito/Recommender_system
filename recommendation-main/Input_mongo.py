import csv, pymongo
import ast
#####
#First create the database and collections in mongodb
#Database: booksdatabase
#Collections : book_info,book_genre,book_rating
#Database: moviesdatabase
#Collections : movie_info,movie_genre
#Database: usersdatabase 
#Collections : user_info,user_genre,  user_history

# Then run this file

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb=client["booksdatabase"]
mydb1=client["moviesdatabase"]
book_info=mydb["book_info"]
book_genre=mydb["book_genre"]
book_rating=mydb["book_rating"]
movie_info=mydb1["movie_info"]
movie_genre=mydb1["movie_genre"]


with open("movie.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    movie_reader = list(reader)
with open("FinalBooksDB.csv", "r", encoding="utf8") as g:
    reader1 = csv.DictReader(g)
    book_reader = list(reader1)


for i in book_reader:
    if(',' in i["Author"]):
        temp=i["Author"].split(',')
        author=temp[0]
    else:
        author=i["Author"]
    info={"b_id":i["Book_ID"],"b_name":i["Book_name"],"b_author":author}
    genre={"b_id":i["Book_ID"],"b_genre_p":i["Book_genre_p"],"b_genre_s":i["Book_genre_s"]}
    rating={"b_id":i["Book_ID"],"b_rating" :float(i["Rating"])}
    y = book_info.insert_one(info)
    y = book_genre.insert_one(genre)
    y = book_rating.insert_one(rating)
m_id=0
for i in movie_reader:
    g_list=[]
    temp=i["genres"].split(',')
    for j in temp:
        g_list.append(j)
    m_info={"m_id": m_id,"m_name":i["movie_name"],"m_summary":i["summary"]}
    m_genre={"m_id":   m_id,"m_genre":g_list}
    y = movie_info.insert_one(m_info)
    y = movie_genre.insert_one(m_genre)
    m_id+=1
    

 
"""
###### Enter this data manually in mongo db
user_info={
  "u_id": 0,
  "username": "kaleen",
  "password": "admin",
}
user_genre={
    
    "u_id": 0,
    "liked_genre": [
    "romance",
    "classic",
    "fantasy"
  ],
    "dislike_genre": [
    "comedy",
    "religion"
  ]
}

user_history={
    "u_id": 0,
    "history": [
    "Harry Potter and the Prisoner of Azkaban",
    "The Old Man and the Sea",
    "The Notebook",
    "Winnie-the-Pooh",
    "The Complete Stories and Poems",
    "Interview with the Vampire"
  ]
}

"""




