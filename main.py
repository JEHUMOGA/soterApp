try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import config as conf
import csv
import os
import face_recognition as fr
import time
import empleados
from empleados import *
import threading
from tkinter import ttk
from correos import EnvioCorreo

path = 'image'
images = []
clases = []
lista = os.listdir(path)
horaVisto = 0
horaDesc = 0
anterior = None

# Variables
comp1 = 100

empleados.ejecucionInicial()


def leeDatos():
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
    return clas, listacod


# Temporal
clases, rostroscod = leeDatos()

def registrar(clave: str, nombre: str, imagen: str):
    info = datetime.now()
    fecha = info.strftime('%Y-%m-%d')
    hora = info.strftime('%H:%M:%S')
    registro = Registro(clave=clave, nombre=nombre, fecha=fecha, hora=hora, imagen=imagen)
    insertarRegistro(registro=registro)


def guardarHilo(fecha: str):
    t1 = threading.Thread(target=guardarCSV,args=(fecha,))
    t1.start()


def guardarCSV(fecha):
    limpiarCSV(f"roots/{fecha}.csv")
    file = open(f"roots/{fecha}.csv", 'a+', newline='')
    registros = empleados.consultaRegistrosFecha(fecha)
    fecha = "2022-11-20"
    wr = csv.writer(file, delimiter=',')
    wr.writerows(registros)
    file.close()

def limpiarCSV(nombre):
    file = open(nombre, 'w')
    file.close()


def analisis(frame):
    global comp1, horaVisto, horaDesc, anterior
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
                emp = empleados.consultaClave(nombre)
                if emp.empleado == 0:
                    cv2.rectangle(frame, (xi, yi), (xf, yf), (125, 220, 0), 3)
                    cv2.rectangle(frame, (xi, yf-35), (xf, yf),(125, 220, 0), cv2.FILLED)
                    cv2.putText(frame, emp.nombre, (xi+6, yf-6),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    if time.time() - horaVisto > 60 or nombre != anterior:
                        registrar(clave=emp.clave, nombre=emp.nombre, imagen=emp.imagen)
                        anterior = nombre
                        horaVisto = time.time()
                else:
                    cv2.rectangle(frame, (xi, yi), (xf, yf), (50, 50, 255), 3)
                    cv2.rectangle(frame, (xi, yf-35), (xf, yf),(50, 50, 255), cv2.FILLED)
                    cv2.putText(frame, "CRIMINAL", (xi+6, yf-6),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    if time.time() - horaVisto > 60 or nombre != anterior:
                        registrar(clave=emp.clave, nombre=emp.nombre, imagen=emp.imagen)
                        horaVisto = time.time()
                        anterior = nombre
                        if conf.envio_alerta_crimi():
                            info = datetime.now()
                            fecha = info.strftime('%Y-%m-%d')
                            hora = info.strftime('%H:%M:%S')
                            hilo = threading.Thread(target=EnvioCorreo.enviar_correo, args=(emp.clave, fecha, hora, emp.imagen, True))
                            hilo.start()
        else:
            if conf.guardar_desc():
                clave = datetime.now().strftime('%Y%m%d%H%M%S')
                nombre = "DESCONOCIDO"
                imagen = f"desconocidos/{clave}.jpg"
                if time.time() - horaDesc > 30:
                    cv2.imwrite(imagen, frame)
                    registrar(clave=clave, nombre=nombre, imagen=imagen)
                    if conf.envio_correo_autorizado():
                        info = datetime.now()
                        fecha = info.strftime('%Y-%m-%d')
                        hora = info.strftime('%H:%M:%S')
                        hilo = threading.Thread(target=EnvioCorreo.enviar_correo, args=(clave, fecha, hora, imagen, False))
                        hilo.start()
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
    top_frame, text="SoterApp - Aplicación de Vigilancia", font=("Arial", 25))
lblTitulo.place(x=400, y=5)

left_frame = Frame(
    raiz, bg="white",
    width=conf.width_prct(60),
    height=conf.height_prct(90)
)
left_frame.place(x=0, y=conf.height_prct(10))

notebook = ttk.Notebook(left_frame, width=int(conf.width_prct(40)), height=int(conf.height_prct(85)))
label1 = ttk.Label(notebook, width=int(conf.width_prct(25)))
label2 = ttk.Label(notebook, width=int(conf.width_prct(25)))
label3 = ttk.Label(notebook, width=int(conf.width_prct(25)))
label4 = ttk.Label(notebook, width=int(conf.width_prct(25)))

notebook.add(label1, text="Agregar", padding=10)
notebook.add(label2, text="Consultar", padding=10)
notebook.add(label3, text="Eliminar", padding=10)
notebook.add(label4, text="Utilidades", padding=10)
notebook.place(x=0, y=0)


"""
btnCSV = Button(left_frame, text="Generar CSV", command=guardarHilo("2022-11-20")) # ACA FALTA PONER EL ATRIBUTO
btnCSV.grid(column=0, row=0, columnspan=2, padx=15)
"""
center_frame = Frame(
    raiz, bg="red",
    width=conf.width_prct(60),
    height=conf.height_prct(90)
)
center_frame.place(x=conf.width_prct(40), y=conf.height_prct(10))

lblVideo = Label(center_frame, bg="black")
lblVideo.place(x=0, y=0)

t1 = threading.Thread(target=grabacion)
t1.start()

raiz.mainloop()
