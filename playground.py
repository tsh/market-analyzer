url_wsb = 'https://www.reddit.com/r/wallstreetbets/'
from pprint import pprint

from transformers import AutoModelForSequenceClassification


# Use a pipeline as a high-level helper
# from transformers import pipeline
# 
# pipe = pipeline("text-classification", model="ProsusAI/finbert")  # bad
# print(pipe(["""
# This is a fairly simple thesis of revenue growth and margin expansion. Most of the hard work of rolling out a new product together with difficult market conditions are behind now. The company just needs to keep doing what they’re doing in order to deliver satisfactory results. Based on moderate growth assumptions BKTI is a $33 stock by the end of 2025.
# Catalyst
# Further revenue growth and margin expansion
# """]))

from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import transformers


# finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
# tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
#
# nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)
# results = nlp(['This is a fairly simple thesis of revenue growth and margin expansion. Most of the hard work of rolling out a new product together with difficult market conditions are behind now. The company just needs to keep doing what they’re doing in order to deliver satisfactory results. Based on moderate growth assumptions BKTI is a $33 stock by the end of 2025.'])
#
# print(results)


q_stock_name = [
    {"role": "user", "content": "answer in valid json like this {'ticker': 'stock name'}, what is the stock ticker: BKTI is a microcap and is best suited for small funds and PAs"},
]

q_stock_price = [
    {"role": "user", "content": "answer in valid json like this {'price': 42} what is the stock price: This is a fairly simple thesis of revenue growth and margin expansion. Most of the hard work of rolling out a new product together with difficult market conditions are behind now. The company just needs to keep doing what they’re doing in order to deliver satisfactory results. Based on moderate growth assumptions BKTI is a $33 stock by the end of 2025." }
]
# from transformers import pipeline
# pipe = pipeline("text-generation", model="FINGU-AI/FinguAI-Chat-v1")

# pprint(pipe(q_stock_price))  # bad
# pprint(pipe(q_stock_name))   # good


import torch
from transformers import pipeline, PretrainedConfig

pipe = pipeline(
    "text-generation",
    model="nidum/Nidum-Llama-3.2-3B-Uncensored",  # VERY GOOD, very slow. There are lighter models
    model_kwargs={"torch_dtype": torch.bfloat16},
    config=PretrainedConfig(name_or_path='model-Q2_K')
)


outputs = pipe(q_stock_price, max_new_tokens=256)
assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
print(assistant_response)



