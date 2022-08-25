from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from .forms import FormComment
from io import BytesIO
import base64
from .models import Comment
#{% load static %}

#HTTP response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# ML
import pandas as pd
from collections import Counter
import numpy as np
import pickle
import pythainlp
from pythainlp import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.corpus import wordnet
from nltk.stem.porter import PorterStemmer
from nltk.corpus import words
from stop_words import get_stop_words
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

from pythainlp.corpus import thai_stopwords
stop_words= thai_stopwords()

import nltk
nltk.download("stopwords")
th_stop = thai_stopwords()
en_stop = tuple(get_stop_words('en'))

# Create your views here.
#ดึงข้อมูลจากweb
@csrf_exempt



def hello(request):
    
    #ดึงข้อมูลจากmysql
    data= Post.objects.all()

    return render(request,'home.html',
    {'Posts':data,})

def all(request):
    
    #ดึงข้อมูลจากmysql
    data= Post.objects.all()

    return render(request,'index.html',
    {'Posts':data,})

def department(request):
    
    #ดึงข้อมูลจากmysql
    data= Post.objects.all()

    return render(request,'department.html',
    {'Posts':data,})

#รับความคิดเห็น
#def createForm(request):
#    return render(request,'form.html')


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        raw_data = request.body
        data = json.loads(raw_data)
        detail =data["Detail"]
        department =data["Department"]
        date = data["Date"]
        print("Data received from Webhook is: ", detail)
 #   return  HttpResponse("Webhook received!")

#def addBlog(request):
    #รับค่า
 #   detail=request.POST.get("Detail")
 #   department=request.POST.get("Department")
  #  date = request.POST.get("Date")
    
    s3_file = s3fs.S3FileSystem(key='AKIAZCYHPGBE6FJD7H5Q',
                           secret='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',
                                     
               client_kwargs=dict(endpoint_url="https://s3.amazonaws.com"),anon=True)
    
    with s3_file.open('django-sentiment/static/blogs/media/tfidf_vectorizer.sav', 'rb') as tf:
         tfidf_vectorizer = pickle.load(tf)


    with s3_file.open('django-sentiment/static/blogs/media/svm.sav', 'rb') as svm:
         SVM = pickle.load(svm)

   
    with s3_file.open('django-sentiment/static/blogs/media/SGD.sav', 'rb') as sgd:
         SGD= pickle.load(sgd)

    #ML
    clean_text = [clean_msg(detail)]
    tokens_list = [split_word(txt) for txt in clean_text]

    tfidf_vector= tfidf_vectorizer.transform(tokens_list)
    tfidf_array = np.array(tfidf_vector.todense())

    #แปลงเป็น DataFrame เพื่อง่ายแก่การอ่าน
    df = pd.DataFrame(tfidf_array,columns=tfidf_vectorizer.get_feature_names_out())
    
    y_pred = SVM.predict(df)

    Class=y_pred[0]
    
    Y_pred = SGD.predict(df)

    aspect = Y_pred[0] 

    comment=Comment(
        Class=Class,
        Detail=detail,
        Department=department,
        Aspect=aspect,
        words=tokens_list,
        date=date,
        )
    comment.save()

    return  HttpResponse("Webhook received!")

def clean_msg(msg):
    
    
    # ลบ text ที่อยู่ในวงเล็บ <> ทั้งหมด
    msg = re.sub(r'<.*?>','', msg)
    
    # ลบ hashtag
    msg = re.sub(r'#','',msg)
    
    # ลบ เครื่องหมายคำพูด (punctuation)
    for c in string.punctuation:
        msg = re.sub(r'\{}'.format(c),'',msg)
    
    # ลบ separator เช่น \n \t
    msg = ' '.join(msg.split())
    
    return msg

def split_word(text):
    
    from pythainlp import word_tokenize   
     
    tokens = word_tokenize(text,engine='newmm')
    
    # Remove stop words ภาษาไทย และภาษาอังกฤษ
    tokens = [i for i in tokens if not i in th_stop and not i in en_stop]
    
    # ลบตัวเลข
    tokens = [i for i in tokens if not i.isnumeric()]
    
    # ลบช่องว่าง
    tokens = [i for i in tokens if not ' ' in i]

    return tokens

def identity_fun(text):
    return text
