from unittest import result
import streamlit as st

from rateScrapper import getRate
from rateSystem import rateSystemOutput
from DataBuilder import DataBuilder

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TextClassificationPipeline

st.markdown("# Movie/show rate 🎥")
st.sidebar.markdown("# Movie/show rate 🎥")

value = st.text_input('Enter a show name', value='Titanic')
option = st.selectbox('Which model would u like to use ?',('Distilbert uncased', 'Bert cased'))
option = option.lower()
name, para = option.split(' ')

db = DataBuilder(value)


st.markdown('## The rate given by IMDB :')
st.write(f'the rate of {value} is {getRate(value)}')

st.markdown('## The rate given by our model using reaction from Twitter :')

model = AutoModelForSequenceClassification.from_pretrained("model/"+name+"/", num_labels=2,ignore_mismatched_sizes=True)
tokenizer = AutoTokenizer.from_pretrained(name+"-base-"+para)

pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=1)

results = pipe(db.get_tweets_to_analyze())
st.write(f'the rate of {value} is {rateSystemOutput(results)}')