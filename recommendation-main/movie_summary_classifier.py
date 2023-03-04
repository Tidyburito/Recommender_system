from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import pandas as pd
import json
import pickle

movie_data=pd.read_csv('movie.csv')

print(movie_data)
print(movie_data['genres'].unique())

label_encoder=preprocessing.LabelEncoder()
label_encoder.fit(movie_data['genres'])
movie_data['label']=label_encoder.transform(movie_data['genres'])


print(movie_data['label'].unique())
print(movie_data)

vectorizer=TfidfVectorizer(stop_words='english',max_features=1000)

x=movie_data['summary']
y=movie_data['label']

vectorized_x=vectorizer.fit_transform(x)

rf_clf=RandomForestClassifier()

rf_clf.fit(vectorized_x,y)

pickle.dump(rf_clf,open('movie_text_classifier.pkl','wb'))
pickle.dump(vectorizer,open('movie_text_vectorizer.pkl','wb'))
pickle.dump(label_encoder,open('movie_text_encoder.pkl','wb'))