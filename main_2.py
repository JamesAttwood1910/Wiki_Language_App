import streamlit as st

import nltk
import bs4 as bs
import urllib.request
import re
import heapq
import requests
from bs4 import BeautifulSoup
import inspect


st.title("Wiki English Activities")

container1 = st.container()

container1.markdown('## Welcome language learners')

container1.markdown('''
	Created by passionate language learners and professors this application allows you 
	to choose a wikepedia article of your choice and immeditatly you will be provided 
	with a set of activites designed for you to practice your English. Take control of 
	your improvement with topics you are passionate about and activities designed to your 
	needs.

	Happy studying!!! 
	''')

wiki_site = st.text_input("Choose your wikipedia article: ", value = 'https://en.wikipedia.org/wiki/Nailsea')

url = wiki_site
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

titles = []
for x in doc.find_all('span', class_ = 'mw-headline'):
  if x.string == 'External links':
    continue
  if x.string == 'References':
    continue
  if x.string == 'See also':
  	continue
  if x.string == 'Further reading':
  	continue
  titles.append(x.string)

for title in titles:
  st.header(title)
  
  paragraphs = title.find_all_next('p')
  article_text = ""
  for p in paragraphs: 
    article_text += str(p.get_text())
  article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
  article_text = re.sub(r'\s+', ' ', article_text)

  formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
  formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

  sentence_list = nltk.sent_tokenize(article_text)
  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {}

  for word in nltk.word_tokenize(formatted_article_text):
  	if word not in stopwords:
  		if word not in word_frequencies.keys():
  			word_frequencies[word] = 1
  		else: 
  			word_frequencies[word] +=1


  word_frequencies_weighted = word_frequencies

  maximum_frequency = max(word_frequencies.values())

  for word in word_frequencies_weighted.keys():
  	word_frequencies_weighted[word] = (word_frequencies_weighted[word]/maximum_frequency)


  sentence_scores = {}

  for sent in sentence_list:
  	for word in nltk.word_tokenize(sent.lower()):
  		if word in word_frequencies.keys():
  			if len(sent.split(' ')) < 30:
  				if sent not in sentence_scores.keys():
  					sentence_scores[sent] = word_frequencies[word]
  				else:
  					sentence_scores[sent] += word_frequencies[word]

  summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

  summary = ' '.join(summary_sentences)

  st.write(summary)

Key_words = heapq.nlargest(10, word_frequencies_weighted, key=word_frequencies_weighted.get)

words = ' '.join(Key_words)

st.write(words)










