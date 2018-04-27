import data_generator 
from sample_models import *
import numpy as np
from data_generator import AudioGenerator
from keras import backend as K
from utils import int_sequence_to_text

from keras.layers import (BatchNormalization, Conv1D, Dense, Input, 
    TimeDistributed, Activation, Bidirectional, SimpleRNN, GRU, LSTM)

def TDNN_LSTM(input_dim, output_dim=29):
    """ Build a deep network for speech 
    """  
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    

    lstm1a = LSTM(250,activation="tanh",return_sequences=True)(input_data)
    lstm1b = LSTM(250,activation="tanh",return_sequences=True)(lstm1a)
    time_dense1 = TimeDistributed(Dense(200))(lstm1b)

    # Add batch normalization
    bn_td1 = BatchNormalization(name='bn_td1')(time_dense1)
    lstm2a = LSTM(150, activation='tanh',return_sequences=True)(bn_td1)
    lstm2b = LSTM(150, activation='tanh',return_sequences=True)(lstm2a)
    
    time_dense2 = TimeDistributed(Dense(120))(lstm2b)

    # Add batch normalization
    bn_td2 = BatchNormalization(name='bn_td2')(time_dense2)    
    lstm3a = LSTM(80, activation='tanh',return_sequences=True)(bn_td2)
    
    time_dense = TimeDistributed(Dense(output_dim))(lstm3a)
    # TODO: Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    # TODO: Specify model.output_length
    model.output_length = lambda x: x
    print(model.summary())
    return model

model = TDNN_LSTM(161, output_dim=29)

from train_utils import train_model

train_model(input_to_softmax=model, 
            pickle_path='model_lstm_stack_0425.pickle', 
            save_model_path='model_lstm_stack_0425.h5', spectrogram=True,
            epochs=50)
