# -*- coding: utf-8 -*-
"""SOMAS predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zbsQ4hYbQe4xZEiD4r1zCU_Z5zCh-eXW
"""

# SOMAS PREDICTOR

# imports
import tensorflow as tf
import pandas as pd
import csv
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, BatchNormalization
from keras.callbacks import LearningRateScheduler, ReduceLROnPlateau, EarlyStopping
from keras.optimizers import Adam
from keras import backend as K
import matplotlib.pyplot as plt
import pickle


tf.random.set_seed(1234)

# plot functions

def plot_error(history, filename, metric):
  """
    function to plot the training and validation errors and save the file in a .png file
    ----------------------------------
    @args:
      history (dict): The .fit() training history for loss metric extraction
      filename (str): Name of the filename to be saved
      metric (str): Name of the metric to be used (not loss)
  """

  if metric != None:
    fig, ax = plt.subplots(2,1)
    ax[0].plot(history.history[metric])
    ax[0].plot(history.history['val_'+metric])
    ax[0].legend(['Train', 'Val'])
    ax[0].set_title(f"{metric}")
    ax[0].set_ylabel(f"{metric}")
    ax[0].set_xlabel("Epoch")

    fig.subplots_adjust(hspace=0.5)

    ax[1].plot(history.history['loss'])
    ax[1].plot(history.history['val_loss'])
    ax[1].legend(["Train","Val"])
    ax[1].set_title("Model Loss")
    ax[1].set_ylabel("Loss")
    ax[1].set_xlabel("Epoch")
  else:
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(["Train","Val"])
    plt.set_title("Model Loss")
    plt.set_ylabel("Loss")
    plt.set_xlabel("Epoch")

  plt.savefig(filename)
  plt.show()


def visualise_data(output, modelName, filename = None):
  """
    function to visualise the progress data generated from prediction or training generation.
    Graph is a 3-D scatter plot with a color bar representing game progress.
    -------------------------------------
    @args:
      output (np.array):
      modelName (str): number of the model in string format
      filename (str): [default == None] name of the file to be save (if the user desires)
  """
  # extract the population and progress data
  selfish = output[:,0]
  selfless = output[:,1]
  collective = output[:,2]
  progress = output[:,3]

  fig = plt.figure(figsize=(7.5,6))
  ax = fig.add_subplot(111,projection='3d')

  img = ax.scatter(selfish, selfless, collective, c=progress, cmap='YlOrRd',alpha=1)
  ax.set_xlabel("Selfish")
  ax.set_ylabel("Selfless")
  ax.set_zlabel("Collective")
  fig.colorbar(img, shrink=0.5, pad=0.05, orientation = "horizontal")
  # change orientation so graphs are all in the same angle
  ax.view_init(-161,53)
  plt.title("Game Progress Using Prediction Model"+modelName+" Based On Population Construction")
  plt.show()
  if filename != None:
    plt.savefig(filename)

def plot_lr(history, filename):
  """
    function to plot the evolution of the learning rate over the course of training
    ---------------------------------------
    @args:
      history (dict): .fit() training history for data extraction
      filename(str): name of the file to be saved
  """
  lr = history.history['lr']  # extract the learning rate data
  plt.figure()
  plt.plot(range(0,len(lr)), lr)
  plt.title("Learning Rate Evolution")
  plt.ylabel("Learning Rate")
  plt.xlabel("Epochs")
  plt.savefig(filename)
  print("======== FILE SAVED =========")
  plt.show()

# import and visualise the dataframe
def data_import(filename):
  """
    function to import the .csv data and store as a pandas.dataframe
    -----------------------------------------
    @args:
      filename (str): name of the file to extract the .csv data
  """
  # read the .csv data into a pandas dataframe
  data = pd.read_csv(filename)
  print("================= VISUALISE DATAFRAME =================")
  print(data)

  return data

def create_data_sets(data):
  """
    function to create the training, test and validation data sets from the dataframe set
    -------------------------------------------
    @args:
      data (pandas.dataframe): the training input dataframe for extaction
  """
  # extract the data from the dataframe and convert into a numpy.array for training compatability
  input_data = data.iloc[:,[0,1,2]].to_numpy()
  labels = data.iloc[:,[3]].to_numpy()

  num_items = len(labels)
  # split the data into training, test and validation sets using a 70/20/10 split.
  X_train, X_test, X_val = input_data[:int(num_items*0.7)], input_data[int(num_items*0.7):int(num_items*0.9)], input_data[int(num_items*0.9):]
  Y_train, Y_test, Y_val = labels[:int(num_items*0.7)], labels[int(num_items*0.7):int(num_items*0.9)], labels[int(num_items*0.9):]

  return X_train, X_test, X_val, Y_train, Y_test, Y_val

# STEP 1: RESET THE WEIGHTS AND TENSOR FLOW SESSION
K.clear_session()
tf.compat.v1.reset_default_graph()

# STEP 2: DEFINE THE MACHINE LEARNING ALGORITHM

# modelName = "1"
# # model definition, training and validation steps
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3))
# model.add(Dense(32, activation='relu'))
# model.add(Dense(1))

################## MODEL 1_1 #######################
# first neural network model with the addition of batch noramlisation and drop out layers. Also with initialized kerenels and zero bias
# modelName = "1_1"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
# model.add(Dropout(0.3))
# model.add(Dense(32, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dense(1))
# earlystop = EarlyStopping(monitor="mean_squared_error", min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
############################################
################## MODEL 1_2 #######################
# first neural network model with the addition of batch noramlisation and drop out layers. Also with initialized kerenels and zero bias
# modelName = "1_2"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
# # model.add(Dropout(0.3))
# model.add(Dense(32, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dense(1))
# earlystop = EarlyStopping(monitor="mean_squared_error", min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
############################################
################## MODEL 1_3 #######################
# first neural network model with the addition of batch noramlisation and drop out layers. Also with initialized kerenels and zero bias
# modelName = "1_3"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
# # model.add(Dropout(0.3))
# model.add(Dense(32, activation='relu'))
# # model.add(BatchNormalization())
# model.add(Dense(1))
# earlystop = EarlyStopping(monitor="mean_squared_error", min_delta=0, patience=10, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
############################################
################## MODEL 1_4 #######################
# first neural network model with the addition of batch noramlisation and drop out layers. Also with initialized kerenels and zero bias
# modelName = "1_4"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
# model.add(Dropout(0.3))
# model.add(Dense(32, activation='relu'))
# # model.add(BatchNormalization())
# model.add(Dense(1))
# earlystop = EarlyStopping(monitor="mean_squared_error", min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
############################################
################## MODEL 1_5 #######################
# first neural network model with the addition of batch noramlisation and drop out layers. Also with initialized kerenels and zero bias
modelName = "1_5"
model = Sequential()
model.add(Dense(64, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
# model.add(BatchNormalization())
model.add(Dense(1))
earlystop = EarlyStopping(monitor="mean_squared_error", min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
############################################

################## MODEL 2 #########################
# # second model containing batch normalisation, dropout and normally distributed random initialized weights.
# modelName = "2"
# model = Sequential()
# model.add(Dense(128, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
# model.add(BatchNormalization())
# model.add(Dense(64, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dropout(0.3))
# model.add(Dense(32, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dense(1))
# # add early stopping and returning best weights
# earlystop = EarlyStopping(monitor='mean_absolute_error', min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
# # add dynamic learning rate based on plateau
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
###########################################

################## MODEL 3 #########################
# # second model containing batch normalisation, dropout and normally distributed random initialized weights.
# modelName = "3"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
# model.add(BatchNormalization())
# model.add(Dense(32, activation='relu'))
# model.add(BatchNormalization())
# # model.add(Dropout(0.3))
# model.add(Dense(16, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dense(1))
# # add early stopping and returning best weights
# # earlystop = EarlyStopping(monitor='mean_squared_error', min_delta=0, patience=15, verbose=0, mode='auto', baseline=500, restore_best_weights=True)
# # add dynamic learning rate based on plateau
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
###########################################

################## MODEL 3 mark 2 #########################
# # second model containing batch normalisation, dropout and normally distributed random initialized weights.
# modelName = "3_2"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3))
# model.add(BatchNormalization())
# model.add(Dense(32, activation='relu'))
# model.add(BatchNormalization())
# # model.add(Dropout(0.3))
# model.add(Dense(16, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dense(1))
# # add early stopping and returning best weights
# # earlystop = EarlyStopping(monitor='mean_squared_error', min_delta=0, patience=15, verbose=0, mode='auto', baseline=500, restore_best_weights=True)
# # add dynamic learning rate based on plateau
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
###########################################


################## MODEL 4 #########################
# # second model containing batch normalisation, dropout and normally distributed random initialized weights.
# modelName = "4"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
# # model.add(BatchNormalization())
# model.add(Dense(32, activation='relu'))
# # model.add(BatchNormalization())
# # model.add(Dropout(0.3))
# model.add(Dense(16, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dense(1))
# # add early stopping and returning best weights
# earlystop = EarlyStopping(monitor='mean_absolute_error', min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
# # add dynamic learning rate based on plateau
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
###########################################

################## MODEL 5 #########################
# # # second model containing batch normalisation, dropout and normally distributed random initialized weights.
# modelName = "5"
# model = Sequential()
# model.add(Dense(64, activation='relu', input_dim=3))
# # model.add(BatchNormalization())
# model.add(Dense(32, activation='relu'))
# # model.add(BatchNormalization())
# # model.add(Dropout(0.3))
# model.add(Dense(16, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dense(1))
# # add early stopping and returning best weights
# earlystop = EarlyStopping(monitor='mean_absolute_error', min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
# # add dynamic learning rate based on plateau
# reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=4, min_lr=0.00001, min_delta=0.01)
###########################################


print("=================== MODEL "+modelName+" SUMMARY ==================")
model.summary()

# add optimiser and compile the model
# opt = Adam(learning_rate=1e-3, decay=1e-3/200)
opt = Adam(learning_rate=1e-3)

# compile the model
# model.compile(loss="mean_absolute_percentage_error", optimizer=opt, metrics=["mean_absolute_percentage_error"])
model.compile(loss="mean_absolute_error", optimizer=opt, metrics=["mean_squared_error"])

# import data as a pandas.dataframe from the generated training data
data = data_import('training_data_dynamic.csv')
# create the training, test and validation training set (with labels)
X_train, X_test, X_val, Y_train, Y_test, Y_val = create_data_sets(data)
print(f"The shapes of the data are as follows: train: {len(X_train)}, test: {len(X_test)}, validation: {len(X_val)}")

# train the model
print("================= TRAINING MODEL =================")
history = model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=300, batch_size=64, callbacks=[reduce_lr, earlystop], verbose=1)
# history = model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=300, batch_size=64, callbacks=[reduce_lr], verbose=1)

#######################
###### EDIT HERE ######
#######################

# save the model as a .h5 file
model.save("progress_predictor_"+modelName+".h5")

# save the .fit() training history for use later on
df = pd.DataFrame(history.history)
df.to_csv("trainingHistoryModel"+modelName+".csv", index=False)

# pickle sucks
# with open('trainingHisotryModel'+modelName, 'wb') as file_pi:
#     pickle.dump(history.history, file_pi)
#######################
#######################

print("saved model "+modelName)
# code to re-load the model
# model = load_model('model.h5')

# visualise the training model
# loss = history.history['loss']
# val_loss = history.history['val_loss']

#######################
###### EDIT HERE ######
#######################
plot_error(history, "loss_graph_model"+modelName+".png", 'mean_squared_error')
#######################
#######################

# plot the evolution of the learning rate
#######################
###### EDIT HERE ######
#######################
plot_lr(history, "lr_evolution_model"+modelName+".png")
#######################
#######################

# FOR USE IN CASE OF DISCONNECT OR RETRY

# model = load_model('progress_predictor_1.1.h5')
# model = load_model('progress_predictor_2.h5')
# model = load_model('progress_predictor_3.h5')

# LOAD MODEL HISTORY FOR FURTHER PLOTTING
# with open('/trainingHistoryModel3_3', "rb") as file_pi:
#     history = pickle.load(file_pi)

# evaluate the model using the testing dataset
score = model.evaluate(X_test, Y_test, verbose=1)
print('Test loss:', score[0])
print('Test metric:', score[1])

# prediction step using a parameter sweep of population construction

# import the parameter sweep data as a pandas.dataframe
df = pd.read_csv('parametersSweepData.csv')

# extract data into a numpy.array for model compatebility
predict_data = df.iloc[:,[0,1,2]].to_numpy()

# run predictions on every population construction
predicted_progress = model.predict(predict_data, verbose=2, batch_size=32)

# concatenate outputs to conform to standard progress/population datasets
output = np.concatenate((predict_data, predicted_progress), axis=1)
# save output as csv file
dict = {
    "Selfish": output[:,0],
    "Selfless": output[:,1],
    "Collective": output[:,2],
    "Progress": output[:,3]
}
df = pd.DataFrame(dict)

#######################
###### EDIT HERE ######
#######################
df.to_csv("prediction_results_model"+modelName+".csv", index=False)
#######################
#######################

# visualise the output data
#######################
###### EDIT HERE ######
#######################
visualise_data(output, modelName, "Predicted Progress (model"+modelName+").png")
# visualise_data(output) # supress file save
#######################
#######################

# extract the maximum level
max=np.max(predicted_progress)
# find index of the max level progress and extract the population construction
idx=np.where(predicted_progress==max)
print(f"Max progress made with population - Selfish: {predict_data[idx,0]}, Selfless: {predict_data[idx,1]}, Collective: {predict_data[idx,2]}")
print(f"The max progress was: {predicted_progress[idx]}")

print("Therefore the optimum population dynamics are - [0,90,0] or [0,57,33] - where [selfish, selfless, collective]")

print(idx)

# Loading in the saved models and re-evaluating to regenerate the data... just in case.

# continued learning for model 3

# model3 = load_model("progress_predictor_3.h5")

# model3.evaluate(X_test, Y_test, verbose=1)

# print("==========")

# model1 = load_model("progress_predictor_1.h5")

# model1.evaluate(X_test, Y_test, verbose=1)

# print("===========")

# model1_1 = load_model("progress_predictor_1.1.h5")

# model1_1.evaluate(X_test, Y_test, verbose=1)

# df = pd.DataFrame(history.history)
# df.to_csv("trainingHistoryModel"+modelName+".csv", index=False)
