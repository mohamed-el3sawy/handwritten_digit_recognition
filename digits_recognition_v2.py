import numpy as np
from skimage import io
from keras.datasets import mnist
from sklearn import svm
import tkinter as tk
import mss
from tkinter import *
from PIL import Image

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "black", cursor="cross")
        self.takeScreen_btn = tk.Button(self, text = "takeScreen", command = self.takeScreen)   
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        # Grid structure
        self.canvas.grid(row=6, column=0, pady=2, sticky=W, )
        self.takeScreen_btn.grid(row=8, column=0, pady=2, padx=2)
        self.button_clear.grid(row=9, column=0, pady=2)
        
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.canvas.bind("<B1-Motion>", self.draw_lines)
    def clear_all(self):
        self.canvas.delete("all")
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.create_line(self.x, self.y, event.x, event.y,
                               width=13, fill='white',
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
    #this function will take screen shot of the written image
    def takeScreen(self):
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": 27, "left": 2, "width": 300, "height": 300}
            output = "C:\\Users\\Mohamed\\Desktop\\project\\checkImage.png".format(**monitor)
            # Grab the data
            sct_img = sct.grab(monitor)
            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            print(output)


def fuction_to_capture_and_store_the_check_image():
    app = App()
    mainloop()


def dataset(n):    
    (X_train, y_train), (X_test_null, y_test_null) = mnist.load_data()
    data = X_train[:n].reshape(n,-1)
    target = y_train[:n]
    return data, target


def testImage():
    logo = Image.open("C:\\Users\\Mohamed\\Desktop\\project\\checkImage.png")
    logo.save("C:\\Users\\Mohamed\\Desktop\\project\\checkImage.ico",format='ICO', sizes=[(28, 28)])
    
    image = io.imread('C:\\Users\\Mohamed\\Desktop\\project\\checkImage.ico')
    final_img = np.zeros((image.shape[0],image.shape[1]))
    
    for i in range(0,final_img.shape[0]):
        for j in range(0,final_img.shape[1]):
            final_img[i][j] = ((int(image[i,j,0]) + int(image[i,j,1]) + int(image[i,j,2]))/3)
    
    return np.array([final_img.reshape(-1)])    


if __name__ == '__main__':    

    data, target = dataset(10000)
    
    fuction_to_capture_and_store_the_check_image()
    
    test_image = testImage()
    
    model=svm.SVC(kernel="linear", random_state=6)
    model.fit(data, target)
    y_predict = model.predict(test_image)
    
    print('y_predict: ',y_predict)