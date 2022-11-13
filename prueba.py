import cv2
import json
import os
import random
import face_recognition as fr
import numpy as np

#images=["image/Humberto2.jpg", "../img/Mariana.jpg"]
#Accedemos a la carpeta
path='image'
images = []
clases = []
lista = os.listdir(path)
#print(lista)

#Variables
comp1 = 100
#Leemos los rostros del DB
nombre = ''
apellido = ''
imagen = ''


with open('roots/empleados.json') as file:
    data = json.load(file)
    for empleado in data['empleados']:
        nombre = empleado['nombre']
        apellido = empleado['apellido']
        imagen = empleado['image']

        #Leemos las imagenes de los rostros
        imgdb = cv2.imread(f'{path}/{imagen}')
        #Alacenamos imagen
        images.append(imgdb)
        #Almacenamos nombre
        clases.append(nombre)

'''
for lis in lista:
    
    #Leemos las imagenes de los rostros
    imgdb = cv2.imread(f'{path}/{lis}')
    #Alacenamos imagen
    images.append(imgdb)
    #Almacenamos nombre
    clases.append(os.path.splitext(lis)[0])
print(clases)
'''
#Funcion para codificar los rostros
def codrostros(images):
    listacod=[]

    #Iteracion
    for img in images:
        #correcion de color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #Codificacion de imagen
        cod = fr.face_encodings(img)[0]
        #Almacenacion
        listacod.append(cod)
    return listacod

#Se llama a la funcion para la codificacion de rostros
rostroscod = codrostros(images)

#Realizamos la videocaptura
cap = cv2.VideoCapture(0)

#Empezamos
while True:
    #Leemos los fotogramas
    ret,frame = cap.read()

    #Reducimos las imagenes por segundo
    frame2 = cv2.resize(frame, (0,0), None, 0.25,0.25)

    #conversion de color
    rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    #Buscamos los rostros
    faces = fr.face_locations(rgb)
    facescod = fr.face_encodings(rgb,faces)

    # Iteramos
    for facecod, faceloc in zip(facescod,faces):

        #Comparamos rostro de DB con rostro en tiempo real
        comparacion = fr.compare_faces(rostroscod, facecod)
        
        #Calculamos la similitud
        simi = fr.face_distance(rostroscod,facecod)
        #print(simi)
        #Buscamos el valor mas bajo
        min = np.argmin(simi)

        yi, xf, yf, xi = faceloc
        #Escalamos
        yi,xf,yf,xi = yi*4, xf*4, yf*4, xi*4

        if comparacion[min]:
            nombre = clases[min].upper()
            #print(nombre)
            #Extraemos coordenadas
            

            indice = comparacion.index(True)

            #Comparamos
            if comp1 != indice:
                #Para dibujar colores
                #r = random.randrange(0,255,50)
                #g = random.randrange(0,255,50)
                #b = random.randrange(0,255,50)

                r = 125
                g = 220
                b = 0
                print(indice)
                comp1 = indice
                print(indice)

            
            if comp1 == indice:
                #Dibujamos
                cv2.rectangle(frame,(xi,yi), (xf,yf), (r,g,b), 3)
                cv2.rectangle(frame,(xi,yf-35), (xf,yf), (r,g,b), cv2.FILLED)
                cv2.putText(frame,nombre, (xi+6,yf-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            
        else:
            cv2.rectangle(frame,(xi,yi), (xf,yf), (50,50,255), 3)
            cv2.rectangle(frame,(xi,yf-35), (xf,yf), (50,50,255), cv2.FILLED)
            cv2.putText(frame,"desconocido", (xi+6,yf-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            
            
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == 27 & 0xFF:
        break
cap.release()
cv2.destroyAllWindows()