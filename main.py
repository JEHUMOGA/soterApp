from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import config_interfaz as conf
import os
import json
import face_recognition as fr
import time

class Empleados:
    def __init__(self, nombre, empleado):

        self.nombre = nombre
        self.empleado = empleado


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


def leeDatos():
    with open('roots/empleados.json') as file:
        data = json.load(file)
        d = {}
        for dato in data['empleados']:
            d[dato['clave']] = Empleados(dato['nombre'], dato['empleado'])
    clas = []
    listacod = []
    for lis in lista:
        # Leemos las imagenes de los rostros
        imgdb = cv2.imread(f'{path}/{lis}')
        # Alacenamos imagen
        imgdb = cv2.cvtColor(imgdb, cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(imgdb)[0]
        listacod.append(cod)
        # Almacenamos nombre
        clas.append(os.path.splitext(lis)[0])
    return d, clas, listacod


# Temporal
datos, clases, rostroscod = leeDatos()


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


def analisis(frame):
    global comp1
    global horaVisto
    global horaDesc
    global anterior
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame2 = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    faces = fr.face_locations(frame2)
    facescod = fr.face_encodings(frame2, faces)

    for facecod, faceloc in zip(facescod, faces):
        comparacion = fr.compare_faces(rostroscod, facecod)

        simi = fr.face_distance(rostroscod, facecod)
        min = np.argmin(simi)

        yi, xf, yf, xi = faceloc
        yi, xf, yf, xi = yi*4, xf*4, yf*4, xi*4

        if comparacion[min]:
            nombre = clases[min].upper()
            indice = comparacion.index(True)
            if comp1 != indice:
                comp1 = indice

            if comp1 == indice:
                if datos[nombre].empleado:
                    cv2.rectangle(frame, (xi, yi), (xf, yf), (125, 220, 0), 3)
                    cv2.rectangle(frame, (xi, yf-35), (xf, yf),(125, 220, 0), cv2.FILLED)
                    cv2.putText(frame, datos[nombre].nombre, (xi+6, yf-6),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    if time.time() - horaVisto > 60 or nombre != anterior:
                        registro(nombre, datos[nombre].nombre)
                        horaVisto = time.time()
                        anterior = nombre
                else:
                    cv2.rectangle(frame, (xi, yi), (xf, yf), (50, 50, 255), 3)
                    cv2.rectangle(frame, (xi, yf-35), (xf, yf),(50, 50, 255), cv2.FILLED)
                    cv2.putText(frame, "CRIMINAL", (xi+6, yf-6),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    if time.time() - horaVisto > 60 or nombre != anterior:
                        registro(nombre, 'CRIMINAL')
                        horaVisto = time.time()
                        anterior = nombre
        else:
            if guardarDesc:
                if time.time() - horaDesc > 30:
                    nombre = f"desconocidos/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                    cv2.imwrite(nombre, frame)
                    registro(nombre, "DESCONOCIDO")
                    horaDesc = time.time()
            cv2.rectangle(frame, (xi, yi), (xf, yf), (50, 50, 255), 3)
            cv2.rectangle(frame, (xi, yf-35), (xf, yf),(50, 50, 255), cv2.FILLED)
            cv2.putText(frame, "DESCONOCIDO", (xi+6, yf-6),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return frame


def grabacion():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()


def visualizar():
    global cap
    ret, frame = cap.read()
    if ret:
        frame = analisis(frame)
        frame = imutils.resize(frame, height=int(conf.height_prct(90)))
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)


raiz = Tk()
# Configuración de la ventana
raiz.configure(bg="white")
raiz.geometry(f'{conf.WIDTH}x{conf.HEIGHT}')
raiz.title('SoterApp - Aplicación de Vigilancia')
raiz.resizable(False, False)

# Configuración de los páneles
top_frame = Frame(
    raiz, bg="white",
    width=conf.WIDTH,
    height=conf.height_prct(10)
)
top_frame.place(x=0, y=0)

lblTitulo = Label(
    top_frame, text="SoterApp - Aplicación de Vigilancia", font="bold")
lblTitulo.place(x=550, y=5)

left_frame = Frame(
    raiz, bg="blue",
    width=conf.width_prct(60),
    height=conf.height_prct(90)
)
left_frame.place(x=0, y=conf.height_prct(10))

center_frame = Frame(
    raiz, bg="red",
    width=conf.width_prct(60),
    height=conf.height_prct(90)
)
center_frame.place(x=conf.width_prct(40), y=conf.height_prct(10))

lblVideo = Label(center_frame, bg="black")
lblVideo.place(x=0, y=0)

grabacion()

raiz.mainloop()