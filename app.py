#importing necessary libraries
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
import streamlit as st
from PIL import Image

#importing cover image
image = Image.open('NLP.png')

#loading the pre-trained weights and model architecture
model = tf.keras.models.load_model('textPredictorModel.h5')

#defining project title
st.title("Text Predictor!")
st.subheader("A Deep Learning Model that foretells text before you type it.")
st.image(image, caption='',use_column_width=True)

#dataset preprocessing
file = open("Goodwill.txt").read() #opeining the dataset and reading from it

tokenizer = Tokenizer() #tokenizing the dataset
data = file.lower().split("\n") #converting dataset to lowercase

#removing whitespaces from the dataset
corpus = []
for line in data:
    a = line.strip()
    corpus.append(a)

#generating tokens for each sentence in the data
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1
print(tokenizer.word_index)
print(total_words)

#creating labels for each sentence in dataset
input_sequences = []
for line in corpus:
	token_list = tokenizer.texts_to_sequences([line])[0]
	for i in range(1, len(token_list)):
		n_gram_sequence = token_list[:i+1]
		input_sequences.append(n_gram_sequence)

# pad sequences 
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# create predictors and label
xs, labels = input_sequences[:,:-1],input_sequences[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

num = st.slider("Number of text predictions?",0,10)

#generating next words given a seed
def next_word(seed):
  seed_text = seed
  next_words = num
  for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted = model.predict_classes(token_list, verbose=0)
    output_word = ""
    for word, index in tokenizer.word_index.items():
      if index == predicted:
        output_word = word
        break
    seed_text += " " + output_word
  st.subheader(seed_text)

#getting the output/predicted text  
next_word(st.text_input('Enter seed sentence','I want to meet'))