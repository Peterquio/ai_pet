import cv2
import requests
import numpy as np
from ultralytics import YOLO
import serial
import time

# === CONFIGURAÇÕES ===
CAMERA_URL = 'http://10.233.191.56/capture'# substitua pelo IP da sua ESP32-CAM
MODEL_PATH = 'models/espeon_umbreon.pt'
#SERIAL_PORT = 'COM5'  # porta do seu Arduino
THRESHOLD = 0.5
cooldown = 30  # segundos
last_sent = 0

# === INICIALIZAÇÕES ===
model = YOLO(MODEL_PATH)
#arduino = serial.Serial(SERIAL_PORT, 9600)
time.sleep(2)  # tempo para o Arduino resetar

class_name_dict = {0: 'Espeon',
                   1: 'Umbreon'}
color_dict = {0: (0, 255, 0)}

print("Sistema iniciado. Aguardando detecção...")

while True:
    try:
        # === CAPTURA DA CÂMERA ESP32 ===
        response = requests.get(CAMERA_URL, timeout=5)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, -1)

        results = model(frame)[0]

        for box in results.boxes:
            conf = box.conf[0].item()
            if conf > THRESHOLD:
                cls = int(box.cls[0])
                label = class_name_dict.get(cls, f'Classe {cls}')
                color = color_dict.get(cls, (255, 255, 255))
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Desenhar box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Label com fundo
                label_text = f"{label} {conf:.2f}"
                (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                text_x = x1
                text_y = max(y1 - 5, text_h + 5)
                cv2.rectangle(frame, (text_x, text_y - text_h - 4), (text_x + text_w + 4, text_y), color, -1)
                cv2.putText(frame, label_text, (text_x + 2, text_y - 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                # ENVIA SINAL PARA ARDUINO SE FOR A NUVEM
                if cls == 0 and (time.time() - last_sent) > cooldown:
                    print("🐱 Espeon detectada! Enviando sinal para o Arduino...")
#arduino.write(b'nuvem\n')
                    last_sent = time.time()  # atualiza o último envio

        # === EXIBE JANELA ===
        cv2.imshow("Detecção - ESP32-CAM", frame)

        # Tecla ESC para sair
        if cv2.waitKey(1) & 0xFF == 27:
            break

    except Exception as e:
        print(f"Erro ao capturar/processar imagem: {e}")

# Finalização
arduino.close()
cv2.destroyAllWindows()