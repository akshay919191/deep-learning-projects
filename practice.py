import tensorflow as tf
from tensorflow.keras import layers




def cross_attention(visual_feature , num_head , text_embedd , key_dim):
    norm_visual = layers.LayerNormalization(epsilon = 1e-6)(visual_feature)

    attn_output = layers.MultiHeadAttention(num_heads = num_head , 
                                            key_dim = key_dim,
                                            Dropout = 0.1)(query = norm_visual , key = text_embedd , value = text_embedd)
    
    x = layers.Add()([visual_feature , attn_output])

    norm_ffn = layers.LayerNormalization(epsilon = 1e-6)(x)
    ffn_output = layers.Dense(key_dim * 4 , activation = 'gelu')(norm_ffn)
    ffn_output = layers.Dense(key_dim)(ffn_output)

    output = layers.Add([x , ffn_output])

    return output

