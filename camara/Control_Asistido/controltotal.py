import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import math

def distancia_entre_dedos(punto1, punto2):
    """Calcula distancia euclidiana entre dos landmarks"""
    return math.sqrt((punto1.x - punto2.x)**2 + (punto1.y - punto2.y)**2)

camara = cv2.VideoCapture(0)

camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camara.set(cv2.CAP_PROP_FPS, 30)

mp_manos = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils
manos = mp_manos.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

ancho_pantalla,alto_pantalla = pyautogui.size()
historial_x = []
historial_y = []
TAMANO_HISTORIAL = 5
clic_activo = False
doble_clic_activo = False
arrastrando = False
umbral_clic = 0.05

while True:
    exito,frame = camara.read()
    if not exito:
        break
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resultados = manos.process(frame_rgb)

    if resultados.multi_hand_landmarks:
        mano = resultados.multi_hand_landmarks[0] 
        pulgar = mano.landmark[4]    
        indice = mano.landmark[8]    
        medio = mano.landmark[12]    
        corazon = mano.landmark[9]   
        distancia_pulgar_indice = distancia_entre_dedos(pulgar, indice)
        distancia_indice_medio = distancia_entre_dedos(indice, medio)
        distancia_base_dedos = distancia_entre_dedos(indice, corazon)
        mano_abierta = distancia_base_dedos > 0.1
        if distancia_pulgar_indice < umbral_clic and not clic_activo:
            pyautogui.click()
            clic_activo = True
        elif distancia_pulgar_indice >= umbral_clic:
            clic_activo = False
        mano = resultados.multi_hand_landmarks[0]
        mp_dibujo.draw_landmarks(
            frame,mano,mp_manos.HAND_CONNECTIONS
        )
        alto, ancho, _ = frame.shape
        dedo_indice = mano.landmark[8]

        x_camara = int(dedo_indice.x * ancho)
        y_camara = int(dedo_indice.y * alto)

        cv2.circle(frame,(x_camara,y_camara),10,(255,0,0),-1)
        x_pantalla = ancho_pantalla - int(dedo_indice.x * ancho_pantalla)
        historial_x.append(x_pantalla)
        y_relativa = dedo_indice.y
        factor_vertical = 1.2
        y_mapeada = y_relativa * factor_vertical
        y_mapeada = max(0, min(y_mapeada, 1))
        y_pantalla = int(y_mapeada * alto_pantalla)
        historial_y.append(y_pantalla)

        if len(historial_x) > TAMANO_HISTORIAL:
            historial_x.pop(0)
            historial_y.pop(0)
        if len(historial_x) > 0:
            x_promedio = sum(historial_x) // len(historial_x)
            y_promedio = sum(historial_y) // len(historial_y)
        else:
            x_promedio = x_pantalla
            y_promedio = y_pantalla

        try:
            pyautogui.moveTo(x_promedio,y_promedio,duration=0)

        except Exception as e:
            print("Error al mover el mouse:", e)

    cv2.imshow("Jarvis",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()