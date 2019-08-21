#%%
import cv2
#%%
cv2.namedWindow("Camera 1")
cv2.namedWindow("Camera 2")
cam_1 = cv2.VideoCapture(0+cv2.CAP_DSHOW)
cam_2 = cv2.VideoCapture(1+cv2.CAP_DSHOW)


if cam_1.isOpened():
    val_1, frame_1 = cam_1.read()
else:
    val_1 = False

if cam_2.isOpened():
    val_2, frame_2 = cam_2.read()
else:
    val_2 = False

#%%
while val_1 and val_2:
    cv2.imshow("Camera 1", frame_1)
    cv2.imshow("Camera 2", frame_2)
    val_1, frame_1 = cam_1.read()
    val_2, frame_2 = cam_2.read()
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyWindow("Camera 1")
cv2.destroyWindow("Camera 2")


#%%
