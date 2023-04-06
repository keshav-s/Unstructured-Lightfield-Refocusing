import numpy as np
import scipy
import cv2
import skimage
from skimage import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import interpolate
from scipy import signal
import lib

def readVideo(path):
    cap = cv2.VideoCapture(path)
    if (cap.isOpened() is False):
        print("Error opening video file")
        exit()

    vid = np.zeros((308,1080,1920,3))
    ret,f = cap.read()
    i=0
    while(cap.isOpened()):
        ret,f = cap.read()
        if ret == True:
            vid[i] = f/255
            i+=1
        else:
            break

    print(i)
    cap.release()
    return vid

def linearize(I):
    # Convert sRGB to linear RGB by removing gamma correction
    return np.where(I <= 0.0404482, I/12.92, np.power((I+.055)/1.055, 2.4))

def refocus(vid, mid, wini, winj, twidth, swwidth):
    template = mid[wini:wini+twidth, winj:winj+twidth]
    g = linearize(template)
    g = lib.lRGB2XYZ(g[:,:,::-1])[:,:,1]
    gbar = np.mean(g)
    fs,h,w,d = vid.shape
    im = np.zeros((h,w,d))

    tempMidI = int(wini+twidth/2)
    tempMidJ = int(winj+twidth/2)

    print(tempMidI, tempMidJ)

    box = np.ones((twidth,twidth))
    for t in range(fs):
        print("frame %d/%d" % (t+1, fs))
        window = np.copy(vid[t])
        window = window[tempMidI-swwidth:tempMidI+swwidth, \
                        tempMidJ-swwidth:tempMidJ+swwidth, :]
        I = linearize(window)
        I = lib.lRGB2XYZ(I[:,:,::-1])[:,:,1]
        Ibar = signal.convolve2d(I, box, mode='same') / (twidth**2)
        I2bar = signal.convolve2d(I**2, box, mode='same')

        num = signal.correlate2d(I-Ibar, g-gbar, mode='same')
        # To calculate the denominator, I used section 3.1 of the following paper:
        # https://isas.iar.kit.edu/pdf/SPIE01_BriechleHanebeck_CrossCorr.pdf
        denom = (I2bar - Ibar)
        denom = denom * np.sum((g-gbar)**2)
        denom = np.maximum(denom, 0) # to prevent imaginary component in denom
        denom[denom == 0] = 1e-12    # to prevent divide by 0
        denom = np.sqrt(denom)

        corr = num/denom
        y, x = np.unravel_index(np.argmax(corr), corr.shape)  # find the match
        # print(y,x)

        frame = vid[t]
        fshift = np.zeros(frame.shape)
        I = np.arange(frame.shape[0])
        J = np.arange(frame.shape[1])
        for dd in range(3):
            fI = interpolate.interp2d(J,I, frame[:,:,dd])
            qI = I + (y-100)
            qJ = J + (x-100)
            fshift[:,:,dd] = fI(qJ,qI)

        im = im+fshift

    return im/(vid.shape[0])

def main(rubiks = False, tea = False, mouse = False):
    vid = readVideo('../data/IMG_1857.mov')
    vid=vid[5::5,:,:,:]
    print(vid.shape)

    mid = vid[31]
    twidth = 60
    if rubiks:
        wini,winj = 400, 1010
    elif tea:
        wini, winj = 180, 1280
    elif mouse:
        wini, winj = 415, 390

    im = refocus(vid, mid, wini, winj, twidth, 100)
    im = im[:,:,::-1]
    if rubiks:
        io.imsave('../data/rubiks.png', im)
    elif tea:
        io.imsave('../data/tea.png', im)
    elif mouse:
        io.imsave('../data/mouse.png', im)


if __name__ == '__main__':
    main(tea=True)
