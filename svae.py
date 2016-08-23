'''
This script demonstrates how to build a variational autoencoder with Keras.
Reference: "Auto-Encoding Variational Bayes" https://arxiv.org/abs/1312.6114
'''
import numpy as np
import matplotlib.pyplot as plt
import tensor

from keras.layers import Input, Dense, Lambda, LSTM, RepeatVector, TimeDistributed
from keras.models import Model
from keras import backend as K
from keras import objectives


batch_size = 20
embedim = 98
maxlen = 300
rnnDim = 50
latentDim = 2
nb_epoch = 50

x = Input(batch_shape=(batch_size, maxlen, embedim))
#e1 = LSTM(rnnDim, activation='relu', return_sequences=True )(x)
#e2 = LSTM(rnnDim, activation='relu', return_sequences=True )(e1)
e3 = LSTM(rnnDim, activation='relu')(x)

z_mean = Dense(latentDim)(e3)
z_log_var = Dense(latentDim)(e3)

def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(shape=(batch_size, latentDim), mean=0.)
    return z_mean + K.exp(z_log_var / 2) * epsilon

# note that "output_shape" isn't necessary with the TensorFlow backend
z = Lambda(sampling)([z_mean, z_log_var])

# we instantiate these layers separately so as to reuse them later
decoded_mean = RepeatVector(maxlen)(z)
d3 = LSTM(embedim, activation='relu', return_sequences=True)(decoded_mean)
#d2 = LSTM(rnnDim, activation='relu', return_sequences=True)(d3)
#d1 = LSTM(embedim, activation='relu', return_sequences=True)(d2)
output = d3

def vae_loss(x, x_decoded_mean):
    xent_loss = embedim * K.sum(objectives.binary_crossentropy(x, x_decoded_mean), axis=-1)
    kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
    return xent_loss + kl_loss

vae = Model(x, output)

print(vae.summary())

vae.compile(optimizer='rmsprop', loss=vae_loss)

train = tensor.toCorpusTensor("sentence/sentence0.txt")

vae.fit(train, train,
        shuffle=True,
        nb_epoch=nb_epoch,
        batch_size=batch_size)
        #validation_data=(x_test, x_test))

exit()

# build a model to project inputs on the latent space
encoder = Model(x, z_mean)

# display a 2D plot of the digit classes in the latent space
x_test_encoded = encoder.predict(train, batch_size=batch_size)
