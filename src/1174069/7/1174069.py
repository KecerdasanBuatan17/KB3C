# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 22:10:00 2020

@author: FannyShafira
"""

# In[1]:import lib
# menimport libtari CSV untuk mengolah data ber ekstensi csv
import csv 
#kemudian Melakukan import library Image yang berguna untuk dari PIL atau Python Imaging Library yang berguna untuk mengolah data berupa gambar
from PIL import Image as pil_image 
# kemudian Melakukan import library keras yang menggunakan method preprocessing yang digunakan untuk membuat neural network
import keras.preprocessing.image

# In[2]:load all images (as numpy arrays) and save their classes
#Menginisiasi variabel imgs dan classes dengan variabel array kosong
imgs = []
classes = []
#membuaka file hasy-data-labels.csv yang berada di folede HASYv2 yang di inisialisasi menjadi csvfile
with open('F://Semester 6/Artificial Intelligence/Tugas 7/New Folder/hasy-data-labels.csv') as csvfile:
    #Menginisiasi variabel csvreader yang berisi method csv.reader yang membaca variabel csvfile
    csvreader = csv.reader(csvfile)
    # Menginisiasi variabel i dengan isi 0
    i = 0
    # membuat looping pada variabel csvreader
    for row in csvreader:
        # dengan ketentuan jika i lebihkecil daripada o
        if i > 0:
            # dibuat variabel img dengan isi keras untuk aktivasi neural network fungsi yang membaca data yang berada dalam folder HASYv2 dengan input nilai -1.0 dan 1.0
            img = keras.preprocessing.image.img_to_array(pil_image.open("F://Semester 6/Artificial Intelligence/Tugas 7/New Folder/" + row[0]))
            #Pembagian data yang ada pada fungsi img sebanyak 255.0
            img /= 255.0
            # Penambahan nilai baru pada imgs pada row ke 1 2 dan dilanjutkan dengan variabel img
            imgs.append((row[0], row[2], img))
            # Penambahan nilai pada row ke 2 pada variabel classes
            classes.append(row[2])
            # penambahan nilai satu pada variabel i
        i += 1

# In[3]:shuffle the data, split into 80% train, 20% test
# Melakukan import library random 
import random
# melakukan random pada vungsi imgs
random.shuffle(imgs)
# Menginisiasi variabel split_idx dengan nilai integer 80 persen dikali dari pengembalian jumlah dari variabel imgs
split_idx = int(0.8*len(imgs))
# Menginisiasi variabel train dengan isi lebih besar split idx
train = imgs[:split_idx]
# Menginisiasi variabel test dengan isi lebih kecil split idx
test = imgs[split_idx:]

# In[4]: 
# Melakukan import library numpy dengan inisial np
import numpy as np
# Menginisiasi variabel train input dengan np method asarray yang mana membuat array dengan isi row 2 dari data train
train_input = np.asarray(list(map(lambda row: row[2], train)))
# membuat test input input dengan np method asarray yang mana membuat array dengan isi row 2 dari data test
test_input = np.asarray(list(map(lambda row: row[2], test)))
# Menginisiasi variabel train_output dengan np method asarray yang mana membuat array dengan isi row 1 dari data train
train_output = np.asarray(list(map(lambda row: row[1], train)))
# Menginisiasi variabel test_output dengan np method asarray yang mana membuat array dengan isi row 1 dari data test
test_output = np.asarray(list(map(lambda row: row[1], test)))

# In[5]: import encoder and one hot
# Melakukan import library LabelEncode dari sklearn
from sklearn.preprocessing import LabelEncoder
# Melakukan import library OneHotEncoder dari sklearn
from sklearn.preprocessing import OneHotEncoder

# In[6]:convert class names into one-hot encoding

# Menginisiasi variabel label_encoder dengan isi LabelEncoder
label_encoder = LabelEncoder()
# Menginisiasi variabel integer_encoded yang berfungsi untuk Menconvert variabel classes kedalam bentuk integer
integer_encoded = label_encoder.fit_transform(classes)

# In[7]:then convert integers into one-hot encoding
# Menginisiasi variabel onehot_encoder dengan isi OneHotEncoder
onehot_encoder = OneHotEncoder(sparse=False)
# mengisi variabel integer_encoded dengan isi integer_encoded yang telah di convert pada fungsi sebelumnya
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
# Menconvert variabel integer_encoded kedalam onehot_encoder
onehot_encoder.fit(integer_encoded)

# In[8]:convert train and test output to one-hot
# Menconvert data train output  mengguanakn variabel label_encoder kedalam variabel train_output_int
train_output_int = label_encoder.transform(train_output)
# Menconvert variabel train_output_int kedalam fungsi onehot_encoder 
train_output = onehot_encoder.transform(train_output_int.reshape(len(train_output_int), 1))
# Menconvert data test_output mengguanakn variabel label_encoder kedalam variabel test_output_int
test_output_int = label_encoder.transform(test_output)
# Menconvert variabel test_output_int kedalam fungsi onehot_encoder 
test_output = onehot_encoder.transform(test_output_int.reshape(len(test_output_int), 1))
# Menginisiasi variabel num_classes dengan isi variabel label_encoder dan classess
num_classes = len(label_encoder.classes_)
# mencetak hasil dari nomer Class beruapa persen 
print("Number of classes: %d" % num_classes)

# In[9]: import sequential
# Melakukan import library Sequential dari Keras
from keras.models import Sequential
# Melakukan import library Dense, Dropout, Flatten dari Keras
from keras.layers import Dense, Dropout, Flatten
# Melakukan import library Conv2D, MaxPooling2D dari Keras
from keras.layers import Conv2D, MaxPooling2D

# In[10]: desain jaringan
# Menginisiasi variabel model dengan isian library Sequential
model = Sequential()
# variabel model di tambahkan library Conv2D tigapuluh dua bit dengan ukuran kernel 3 x 3 dan fungsi penghitungan relu dang menggunakan data train_input
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',
                 input_shape=np.shape(train_input[0])))
# variabel model di tambahkan dengan lib MaxPooling2D dengan ketentuan ukuran 2 x 2 pixcel 
model.add(MaxPooling2D(pool_size=(2, 2)))
# variabel model di tambahkan dengan library Conv2D 32bit dengan kernel 3 x 3
model.add(Conv2D(32, (3, 3), activation='relu'))
# variabel model di tambahkan dengan lib MaxPooling2D dengan ketentuan ukuran 2 x 2 pixcel 
model.add(MaxPooling2D(pool_size=(2, 2)))
# variabel model di tambahkan library Flatten
model.add(Flatten())
# variabel model di tambahkan library Dense dengan fungsi tanh
model.add(Dense(1024, activation='tanh'))
# variabel model di tambahkan library dropout untuk memangkas data tree sebesar 50 persen
model.add(Dropout(0.5))
# variabel model di tambahkan library Dense dengan data dari num_classes dan fungsi softmax
model.add(Dense(num_classes, activation='softmax'))
# mengkompile data model untuk mendapatkan data loss akurasi dan optimasi
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
# mencetak variabel model kemudian memunculkan kesimpulan berupa data total parameter, trainable paremeter dan bukan trainable parameter
print(model.summary())

# In[11]: import sequential
# Melakukan import library keras callbacks
import keras.callbacks
# Menginisiasi variabel tensorboard dengan isi lib keras 
tensorboard = keras.callbacks.TensorBoard(log_dir='./logs/mnist-style')

# In[12]: 5menit kali 10 epoch = 50 menit
# fungsi model titambahkan metod fit untuk mengetahui perhitungan dari train_input train_output
model.fit(train_input, train_output,
# dengan batch size 32 bit 
          batch_size=32,
          epochs=10,
          verbose=2,
          validation_split=0.2,
          callbacks=[tensorboard])

score = model.evaluate(test_input, test_output, verbose=2)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# In[13]:try various model configurations and parameters to find the best
# Melakukan import library time 
import time
#Menginisiasi variabel result dengan array kosong
results = []
# melakukan looping dengan ketentuan konvolusi 2 dimensi 1 2 
for conv2d_count in [1, 2]:
    # menentukan ukuran besaran fixcel dari data atau konvert 1 fixcel mnjadi data yang berada pada codigan dibawah.
    for dense_size in [128, 256, 512, 1024, 2048]:
        # membuat looping untuk memangkas masing-masing data dengan ketentuan 0 persen 25 persen 50 persen dan 75 persen.
        for dropout in [0.0, 0.25, 0.50, 0.75]:
            # Menginisiasi variabel model Sequential
            model = Sequential()
            #membuat looping untuk variabel i dengan jarak dari hasil konvolusi.
            for i in range(conv2d_count):
                # syarat jika i samadengan bobotnya 0
                if i == 0:
                    # Penambahan method add pada variabel model dengan konvolusi 2 dimensi 32 bit didalamnya dan membuat kernel dengan ukuran 3 x 3 dan rumus aktifasi relu dan data shape yang di hitung dari data train.
                    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=np.shape(train_input[0])))
                    # jika tidak
                else:
                    # Penambahan method add pada variabel model dengan konvolusi 2 dimensi 32 bit dengan ukuran kernel 3 x3 dan fungsi aktivasi relu
                    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
                # Penambahan method add pada variabel model dengan isian method  Max pooling berdimensi 2 dengan ukuran fixcel 2 x 2.
                model.add(MaxPooling2D(pool_size=(2, 2)))
            # merubah feature gambar menjadi 1 dimensi vektor
            model.add(Flatten())
            # Penambahan method dense untuk pemadatan data dengan ukuran dense di tentukan dengan rumus fungsi tanh.
            model.add(Dense(dense_size, activation='tanh'))
            # membuat ketentuan jika pemangkasan lebih besar dari 0 persen
            if dropout > 0.0:
                # Penambahan method dropout pada model dengan nilai dari dropout
                model.add(Dropout(dropout))
                # Penambahan method dense dengan fungsi num classs dan rumus softmax
            model.add(Dense(num_classes, activation='softmax'))
            # mongkompile variabel model dengan hasi loss optimasi dan akurasi matrix
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            # melakukan log pada dir 
            log_dir = './logs/conv2d_%d-dense_%d-dropout_%.2f' % (conv2d_count, dense_size, dropout)
            # Menginisiasi variabel tensorboard dengan isian dari library keras dan nilai dari lig dir
            tensorboard = keras.callbacks.TensorBoard(log_dir=log_dir)
            # Menginisiasi variabel start dengan isian dari library time menggunakan method time

            start = time.time()
            # Penambahan method fit pada model dengan data dari train input train output nilai batch nilai epoch verbose nilai 20 persen validation split dan callback dengan nilai tnsorboard.
            model.fit(train_input, train_output, batch_size=32, epochs=10,
                      verbose=0, validation_split=0.2, callbacks=[tensorboard])
            # Menginisiasi variabel score dengan nilai evaluasi dari model menggunakan data tes input dan tes output
            score = model.evaluate(test_input, test_output, verbose=2)
            # Menginisiasi variabel end 
            end = time.time()
            # Menginisiasi variabel elapsed
            elapsed = end - start
            # mencetak hasil perhitungan
            print("Conv2D count: %d, Dense size: %d, Dropout: %.2f - Loss: %.2f, Accuracy: %.2f, Time: %d sec" % (conv2d_count, dense_size, dropout, score[0], score[1], elapsed))
            results.append((conv2d_count, dense_size, dropout, score[0], score[1], elapsed))

# In[14]:rebuild/retrain a model with the best parameters (from the search) and use all data
# Menginisiasi variabel model dengan isian library Sequential
model = Sequential()
# variabel model di tambahkan library Conv2D tigapuluh dua bit dengan ukuran kernel 3 x 3 dan fungsi penghitungan relu dang menggunakan data train_input
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=np.shape(train_input[0])))
# variabel model di tambahkan dengan lib MaxPooling2D dengan ketentuan ukuran 2 x 2 pixcel
model.add(MaxPooling2D(pool_size=(2, 2)))
# variabel model di tambahkan dengan library Conv2D 32bit dengan kernel 3 x 3
model.add(Conv2D(32, (3, 3), activation='relu'))
# variabel model di tambahkan dengan lib MaxPooling2D dengan ketentuan ukuran 2 x 2 pixcel
model.add(MaxPooling2D(pool_size=(2, 2)))
# variabel model di tambahkan library Flatten
model.add(Flatten())
# variabel model di tambahkan library Dense dengan fungsi tanh
model.add(Dense(128, activation='tanh'))
# variabel model di tambahkan library dropout untuk memangkas data tree sebesar 50 persen
model.add(Dropout(0.5))
# variabel model di tambahkan library Dense dengan data dari num_classes dan fungsi softmax
model.add(Dense(num_classes, activation='softmax'))
# mengkompile data model untuk mendapatkan data loss akurasi dan optimasi
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# mencetak variabel model kemudian memunculkan kesimpulan berupa data total parameter, trainable paremeter dan bukan trainable parameter
print(model.summary())

# In[15]:join train and test data so we train the network on all data we have available to us
# melakukan join numpy menggunakan data train_input test_input
model.fit(np.concatenate((train_input, test_input)),
          # kelanjutan data yang di gunakan pada join train_output test_output
          np.concatenate((train_output, test_output)),
          #menggunakan ukuran 32 bit dan epoch 10 
          batch_size=32, epochs=10, verbose=2)

# In[16]:save the trained model
#menyimpan model atau mengeksport model yang telah di jalantadi
model.save("mathsymbols.model")

# In[17]:save label encoder (to reverse one-hot encoding)
# menyompan label encoder dengan nama classes.npy 
np.save('classes.npy', label_encoder.classes_)

# In[18]:load the pre-trained model and predict the math symbol for an arbitrary image;
# the code below could be placed in a separate file
# mengimpport library keras model
import keras.models
# Menginisiasi variabel model2 untuk meload model yang telah di simpan tadi
model2 = keras.models.load_model("mathsymbols.model")
# mencetak hasil model2
print(model2.summary())

# In[19]:restore the class name to integer encoder
# Menginisiasi variabel label encoder ke 2 dengan isian fungsi label encoder.
label_encoder2 = LabelEncoder()
# Penambahan method classess dengan data classess yang di eksport tadi
label_encoder2.classes_ = np.load('classes.npy')
# membuat fumgsi predict dengan path img
def predict(img_path):
    # Menginisiasi variabel newimg dengam membuay immage menjadi array dan membuka data berdasarkan img path
    newimg = keras.preprocessing.image.img_to_array(pil_image.open(img_path))
    # membagi data yang terdapat pada variabel newimg sebanyak 255
    newimg /= 255.0

    # do the prediction
    # Menginisiasi variabel predivtion dengan isian variabel model2 menggunakan fungsi predic dengan syarat variabel newimg dengan data reshape
    prediction = model2.predict(newimg.reshape(1, 32, 32, 3))

    # figure out which output neuron had the highest score, and reverse the one-hot encoding
    # Menginisiasi variabel inverted  denagan label encoder2 dan  menggunakan argmax untuk mencari skor luaran tertinggi
    inverted = label_encoder2.inverse_transform([np.argmax(prediction)])
    # mencetak prediksi gambar dan confidence dari gambar.
    print("Prediction: %s, confidence: %.2f" % (inverted[0], np.max(prediction)))

# In[20]: grab an image (we'll just use a random training image for demonstration purposes)
# mencari prediksi menggunakan fungsi prediksi yang di buat tadi dari data di HASYv2/hasy-data/v2-00010.png
predict("F://Semester 6/Artificial Intelligence/Tugas 7/New Folder/hasy-data/v2-00010.png")
# mencari prediksi menggunakan fungsi prediksi yang di buat tadi dari data di HASYv2/hasy-data/v2-00500.png
predict("F://Semester 6/Artificial Intelligence/Tugas 7/New Folder/hasy-data/v2-00500.png")
# mencari prediksi menggunakan fungsi prediksi yang di buat tadi dari data di HASYv2/hasy-data/v2-00700.png
predict("F://Semester 6/Artificial Intelligence/Tugas 7/New Folder/hasy-data/v2-00700.png")