
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import cv2                  
import numpy as np  
from tqdm import tqdm
import os                   
from random import shuffle  
from zipfile import ZipFile
from PIL import Image

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,roc_auc_score
from sklearn.preprocessing import LabelEncoder

#dl libraraies
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop
from keras.utils import to_categorical
import pickle

import tensorflow as tf
print(tf.__version__)

#import tensorflowjs as tfjs

X=[] #for features
Z=[] #for labels
#IMG_SIZE=150
IMG_SIZE=28

def assign_label(img,letter_type):
    return letter_type

def make_train_data(letter_type,DIR):
    for img in DIR:
        label=assign_label(img,letter_type)
        #path = os.path.join(DIR,img)
        img = cv2.imread(img,0)#load the image
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))#resize the image
        
        X.append(np.array(img))
        Z.append(str(label))

data_path = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\Datasets\\Hnd\\Sample\\mod_img"
Sample001 = data_path + '\\Sample001'
Sample002 = data_path + '\\Sample002'
Sample003 = data_path + '\\Sample003'
Sample004 = data_path + '\\Sample004'
Sample005 = data_path + '\\Sample005'

X=[] #for features
Z=[] #for labels
#IMG_SIZE=150
IMG_SIZE=28

def assign_label(img,letter_type):
    return letter_type

def make_train_data(letter_type,DIR):
    for img in tqdm(os.listdir(DIR)):
        label=assign_label(img,letter_type)
        path = os.path.join(DIR,img)
        img = cv2.imread(path,0)#load the image
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))#resize the image
        
        X.append(np.array(img))
        Z.append(str(label))

make_train_data('001',Sample001)
make_train_data('002',Sample002)
make_train_data('003',Sample003)
make_train_data('004',Sample004)
make_train_data('005',Sample005)


#no of class labels
n = 5

#X=np.array(X)
#X=X/255

X = np.array(X)
#X = X.reshape([28, 28, 1])
X = X.reshape([-1, 28, 28,1])
X = X/255.0

#Label encoding on Y 
le=LabelEncoder()
Y=le.fit_transform(Z)
Y=to_categorical(Y,n)

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=42)

# define the model architecture
model = keras.Sequential([
    keras.layers.Conv2D(32, (5, 5), padding="same", input_shape=[28, 28, 1]),
    keras.layers.MaxPool2D((2,2)),
    keras.layers.Conv2D(64, (5, 5), padding="same"),
    keras.layers.MaxPool2D((2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(n, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

batch_size=128
no_of_epochs=10

model.fit(x_train,y_train, validation_data=(x_test,y_test), epochs=no_of_epochs)


import matplotlib.pyplot as plt

acc = model.history['acc']
val_acc = model.history['val_acc']
loss = model.history['loss']
val_loss = model.history['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()


###############################################


# save the model to disk
# Pkl_Filename = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\ModelBuild\\kanadda_model\\kanadda_pickle.pkl"  

# #from multiprocessing import Lock
# #lock = Lock()

# with open(Pkl_Filename, 'wb') as file:
#      pickle.dump(model, file)

# tfjs.converters.save_keras_model(model, 'kanadda_model_tfjs')
# print("tfjs Saved model to disk")

# Saving the model
model_json = model.to_json()
with open("C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\OCR_Detection_Project\\models\\model.json", "w") as json_file :
	json_file.write(model_json)

model.save_weights("C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\OCR_Detection_Project\\models\\cnn_model\\model.h5")
print("Saved model to disk")

model.save('C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\OCR_Detection_Project\\models\\cnn_model\\CNN.model')

model.save('C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\OCR_Detection_Project\\models\\model.hdf5')


# #load the model from saved location
# model = tf.keras.models.load_model("C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\OCR_Detection_Project\\cnn_model\\CNN.model")
# #prediction
# #With the model trained, you can use it to make predictions about some images. The model's linear outputs, logits. Attach a softmax layer to convert the logits to probabilities, which are easier to interpret.
# probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
# predictions = probability_model.predict(x_test)
# predictions[0]
# np.argmax(predictions[0])

# #verify predictions
# import matplotlib.pyplot as plt
# i = 0
# plt.figure(figsize=(6,3))
# plt.subplot(1,2,1)
# plot_image(i, predictions[i], test_labels, test_images)
# plt.subplot(1,2,2)
# plot_value_array(i, predictions[i],  test_labels)
# plt.show()


#test prediction

import cv2
import tensorflow as tf
CATEGORIES = ["001", "002", "003", "004", "005"]

def prepare(file):
    IMG_SIZE = 28
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

model = tf.keras.models.load_model("C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\OCR_Detection_Project\\models\\cnn_model\\CNN.model")
image = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\Datasets\\for_test\\img004-002.png" #your image path
#image = input()
image = prepare(image)
prediction = model.predict([image])
prediction = list(prediction[0])
print(CATEGORIES[prediction.index(max(prediction))])

