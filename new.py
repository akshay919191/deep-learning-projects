import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense , Flatten , LSTM , Embedding , Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import imdb
from tensorflow.keras.callbacks import EarlyStopping


max_words = 10000

(X_train , y_train) , (x_test , y_test) = imdb.load_data(num_words = max_words)


from tensorflow.keras.preprocessing.sequence import pad_sequences

max_length = 500

x_pad = pad_sequences(X_train , maxlen = max_length)
x_te = pad_sequences(x_test , maxlen = max_length)

embedding_length = 32
x = 500

early_stop = EarlyStopping(patience = 3 , monitor = 'val_loss' , restore_best_weights = True)

model = Sequential([Embedding(input_dim = max_words,
                              output_dim = embedding_length,
                              input_length = x) ,
                              
                    LSTM(units = 100) ,
                    Dense(16 , activation = 'relu') ,
                    Dropout(0.5) ,
                    Dense(1 , activation = "sigmoid")])

model.summary()

model.compile(optimizer = Adam(learning_rate = 0.001) ,
              loss = "binary_crossentropy" ,
              metrics = ['accuracy'])

model.fit(x_pad , y_train , epochs = 10 , 
          validation_split = 0.2 , 
          batch_size = 64 ,
          callbacks = [early_stop])


loss , accuracy = model.evaluate(x_te , y_test , verbose = 0)

print(f"\nFinal Test Loss: {loss:.4f}")
print(f"Final Test Accuracy: {accuracy:.4f}")