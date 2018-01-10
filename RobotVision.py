# import the necessary packages
from collections import deque
from itertools import islice as slice
import numpy as np
import argparse
import cv2
import time
from scipy.interpolate import *
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib import pyplot as plt
from matplotlib import style
import os


TRANS_ACC = deque(maxlen=10) # Accumulated transforms

class RobotVision():
    def __init__(self):
        style.use('fivethirtyeight')
        self.X_er = 0
        self.Y_er = 0
        self.contour = False
    ## This Code tracks the trajectory based on a polynomial regression

    ## Custom Functions:
    def Get_Traj(self,X,Y, samp, order, Time_vec, pred_len):

        x_tr = np.empty((0,1))
        y_tr = np.empty((0,1))
        
        X1 = X[-samp:]
        Y1= Y[-samp:] 
        t = np.arange(0,len(X1))
        X_Tr_dat, Y_Tr_dat, Time_vec_fin = self.Traj_decompose(X1, Y1, t)

        X_Seasonal = X_Tr_dat.seasonal.reshape( (len(X_Tr_dat.seasonal), 1) )
        Y_Seasonal = Y_Tr_dat.seasonal.reshape( (len(Y_Tr_dat.seasonal), 1) )
        X_Trend = X1 - X_Seasonal
        Y_Trend = Y1 - Y_Seasonal
        
        X_resid = X_Tr_dat.resid
        Y_resid = Y_Tr_dat.resid
        
        t1 =np.arange(0, pred_len)
        t1 = np.array(t1) +t[-1]
        
        f1 = np.polyfit(t, X_Trend, order)
        f2 = np.polyfit(t, Y_Trend, order)
        f_x = np.polyval(f1, t1)
        f_y = np.polyval(f2, t1)
        
        X_Sc = np.array(X_Seasonal[-pred_len:])
        Y_Sc = np.array(Y_Seasonal[-pred_len:])


        x_tr = np.array(f_x).reshape( (len(f_x), 1) ) 
        y_tr = np.array(f_y).reshape( (len(f_y), 1) )
        
        Sum_X = X_Sc + x_tr
        Sum_Y = Y_Sc + y_tr
        
        # print('\n Size of x_sum: ' + repr(np.shape(Sum_X)))   
        # print('\n Size of y_sum: ' + repr(np.shape(Sum_Y)))  

           # print(np.array([time.time(), X_las, Y_las]))
        return Sum_X, Sum_Y

    def Traj_mismatch(self,X_Current, Y_Current, P_X, P_Y):
        x_pred = P_X[0]
        y_pred = P_Y[0]
        x_sq_err = pow(x_pred-X_Current,2)
        y_sq_err = pow(y_pred-Y_Current,2) 
        P_X = P_X[-(len(P_X) - 1) :]
        P_Y = P_Y[-(len(P_Y) - 1) :]
        err = pow(x_sq_err+y_sq_err, 0.5)
        if err <= 20:
            return True, err, P_X, P_Y
        else:
            return False, err, P_X, P_Y
        

    def Traj_decompose(self,X_Current, Y_Current, Time_set):
        Tr_l = min(len(X_Current),len(Y_Current))
        X_Current = X_Current[-Tr_l:]
        Y_Current = Y_Current[-Tr_l:]
        Time_set_fin = Time_set[-Tr_l:]
        X_Set = seasonal_decompose(X_Current, model='additive', freq = 2)
        Y_Set = seasonal_decompose(Y_Current, model='additive', freq = 2)
        return X_Set, Y_Set, Time_set_fin

    def main(self):
        x_sh = 0
        y_sh = 0
        X_old = 0
        Y_old = 0
        X_older = 0
        Y_older = 0
        ct = 0
        c = 0
        t = 0
        dt = 0
        net_err = 0
        X_traj = np.empty((0,1))
        Y_traj = np.empty((0,1))
        X_traj_sh = np.empty((0,1))
        Y_traj_sh = np.empty((0,1))
        Time_Vec = np.empty((0,1))
        tim = np.empty((0,1))
        X_pr = np.array([])
        Y_pr = np.array([])

        X_Trend = np.empty((0,1))
        Y_Trend = np.empty((0,1))                
        x_sh = 0
        y_sh = 0
        x_netsh = 0
        y_netsh = 0

        X_las = None
        Y_las = None
        file = open('Image Threshold','r')
        line = file.read()
        try:
            thresh = np.int_(line.strip('[]').rstrip('\n').rstrip(' ').rstrip(']').split(','))
        except:
            thresh = np.int_(line.strip('[]').rstrip('\n').rstrip(' ').rstrip(']').split())
        threshLower = np.array(thresh[0:3])
        threshUpper = np.array(thresh[3:6])
        Traj_hist = deque()
        try:
            pts = deque(maxlen=args["buffer"])
        except:
            pts = deque()
        traj = deque(maxlen=30)


        # Plotting Parameters
        thickness = 3

        ## Regression Parameters
        Tr_len= 6  #35
        Pred_len = 6 #15
        poly_ord = 1

        # Should you track ?
        tr_fl = False
        min_Tr_len = Tr_len/3

        ## Decomposition
        X_T = pd.Series()
        Y_T = pd.Series()
        # pts = deque(maxlen=args["buffer"])

        camera = cv2.VideoCapture(0)

        if camera.isOpened() == False:               # check if VideoCapture object was associated to webcam successfully
            print "error: camera not accessed successfully\n\n"      # if not, print error message to std out
            os.system("pause")                                          # pause until user presses a key so user can see error message
        # end if
        cv2.namedWindow('Frame')
        cv2.namedWindow('Mask')
        # cv2.startWindowThread()
        stabilizer=VidStabilizer()
        # _,prev = camera.read()
        first = 1
        while ((cv2.getWindowProperty('Frame', 0) != -1) or (cv2.getWindowProperty('Mask', 0) != -1)) and cv2.waitKey(1) & 0xFF != ord("q") and camera.isOpened():
            # grab the current frame
            grabbed, frame = camera.read()
            
            # resize the frame, blur it, and convert it to the HSV
            # color space
            #frame = imutils.resize(frame, width=600)
            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            height, width, channels = frame.shape
            im_x = width/2
            im_y = height/2
            ma_ln=5
            cv2.line(frame, (im_x-ma_ln,im_y-ma_ln), (im_x+ma_ln,im_y+ma_ln), (0,0,255),4)
            cv2.line(frame, (im_x+ma_ln,im_y-ma_ln), (im_x-ma_ln,im_y+ma_ln), (0,0,255),4)
         
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, threshLower, threshUpper)
            mask = cv2.erode(mask, None, iterations=3)
            mask = cv2.dilate(mask, None, iterations=5)
            if first==1:
                prev = mask
                first = 2

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            ct = 0
            cen2 = None
            
            if len(cnts) is 0:
                pts.clear()
                traj.clear()
                ct = 0
                cen2 = None
                X_las = None
                Y_las = None
                X_old = 0
                Y_old = 0
                X_older = 0
                Y_older = 0
                X_off = 0
                Y_off = 0
                net_err = 0
                X_traj = np.empty((0,1))
                Y_traj = np.empty((0,1))
                X_traj_sh = np.empty((0,1))
                Y_traj_sh = np.empty((0,1))
                Time_Vec = np.empty((0,1))
                X_Trend = np.empty((0,1))
                Y_Trend = np.empty((0,1))
                Traj_hist = None
                X_pr = np.empty((0,1))
                Y_pr = np.empty((0,1))
                x_sh = 0
                y_sh = 0
                x_netsh = 0
                y_netsh = 0

                tim = None
                tr_fl = False
                # Did not detect any contours, then set error to 0
                self.contour = False
                self.X_er = 0
                self.Y_er = 0
            # only proceed if at least one contour was found
            t0 = time.time()
            if len(cnts) > 0:
                self.contour = True
                c = max(cnts, key=cv2.contourArea)
                #for c in cnts:
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                X_des = x+(w/2)
                Y_des = y+(h/2)
                cen = (X_des, Y_des)
                m_r=3
                cv2.circle(frame,cen, m_r, (0,255,0), -1)
                #pts.appendleft(cen)
                    # loop over the set of tracked points
                pts.appendleft(cen)
                #for i in xrange(1, len(pts)):
                 #       if pts[i] is  not None:
                  #          cv2.line(frame, pts[i - 1], pts[i], (0,255, 0), thickness)
                            #cv2.line(frame, pts[i - 1], pts[i], (0,255, 0), thickness)

                if X_des is not None and Y_des is not None:
                    t = time.time() - t0
                    Time_Vec = np.vstack([Time_Vec, t])
                    if len(X_traj) > 2:
                    	X_old = X_traj[len(X_traj)-1]
                    	Y_old = Y_traj[len(Y_traj)-1]
                    	X_older = X_traj[len(X_traj)-2]
                    	Y_older = Y_traj[len(Y_traj)-2]

                    x_sh= X_old-X_older
                    y_sh= Y_old-Y_older
                    x_netsh= x_netsh + x_sh
                    y_netsh= y_netsh + y_sh
                    X_off= X_des + x_netsh
                    Y_off= Y_des + y_netsh

                    X_traj = np.vstack( [X_traj, X_des] )
                    Y_traj = np.vstack( [Y_traj, Y_des] )
                    X_traj_sh = np.vstack( [X_traj_sh, X_off] )
                    Y_traj_sh = np.vstack( [Y_traj_sh, Y_off] )

                    
                if len(X_traj) > Tr_len:					
                    #print(' Acquiring trajectory...')
                    if tr_fl is False:
                        #X_pr, Y_pr = self.Get_Traj(X_traj_sh,Y_traj_sh, Tr_len, poly_ord, Time_Vec, Pred_len)
                        X_pr, Y_pr = self.Get_Traj(X_traj,Y_traj, Tr_len, poly_ord, Time_Vec, Pred_len)
                        #print(' Trajectory acquired.')

                        for c in np.arange(1,len(X_traj_sh)):
                            #cv2.line(frame, (int(X_traj_sh[c - 1]), int(Y_traj_sh[c - 1])),  (int(X_traj_sh[c]), int(Y_traj_sh[c])), (0,255, 0), thickness)
                            cv2.line(frame, (int(X_traj[c - 1]), int(Y_traj[c - 1])),  (int(X_traj[c]), int(Y_traj[c])), (0,255, 0), thickness)


                        #cv2.line(frame, (int(X_traj_sh[len(X_traj_sh)-1]), int(Y_traj_sh[len(Y_traj_sh)-1])), (int(X_pr[0]), int(Y_pr[0])), (0,0, 255), thickness)
                        cv2.line(frame, (int(X_traj[len(X_traj)-1]), int(Y_traj[len(Y_traj)-1])), (int(X_pr[0]), int(Y_pr[0])), (0,0, 255), thickness)

                        for c in np.arange(1,len(X_pr)):
                            cv2.line(frame, (int(X_pr[c - 1]), int(Y_pr[c - 1])), (int(X_pr[c]), int(Y_pr[c])), (0,0, 255), thickness)
                            tr_fl = False    
                self.X_er = X_des - im_x
                self.Y_er = Y_des - im_y
                # print(self.X_er,self.Y_er)
                # Stabilize the video
                #frame = stabilizer.stabilize(prev,mask,frame)
                #prev = mask               
                dt = time.time()-t
            try:
                # show the frame to our screen
                if(cv2.getWindowProperty('Frame', 0) != -1) or (cv2.getWindowProperty('Mask', 0) !=-1):
                    cv2.imshow("Frame", frame)
                    cv2.imshow("Mask", mask)
                else:
                    print('No frames')
                    break
            except:
                break


        print("Releasing camera")         
        # cleanup the camera and close any open windows
        camera.release()
        plt.close()
        self.__del__()

    def __del__(self):
        cv2.destroyAllWindows()
        print('Exiting RobotVision!')

    def getError(self):
        er = [self.X_er,self.Y_er,self.contour]
        # print er
        return np.array(er)

class VidStabilizer():
    def stabilize(self,old, frame,color_frame):
            # params for ShiTomasi corner detection
            feature_params = dict( maxCorners = 100,qualityLevel = 0.3,minDistance = 7,blockSize = 7 )
            # Parameters for lucas kanade optical flow
            lk_params = dict( winSize  = (15,15),
                              maxLevel = 2,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
            hsv = np.zeros_like(frame)
            # prev = cv2.cvtColor(old, cv2.COLOR_BGR2GRAY)
            prev = old
            p0 = cv2.goodFeaturesToTrack(prev, mask = None, **feature_params)
            # next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            next = frame
            # d = np.ones(3)*4e-3
            # n = np.ones(3)*0.25
            try:
                # calculate optical flow
                p1,st,_ = cv2.calcOpticalFlowPyrLK(prev, next, p0, None, **lk_params)
                # Select good points
                good_new = p1[st==1]
                good_old = p0[st==1]
                # print 'Good points old :-\n',good_old
                # print 'Good points new :-\n',good_new
                # Get transformation matrix from the optical flow
                transform = cv2.findHomography(good_old,good_new)
                TRANS_ACC.append(transform[0])
                len_trans = len(TRANS_ACC)
                # print len_trans,'\n\n'
                # print deque(slice(TRANS_ACC,1, len_trans))
                # value1 = deque(slice(TRANS_ACC,1, len_trans))-deque(slice(TRANS_ACC,0, len_trans-1))
                TRANS_DIFF = deque(slice(TRANS_ACC,1, len_trans))-deque(slice(TRANS_ACC,0, len_trans-1)) if len_trans>2 else np.zeros(shape=(3,3)) if len_trans==1 else TRANS_ACC[1]-TRANS_ACC[0]
                transform_mean = sum(TRANS_ACC)/len_trans
                #print transform_mean
            except:
                transform = np.eye(3) #np.zeros(shape=(3,3))
                #print('<4 Good points found')
            
            try:
                result=cv2.warpPerspective(color_frame,transform_mean, (frame.shape[1],frame.shape[0]))
            except Exception as e:
                #print('wrap failed due to <4 Good points found. No worries')
                result = color_frame
            return result

if __name__=='__main__':
    vision = RobotVision()
    vision.main()
