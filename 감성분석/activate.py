import pickle
import tensorflow as tf
from stopword import stopwords
from functions import review_process , sentiment

from
model_lstm = tf.keras.models.load_model('model_lstm.h5')

with open('full_word.dat','rb') as fp:
    full_word = pickle.load(fp)
with open('naver_count.dat', 'rb') as fp:
    naver_count = pickle.load(fp)
with open('sentiment_pipe.dat', 'rb') as fp:
    pipe = pickle.load(fp)
with open('sentiment_word2vec.dat', 'rb') as fp:
    model = pickle.load(fp)


from konlpy.tag import Okt
import numpy as np
okt =Okt()
mapped_review, review_p = review_process(review)
r = model_lstm.predict(mapped_review)

pos=0
neg=0
for _ in range(len(review_p)):
    try:
        w2v_proba = sentiment(review_p[_])
        if w2v_proba >= 0.6 and r[_][0] ==0:
            neg+=1
        else:
             pos+=1
    except:
        pass

print(f'긍정적 리뷰 비율 : {pos/(pos+neg)*100}, 부정적 리뷰 비율: {neg/(pos+neg)*100}')