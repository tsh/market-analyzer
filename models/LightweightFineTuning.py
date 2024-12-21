#!/usr/bin/env python
# coding: utf-8

# # Lightweight Fine-Tuning Project

# TODO: In this cell, describe your choices for each of the following
# 
# * PEFT technique: 
# * Model: 
# * Evaluation approach: 
# * Fine-tuning dataset: 

# ## Loading and Evaluating a Foundation Model
# 
# TODO: In the cells below, load your chosen pre-trained Hugging Face model and evaluate its performance prior to fine-tuning. This step includes loading an appropriate tokenizer and dataset.

# In[17]:


from datasets import load_dataset
ds = load_dataset("rotten_tomatoes", split="validation")
ds = ds.train_test_split(test_size=0.1)
print(ds)

from transformers import AutoTokenizer
model_name = 'distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenized_ds = tokenizer(ds['test']['text'], truncation=True)

def preprocess_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenized_ds = {}
for split in ['train', 'test']:
    tokenized_ds[split] = ds[split].map(preprocess_function, batched=True)
    
print(tokenized_ds)


# In[18]:


from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')

for param in model.base_model.parameters():
    param.requires_grad = False


# In[19]:


from transformers import Trainer, TrainingArguments, DataCollatorWithPadding
import numpy as np

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {"accuracy": (predictions == labels).mean()}

pre_trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir='./trainerdata/',
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        num_train_epochs=1,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    ),
    train_dataset=tokenized_ds["train"],
    eval_dataset=tokenized_ds["test"],
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    compute_metrics=compute_metrics,
)
pre_trainer.train()
eval_before_tune = pre_trainer.evaluate()
print(eval_before_tune)


# In[ ]:





# In[ ]:





# In[ ]:





# ## Performing Parameter-Efficient Fine-Tuning
# 
# TODO: In the cells below, create a PEFT model from your loaded model, run a training loop, and save the PEFT model weights.

# In[20]:


from peft import get_peft_config, get_peft_model, LoraConfig, TaskType
peft_config = LoraConfig(
    task_type=TaskType.SEQ_CLS, 
    inference_mode=False, 
    r=8, 
    target_modules=["q_lin", "v_lin"],
    lora_alpha=32, 
    lora_dropout=0.1
)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name
)

# creating a PEFT model
peft_model = get_peft_model(model, peft_config)
peft_model.print_trainable_parameters()


# In[21]:


peft_trainer = Trainer(
    model=peft_model,
    args=TrainingArguments(
        output_dir='./peft_trainerdata/',
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        num_train_epochs=3,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    ),
    train_dataset=tokenized_ds["train"],
    eval_dataset=tokenized_ds["test"],
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    compute_metrics=compute_metrics,
)
peft_trainer.train()
peft_trainer.evaluate()
model_path = 'peft_model'
peft_model.save_pretrained(model_path)


# In[ ]:





# In[ ]:





# In[ ]:





# ## Performing Inference with a PEFT Model
# 
# TODO: In the cells below, load the saved PEFT model weights and evaluate the performance of the trained PEFT model. Be sure to compare the results to the results from prior to fine-tuning.

# In[22]:


from peft import AutoPeftModelForSequenceClassification, PeftConfig
lora_model = AutoPeftModelForSequenceClassification.from_pretrained(model_path,  num_labels=2)
config = PeftConfig.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)


# In[23]:


import pandas as pd
df = pd.DataFrame(tokenized_ds["test"])
df = df[["text", "label"]]
predictions = peft_trainer.predict(tokenized_ds["test"])
df["predicted_label"] = np.argmax(predictions[0], axis=1)
df.head(10)


# In[24]:


get_ipython().system('pip install evaluate')
get_ipython().system('pip install scikit-learn')
import evaluate


# In[25]:


accuracy_metric = evaluate.load("accuracy")
results = accuracy_metric.compute(references=df['label'], predictions=df['predicted_label'])
print(results)


# In[ ]:




