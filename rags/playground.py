# TESTED
# ProsusAI/finbert              TEXT-CLASSIFICATION     BAD
# yiyanghkust/finbert-tone      TEXT-CLASSIFICATION     GOOD
# FINGU-AI/FinguAI-Chat-v1      TEXT-GENERATION         AVG (ok with ticker name, bad with ticker price)


from pprint import pprint

statement = 'This is a fairly simple thesis of revenue growth and margin expansion. Most of the hard work of rolling out a new product together with difficult market conditions are behind now. The company just needs to keep doing what they’re doing in order to deliver satisfactory results. Based on moderate growth assumptions BKTI is a $33 stock by the end of 2025.'
q_stock_name = [
    {"role": "user", "content": f"answer in valid json like this {'ticker': 'stock name'}, {statement}"},
]
q_stock_price = [
    {"role": "user", "content": f"answer in valid json like this {'price': 42} what is the stock price: {statement}"}
]


# # positive/negative classifier
# from transformers import BertTokenizer, BertForSequenceClassification, pipeline
# import transformers
# 
# finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
# tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
# 
# nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)
# results = nlp(['This is a fairly simple thesis of revenue growth and margin expansion. Most of the hard work of rolling out a new product together with difficult market conditions are behind now. The company just needs to keep doing what they’re doing in order to deliver satisfactory results. Based on moderate growth assumptions BKTI is a $33 stock by the end of 2025.'])
# 
# print(results)



# =================================

# import torch
# from transformers import pipeline, PretrainedConfig
#
# pipe = pipeline(
#     "text-generation",
#     model="nidum/Nidum-Llama-3.2-3B-Uncensored",  # VERY GOOD, very slow. There are lighter models
#     model_kwargs={"torch_dtype": torch.bfloat16},
#     config=PretrainedConfig(name_or_path='model-Q2_K')
# )
#
#
# outputs = pipe(q_stock_price, max_new_tokens=256)
# assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
# print(assistant_response)

# ============================

# from transformers import AutoModelForCausalLM, AutoTokenizer
#
# model = AutoModelForCausalLM.from_pretrained("instruction-pretrain/finance-Llama3-8B")
# tokenizer = AutoTokenizer.from_pretrained("instruction-pretrain/finance-Llama3-8B")
#
# # Put your input here, NO prompt template is required
# user_input = '''Use this fact to answer the question: Title of each class Trading Symbol(s) Name of each exchange on which registered
# Common Stock, Par Value $.01 Per Share MMM New York Stock Exchange
# MMM Chicago Stock Exchange, Inc.
# 1.500% Notes due 2026 MMM26 New York Stock Exchange
# 1.750% Notes due 2030 MMM30 New York Stock Exchange
# 1.500% Notes due 2031 MMM31 New York Stock Exchange
#
# Which debt securities are registered to trade on a national securities exchange under 3M's name as of Q2 of 2023?'''
#
# inputs = tokenizer(user_input, return_tensors="pt", add_special_tokens=True).input_ids.to(model.device)
# outputs = model.generate(input_ids=inputs, max_new_tokens=400)[0]
#
# answer_start = int(inputs.shape[-1])
# pred = tokenizer.decode(outputs[answer_start:], skip_special_tokens=True)  #??? TODO: test
#
# print(pred)



