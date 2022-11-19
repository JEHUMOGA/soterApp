import cv2
import json
import os
import face_recognition as fr
import os
from datetime import datetime
import time
import numpy as np
import pyautogui
import webbrowser
from time import sleep
import threading


"""def envioAlerta():
    webbrowser.open('https://web.whatsapp.com/send?phone=+5216671641334')
    pyautogui.typewrite(mensaje)
    pyautogui.press('enter')
"""


class Empleados:
    def __init__(self, nombre, empleado):

        self.nombre = nombre
        self.empleado = empleado


# Accedemos a la carpeta
path = 'image'
images = []
clases = []
lista = os.listdir(path)
horaVisto = 0
horaDesc = 0
anterior = None
guardarDesc = True

# Variables
comp1 = 100


def leeJson():
    with open('roots/empleados.json') as file:
        data = json.load(file)
        d = {}
        for dato in data['empleados']:
            d[dato['clave']] = Empleados(dato['nombre'], dato['empleado'])
    return d


# Temporal
datos = leeJson()


for lis in lista:
    # Leemos las imagenes de los rostros
    imgdb = cv2.imread(f'{path}/{lis}')
    # Alacenamos imagen
    images.append(imgdb)
    # Almacenamos nombre
    clases.append(os.path.splitext(lis)[0])


# Funcion para codificar los rostros
def registro(clave, nombre):
    # Se abre e archivo en modo elctura y escritura
    with open('roots/Registro.csv', 'r+') as h:
        # Leemos la informacion
        data = h.readline()
        # Creamos lista de nombres
        listanombres = []

        # Iteramos con cada linea del doc
        for line in data:
            # Buscamos la entrada y la diferenciamos con,
            entrada = line.split(',')
            # Almacenamos los nombres
            listanombres.append(entrada[0])

        # Verificamos si ya hemos almacenado el nombre
        if nombre not in listanombres:
            # Extraemos informacion acctual
            info = datetime.now()
            # Extraemos fecha
            fecha = info.strftime('%Y:%m:%d')
            # Extraemos hora
            hora = info.strftime('%H:%M:%S')

            # Guardamos la informacion
            h.writelines(f'\n{clave},{nombre},{fecha},{hora}')


def codrostros(images):
    listacod = []

    # Iteracion
    for img in images:
        # correcion de color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Codificacion de imagen
        cod = fr.face_encodings(img)[0]
        # Almacenacion
        listacod.append(cod)
    return listacod


# Se llama a la funcion para la codificacion de rostros
rostroscod = codrostros(images)

# Realizamos la videocaptura
cap = cv2.VideoCapture(0)

# Empezamos
while True:
    # Leemos los fotogramas
    ret, frame = cap.read()

    # Reducimos las imagenes por segundo
    frame2 = cv2.resize(frame, (0, 0), None, 0.25, 0.25)

    # conversion de color
    rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    # Buscamos los rostros
    faces = fr.face_locations(rgb)
    facescod = fr.face_encodings(rgb, faces)

    # Iteramos
    for facecod, faceloc in zip(facescod, faces):

        # Comparamos rostro de DB con rostro en tiempo real
        comparacion = fr.compare_faces(rostroscod, facecod)

        # Calculamos la similitud
        simi = fr.face_distance(rostroscod, facecod)
        # print(simi)
        # Buscamos el valor mas bajo
        min = np.argmin(simi)

        yi, xf, yf, xi = faceloc
        # Escalamos
        yi, xf, yf, xi = yi*4, xf*4, yf*4, xi*4

        if comparacion[min]:
            nombre = clases[min].upper()
            # Extraemos coordenadas

            indice = comparacion.index(True)

            # Comparamos
            if comp1 != indice:
                r, g, b = 125, 220, 0
                comp1 = indice

            if comp1 == indice:
                # Dibujamos
                if datos[nombre].empleado:
                    cv2.rectangle(frame, (xi, yi), (xf, yf), (r, g, b), 3)
                    cv2.rectangle(frame, (xi, yf-35), (xf, yf),
                                  (r, g, b), cv2.FILLED)
                    cv2.putText(frame, datos[nombre].nombre, (xi+6, yf-6),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    if time.time() - horaVisto > 60 or nombre != anterior:
                        registro(nombre, datos[nombre].nombre)
                        horaVisto = time.time()
                        anterior = nombre
                    else:
                        continue
                else:
                    cv2.rectangle(frame, (xi, yi), (xf, yf), (50, 50, 255), 3)
                    cv2.rectangle(frame, (xi, yf-35), (xf, yf),
                                  (50, 50, 255), cv2.FILLED)
                    cv2.putText(frame, "DESCONOCIDO", (xi+6, yf-6),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    if time.time() - horaVisto > 60 or nombre != anterior:
                        registro(nombre, 'DESCONOCIDO')
                        horaVisto = time.time()
                        anterior = nombre

        else:
            # aca escribir
            if guardarDesc:
                if time.time() - horaDesc > 30:
                    nombre = f"desconocidos/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                    cv2.imwrite(nombre, frame)
                    registro(nombre, "DESCONOCIDO")
                    horaDesc = time.time()
            cv2.rectangle(frame, (xi, yi), (xf, yf), (50, 50, 255), 3)
            cv2.rectangle(frame, (xi, yf-35), (xf, yf),
                          (50, 50, 255), cv2.FILLED)
            cv2.putText(frame, "DESCONOCIDO", (xi+6, yf-6),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == 27 & 0xFF:
        break
cap.release()
cv2.destroyAllWindows()
