import cv2
import numpy as np

# Открываем видео
cap = cv2.VideoCapture("/Users/vladislav/Временное/enina2.mp4")

# Читаем первый кадр
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

while True:
    ret, frame2 = cap.read()
    if not ret:
        break
    
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Вычисляем оптический поток
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    # Вычисляем величину и направление движения
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    # Фильтрация кадров с интенсивным движением
    if np.mean(mag) > 2:  # Условие движения
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        print(f"Много движения на {timestamp:.2f} секунде")
    
    prvs = next

cap.release()