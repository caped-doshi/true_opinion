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
