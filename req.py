import tensorflow as tf
from tensorflow.keras import layers

D_MODEL = 1024
NUM_HEAD = 8
N_TOKENS = 196

layer = layers.MultiHeadAttention(num_heads = NUM_HEAD ,
                                  key_dim = D_MODEL // NUM_HEAD)

sample_input = tf.random.normal(shape = (32 , N_TOKENS , D_MODEL))

output = layer(query = sample_input , 
               key = sample_input ,
               value = sample_input)


print(output.shape)