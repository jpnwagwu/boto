#!/usr/bin/env python
# coding: utf-8

# In[10]:


#importing libraries
import nltk
import numpy as np
import random
import string
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import warnings
#warnings.filterwarnings('ignore')


# In[11]:


#Load and read file
file = open('test.txt','r')
data = file.read()


# In[12]:


#Convert all words in corpus to lower case and convert to list of words or sentences
data = data.lower()
sentences = nltk.sent_tokenize(data)
words = nltk.word_tokenize(data)


# In[13]:


sentences[:3]


# In[14]:


words[:3]


# In[15]:


#Extracting root words with meanings
lemma = nltk.stem.WordNetLemmatizer()

def LemmaTokens(tokens):
    return [lemma.lemmatize(token) for token in tokens]

#Remove noise and stop words
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

#Lemmatize and remove stop words and noise
def LemmaNormalize(word):
    return LemmaTokens(nltk.word_tokenize(word.lower().translate(remove_punct_dict)))


# In[16]:


#Greetings 
input_greetings = ("hello", "greetings", "hi", "sup", "what's up", "hey", "Good Morning", "Good Afternoon", "Good Evening", "How are you" )
output_greetings = ["hi", "hey", "hi there", "I'm glad you are talking to me"]

#returns Greetings if word is present in list of input greetings
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in input_greetings:
            return random.choice(output_greetings)


# In[17]:


def response(user_input):
    boto_response = ''
    sentences.append(user_input)
    TfidVec = TfidfVectorizer(tokenizer=LemmaNormalize, stop_words='english')
    tfidf = TfidVec.fit_transform(sentences)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf==0):
        boto_response = boto_response+"Could you rephrase? Remember I talk only about Vector"
    else:
        boto_response = boto_response+sentences[idx]
        return boto_response
    
    


# In[ ]:


marker=True
print("BOTO: My name is Boto. I will answer your queries about Vector. If you want to exit, type Goodbye")
while (marker==True):
    user_input = input()
    user_input = user_input.lower()
    if (user_input != 'goodbye'):
        if (user_input=='thanks' or user_input =='thank you'):
            marker=False
            print("BOTO: You are welcome..")
        else:
            if greeting(user_input)!=None:
                print("BOTO: "+greeting(user_input))
            else:
                print("BOTO: ", end="")
                print(response(user_input))
                sentences.remove(user_input)
    else:
        marker=False
        print("BOTO: Bye! Have a great day ")


# In[ ]:




