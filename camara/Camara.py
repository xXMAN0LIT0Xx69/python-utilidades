import cv2
import numpy as np
import os
ruta = os.path.join(os.path.dirname(__file__), "monodef.png")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
replacement = cv2.imread(ruta, cv2.IMREAD_UNCHANGED)

camara = cv2.VideoCapture(0)

while True:
    ret, frame = camara.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        scale = 2.0
        replacement_resized = cv2.resize(replacement, (int(w*scale), int(h*scale)))

        bgr = replacement_resized[:, :, :3]
        alpha = replacement_resized[:, :, 3] / 255.0
        alpha = cv2.merge([alpha, alpha, alpha])  

        new_h, new_w = replacement_resized.shape[:2]

        x_offset = x - (new_w - w) // 2
        y_offset = y - (new_h - h) // 2

        if x_offset < 0: x_offset = 0
        if y_offset < 0: y_offset = 0
        if x_offset+new_w > frame.shape[1]: new_w = frame.shape[1] - x_offset
        if y_offset+new_h > frame.shape[0]: new_h = frame.shape[0] - y_offset

        roi = frame[y_offset:y_offset+new_h, x_offset:x_offset+new_w]

        blended = (1 - alpha[:new_h, :new_w]) * roi + alpha[:new_h, :new_w] * bgr[:new_h, :new_w]
        frame[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = blended.astype(np.uint8)

    cv2.imshow("Camara", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()
