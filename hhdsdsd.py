import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout , Dense , GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam

(X_train , y_train) , (X_test , y_test) = tf.keras.datasets.cifar10.load_data()

X_train = X_train.astype('float32') 
X_test = X_test.astype('float32') 


xp = preprocess_input(X_train)
Xtp = preprocess_input(X_test)

base_model = MobileNetV2(
    input_shape = (32 , 32 , 3), 
    include_top = False ,
    weights = 'imagenet'
)

base_model.trainable = True

model = Sequential([
    base_model , 
    GlobalAveragePooling2D() ,
    Dense(200 , activation = "relu"),
    Dropout(0.4),
    Dense(10 , activation = "softmax")]
)


model.compile(optimizer = Adam(learning_rate = 0.0005), 
              loss = "sparse_categorical_crossentropy",
              metrics = ['accuracy'])


model.fit(xp , y_train , epochs = 15 , batch_size = 32 , validation_split = 0.2)


loss , accuracy = model.evaluate(Xtp , y_test , verbose = 0)