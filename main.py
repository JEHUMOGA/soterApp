from tkinter import *

# Configuracion de la pantalla de tkinter "Tamaño de la pantaal y titulo"
raiz = Tk()

alturaPantalla = raiz.winfo_screenheight()
anchuraPantalla = raiz.winfo_screenwidth()

altura = alturaPantalla *0.80
ancho = anchuraPantalla * 0.80

x = (anchuraPantalla/2) -(ancho/2)
y = (alturaPantalla/2) - (altura/2)

raiz.title("face recognition")
raiz.geometry('%dx%d+%d+%d' % (ancho, altura,x,y))
raiz.resizable(0,0)

#Paneles
#Primer panel
panel_1 = PanedWindow(bd=4,relief="raised", bg="red")
panel_1.pack(fill = BOTH, expand=1)

left_label=Label(panel_1, text="Left Panel")
panel_1.add(left_label)

#Segundo panel
panel_2 = PanedWindow(panel_1,orient=VERTICAL,bd=4,relief="raised", bg="red")
panel_1.add(panel_2)

top = Label(panel_2, text="Top panel")
panel_2.add(top)

botton = Label(panel_2,text="Bottom Panel")
panel_2.add(botton)


left_label = Label(panel_1, text="Left Panel")

raiz.mainloop()