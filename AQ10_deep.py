# -*- coding: utf-8 -*-
"""
Implimentation of AQ Dataset using Deep Learning
"""

# Process AQ Dataset

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from keras.callbacks import ReduceLROnPlateau, TensorBoard, EarlyStopping, ModelCheckpoint
from keras.losses import categorical_crossentropy
from keras.optimizers import Adam

import csv
#%%
MODELPATH = 'models/AQ10_model.h5'
dbpath_adult='Databases\Autism_Data_Adult_Version_2.csv';
dbpath_child='Databases\Autism-Child-Data.csv';
#db=2
strdb=input("Enter database number: 1 for Autism_Adult_Data and 2 for Autism-Child-Data\n" )
db=int(strdb)
if(db==1):
    dbpath=dbpath_adult
    db_data=[]
    with open(dbpath,mode='r')as f:
      csvreader = csv.reader(f)
      r=0;
      for row in csvreader:
          if (r==0):
           colNames=row
           r=1
          else:
           db_data.append(row)
    #      print(row)
    
    m=len(db_data)
    data=[]
    ASD_Class=[]
    for i in range(m):
        d=db_data[i][1:11]
        data.append(d)
        c=db_data[i][23]
        if (c=='YES'):
          ASD_Class.append(1)
        if (c=='NO'):
          ASD_Class.append(0)
if(db==2):
    dbpath=dbpath_child
    db_data=[]
    with open(dbpath,mode='r')as f:
      csvreader = csv.reader(f)
      r=0;
      for row in csvreader:
          if (r==0):
           colNames=row
           r=1
          else:
           db_data.append(row)
    #      print(row)
    
    m=len(db_data)
    data=[]
    ASD_Class=[]
    for i in range(m):
        d=db_data[i][0:10]
        data.append(d)
        c=db_data[i][20]
        if (c=='YES'):
          ASD_Class.append(1)
        if (c=='NO'):
          ASD_Class.append(0)

      
#%%   
      
x = np.array(data).astype(float)
seed = 7
y = np_utils.to_categorical(ASD_Class)

test_size = 0.30
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=test_size, random_state=seed)
model = Sequential()
model.add(Dense(10, activation='sigmoid', input_dim=10)) #10nodes in layer
model.add(Dense(20, activation='sigmoid')) #20nodes in layer
model.add(Dense(2, activation='softmax')) #2nodes in output layer
model.summary()
#model.compile(loss='categorical_crossentropy',
#              optimizer='adam',
#              metrics = ['accuracy'])
#model.fit(x_train, y_train, batch_size=50, epochs=1000)

batch_size=50
epochs=100
model.compile(loss=categorical_crossentropy,
              optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
              metrics=['accuracy'])
lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=3, verbose=1)

tensorboard = TensorBoard(log_dir='./logs')

early_stopper = EarlyStopping(monitor='val_loss', min_delta=0, patience=8, verbose=1, mode='auto')

checkpointer = ModelCheckpoint(MODELPATH, monitor='val_loss', verbose=1, save_best_only=True)

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test),
          shuffle=True,
          callbacks=[lr_reducer, tensorboard, early_stopper, checkpointer])


test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)
predictions = model.predict(x_test)

#amax=np.argmax(predictions[11])
#print(amax)
#print(predictions[11])
#s=np.sum(predictions[11])
#print(s)
#%%

#.................................to convert from categorical to list.........
a=len(y_test)
y1=[]
p1=[]
for i in range(a):
    amax=np.argmax(predictions[i])
    p1.append(amax)
    amax1=np.argmax(y_test[i])
    y1.append(amax1)
#...........................................................................
#  Performance Analysis
print(accuracy_score(y1, p1))
print(confusion_matrix(y1, p1))
print(classification_report(y1, p1))
#%%
#.................K-Fold Cross Validation...................................

#def deepml_model():
#    # Model Creation
#    deepml = Sequential()
#    deepml.add(Dense(10, input_dim=10, activation='relu'))
#    deepml.add(Dense(2, activation='softmax'))
#    # Model Compilation
#    deepml.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#    return deepml
#
#estimate = KerasClassifier(build_fn=deepml_model, epochs=20, batch_size=50, verbose=0)
#
#k_fold = KFold(n_splits=10, shuffle=True, random_state=seed)
#
#results = cross_val_score(estimate, x, y, cv=k_fold)
#print("Model: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))