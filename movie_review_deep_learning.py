<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures
import tensorflow as tf
import pandas as pd

model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

URL = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"

dataset = tf.keras.utils.get_file(fname="aclImdb_v1.tar.gz", 
                                  origin=URL,
                                  untar=True,
                                  cache_dir='.',
                                  cache_subdir='')
=======
=======
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
import numpy as np
import pandas as pd
from fast_ml.model_development import train_valid_test_split
from transformers import Trainer, TrainingArguments, AutoConfig, AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch import nn
from torch.nn.functional import softmax
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import datasets

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print (f'Device Availble: {DEVICE}')

df = pd.read_csv('reviews.csv')
#df.drop(columns=['Unnamed: 0'], inplace=True)

df_reviews = df.loc[:, ['text', 'review']].dropna()
df_reviews['review'] = df_reviews['review'].apply(lambda x: f'{x}' if x != 1 else f'{x}')

le = LabelEncoder()
df_reviews['review'] = le.fit_transform(df_reviews['review'])

(train_texts, train_labels,
 val_texts, val_labels,
 test_texts, test_labels) = train_valid_test_split(df_reviews, target = 'review', train_size=0.8, valid_size=0.1, test_size=0.1)

train_texts = train_texts['text'].to_list()
train_labels = train_labels.to_list()
val_texts = val_texts['text'].to_list()
val_labels = val_labels.to_list()
test_texts = test_texts['text'].to_list()
test_labels = test_labels.to_list()

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
    
train_dataset = DataLoader(train_texts, train_labels)
val_dataset = DataLoader(val_texts, val_labels)
test_dataset = DataLoader(test_texts, test_labels)

f1 = datasets.load_metric('f1')
accuracy = datasets.load_metric('accuracy')
precision = datasets.load_metric('precision')
recall = datasets.load_metric('recall')
def compute_metrics(eval_pred):
    metrics_dict = {}
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    metrics_dict.update(f1.compute(predictions = predictions, references = labels, average = 'macro'))
    metrics_dict.update(accuracy.compute(predictions = predictions, references = labels))
    metrics_dict.update(precision.compute(predictions = predictions, references = labels, average = 'macro'))
    metrics_dict.update(recall.compute(predictions = predictions, references = labels, average = 'macro'))
    return metrics_dict

id2label = {idx:label for idx, label in enumerate(le.classes_)}
label2id = {label:idx for idx, label in enumerate(le.classes_)}
config = AutoConfig.from_pretrained('distilbert-base-uncased',
                                    num_labels = 10,
                                    id2label = id2label,
                                    label2id = label2id)
model = AutoModelForSequenceClassification.from_config(config)

training_args = TrainingArguments(
    output_dir='/kaggle/working/results',
    num_train_epochs=2,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    warmup_steps=500,
    weight_decay=0.05,
    report_to='none',
    evaluation_strategy='steps',
    logging_dir='/kagge/working/logs',
    logging_steps=25)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics)

trainer.train()

eval_results = trainer.predict(test_dataset)

print (eval_results.label_ids)

print (eval_results.metrics)

label2id_mapper = model.config.id2label
proba = softmax(torch.from_numpy(eval_results.predictions))
pred = [label2id_mapper[i] for i in torch.argmax(proba, dim = -1).numpy()]
actual = [label2id_mapper[i] for i in eval_results.label_ids]

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
trainer.save_model('sentiment_model')
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
trainer.save_model('sentiment_model')
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
trainer.save_model('sentiment_model')
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
=======
trainer.save_model('sentiment_model')
>>>>>>> 2ccba5a001118d5a724aa98c162e6ae3dca9aa15
