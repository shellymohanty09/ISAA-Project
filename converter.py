root = ""
import sys
import os
from math import log
import numpy as np
import scipy as sp
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import cv2
import time

model = keras.models.load_model('mal_detect.h5')
## This function allows us to process our hexadecimal files into png images##
def convertAndSave(array,name):
    print('Processing '+name)
    start_time = time.time()
    print (array.shape)
    if array.shape[1]!=16: #If not hexadecimal
        assert(False)
    b=int((array.shape[0]*16)**(0.5))
    b=2**(int(log(b)/log(2))+1)
    a=int(array.shape[0]*16/b)
    array=array[:a*b//16,:]
    array=np.reshape(array,(a,b,1)).astype('uint8')
    # print(array)
    img = cv2.resize(array, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = np.reshape(img, (128,128,1))
    predsidx=np.argmax(model.predict(np.array([img]))[0])
    print("--- Time taken: %s seconds ---" % (time.time() - start_time))
    preds=["Adialer.C","Agent.FYI","Allaple.A","Allaple.L","Alueron.gen!J","Autorun.K","C2LOP.P","C2LOP.gen!g","Dialplatform.B","Dontovo.A","Fakerean","Instantaccess","Lolyda.AA1","Lolyda.AA2","Lolyda.AA3","Lolyda.AT","Malex.gen!J","Obfuscator.AD","Rbot!gen","Skintrim.N","Swizzor.gen!E","Swizzor.gen!I","VB.AT","Wintrim.BX","Yuner.A"]
    # im = Image.fromarray(np.uint8(array))
    # im.save(root+'\\'+name+'.png', "PNG")
    return "[CRITICAL]<Warning> "+preds[predsidx]+" was detected"

def findMalware(name):
    # #Get the list of files
    # files=os.listdir(root)
    # print('files : ',files)
    # #We will process files one by one.
    # for counter, name in enumerate(files):
            #We only process .bytes files from our folder.
    if '.bytes' != name[-6:]:
        return
    f=open(name)
    array=[]
    for line in f:
        xx=line.split()
        if len(xx)!=17:
            continue
        array.append([int(i,16) if i!='??' else 0 for i in xx[1:] ])
    im = convertAndSave(np.array(array),name)
    print(im)
    del array
    f.close()

# #Get the list of files
# files=os.listdir(root)
# print('files : ',files)
# #We will process files one by one.
# for counter, name in enumerate(files):
#         #We only process .bytes files from our folder.
#     if '.bytes' != name[-6:]:
#         continue
#     f=open(root+'/'+name)
#     array=[]
#     for line in f:
#         xx=line.split()
#         if len(xx)!=17:
#             continue
#         array.append([int(i,16) if i!='??' else 0 for i in xx[1:] ])
#     im = convertAndSave(np.array(array),name)
#     print(im)
#     del array
#     f.close()