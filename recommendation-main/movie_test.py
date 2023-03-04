import pandas as pd
import pickle , csv


model=pickle.load(open('movie_text_classifier.pkl','rb'))
tfidf_vectorizer=pickle.load(open('movie_text_vectorizer.pkl','rb'))
label_encounter=pickle.load(open('movie_text_encoder.pkl','rb'))
sumi='dance in garden'
header=['id','summary']
data=['1',sumi]

with open('movie1.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerow(data)
def process(inPath,outPath):

    #sumi='I am dancing in the rain' #print(inPath)
    
            
    # To read input file
    input_df=pd.read_csv(inPath,encoding='ANSI')
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
    output_df.to_csv(outPath,index=False)
    with open(outPath, "r", encoding="utf8", newline='') as f:
        reader = csv.DictReader(f)
        a = list(reader)
    for i in a:
        print(i['genres'])
        break
process('movie1.csv','movie_output.csv')

