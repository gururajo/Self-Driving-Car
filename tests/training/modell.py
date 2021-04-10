from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten
def getanothermodel():
    model = Sequential()

    model.add(Conv2D(filters=24, kernel_size=3,input_shape=(320, 320, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=36, kernel_size=3,activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=48, kernel_size=3,activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=3,activation='relu'))#1
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=3,activation='relu'))#2
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='softmax'))


    model.compile(loss='mse',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

def getmodel():
    model = Sequential()

    model.add(Conv2D(filters=24, kernel_size=3,strides=2,input_shape=(66,200, 3), activation='relu'))
    
    model.add(Conv2D(filters=36, kernel_size=3,strides=2,activation='relu'))
    
    model.add(Conv2D(filters=48, kernel_size=3,strides=2,activation='relu'))
    

    model.add(Conv2D(filters=64, kernel_size=3,strides=2,activation='relu'))#1
    
    model.add(Conv2D(filters=64, kernel_size=3,strides=2,activation='relu'))#22
    
    model.add(Flatten())
    
    model.add(Dense(100, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1))


    model.compile(loss='mean square error',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

if __name__== "__main__":
    getmodel().save("model/mynew")
