<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from movie_tweets import Twitter_Query
import tensorflow as tf
from tensorflow import keras
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures

class Reconstructed_Model:
    def __init__(self,file: str):
        self.reconstructed_model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.reconstructed_model.load_weights(file)

        self.tq = Twitter_Query()
    
    def get_sentiment_analysis(self,input: list):
        tf_batch = self.tokenizer(input, max_length=128, padding=True, truncation=True, return_tensors='tf')
        tf_outputs = self.reconstructed_model(tf_batch)
        tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
        labels = ['Negative','Positive']
        label = tf.argmax(tf_predictions, axis=1)
        label = label.numpy()

        positive_count = 0
        negative_count = 0
        for i in range(len(input)):
            if labels[label[i]] == 'Negative':
                negative_count += 1
            else:
                positive_count += 1
        ratio =  (positive_count/ (positive_count + negative_count))
        ratio = round(ratio, 2)
        return float(str(ratio))
=======
=======
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
import pandas as pd
import numpy as np
from transformers import Trainer, TrainingArguments, AutoConfig, AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch import nn
from torch.nn.functional import softmax

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print (f'Device Availble: {DEVICE}')

class DataLoader(torch.utils.data.Dataset):
    def __init__(self, sentences=None, labels=None):
        self.sentences = sentences
        self.labels = labels
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        
        if bool(sentences):
            self.encodings = self.tokenizer(self.sentences,
                                            truncation = True,
                                            padding = True)
        
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        
        if self.labels == None:
            item['labels'] = None
        else:
            item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.sentences)
    
    
    def encode(self, x):
        return self.tokenizer(x, return_tensors = 'pt').to(DEVICE)

class SentimentModel():
    
    def __init__(self, model_path):
        
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path).to(DEVICE)
        args =  TrainingArguments(output_dir='/working/results', per_device_eval_batch_size=64)
        self.batch_model = Trainer(model = self.model, args= args)
        self.single_dataloader = DataLoader()
        
    def batch_predict_proba(self, x):
        
        predictions = self.batch_model.predict(DataLoader(x))
        logits = torch.from_numpy(predictions.predictions)
        
        if DEVICE == 'cpu':
            proba = torch.nn.functional.softmax(logits, dim = 1).detach().numpy()
        else:
            proba = torch.nn.functional.softmax(logits, dim = 1).to('cpu').detach().numpy()
        return proba
        
        
    def predict_proba(self, x):
        
        x = self.single_dataloader.encode(x).to(DEVICE)
        predictions = self.model(**x)
        logits = predictions.logits
        
        if DEVICE == 'cpu':
            proba = torch.nn.functional.softmax(logits, dim = 1).detach().numpy()
        else:
            proba = torch.nn.functional.softmax(logits, dim = 1).to('cpu').detach().numpy()
        return proba


df = pd.read_csv('reviews.csv')
#df.drop(columns = ['Unnamed: 0'], inplace = True)

df_reviews = df.loc[:, ['text', 'review']].dropna()
df_reviews['review'] = df_reviews['review'].apply(lambda x: f'{x}' if x != 1 else f'{x}')

single_sentence = "good great very good amazing"

sentiment_model = SentimentModel('./sentiment_model')

single_sentence_probas = sentiment_model.predict_proba(single_sentence)
id2label = sentiment_model.model.config.id2label
predicted_class_label = id2label[np.argmax(single_sentence_probas)]
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
print (predicted_class_label)
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
print (predicted_class_label)
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
print (predicted_class_label)
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
print (predicted_class_label)
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
