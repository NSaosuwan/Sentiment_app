from django.shortcuts import render

# Create your views here.
def predict(request):
    #รับค่า
    detail=request.GET["Detail"]
    department=request.GET["Department"]
    aspect=request.GET["Aspect"]
    
    #ML
    clean_text = [clean_msg(txt) for txt in detail]
    tokens_list = [split_word(txt) for txt in clean_text]

    tfidf_vectorizer = TfidfVectorizer(analyzer = 'word', #this is default
                                   tokenizer=identity_fun, #does no extra tokenizing
                                   preprocessor=identity_fun, #no extra preprocessor
                                   token_pattern=None)

    tfidf_vector= tfidf_vectorizer.fit_transform(tokens_list)
    tfidf_array = np.array(tfidf_vector.todense())

    #แปลงเป็น DataFrame เพื่อง่ายแก่การอ่าน
    df = pd.DataFrame(tfidf_array,columns=tfidf_vectorizer.get_feature_names())
    SVM = pickle.load(open("/Notebook/svm.sav"))
    
    y_pred = SVM.predict(df)

    Class=y_pred,


    return render(request,"result.html")
