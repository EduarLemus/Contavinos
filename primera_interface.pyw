from tkinter import *
import sqlite3 as sql
import cv2
import numpy as np
import serial
import time

ardu = serial.Serial(port = 'COM7',baudrate = 115200, timeout =.1)
cam = cv2.VideoCapture(1)
raiz=Tk()

class bdd:
    def  __init__(self):
        global cur
        global conn
        conn = sql.connect("Pedidos.db")
        cur = conn.cursor()
        #cur.execute("""CREATE TABLE pedidos (ID text PRIMARY KEY, Peces1 text, Peces2 text, Contacto text, Total text)""")
        #cur.execute("""CREATE TABLE peces (especie text, cantidad text, precio text)""")

        cur.execute("""SELECT * FROM pedidos""")
        datos=cur.fetchall()
        print (datos)
        for j in range(len(datos)):
            ListaPedidos.append(list(datos[j]))
        print (ListaPedidos)

        cur.execute("""SELECT * FROM peces""")
        datos1=cur.fetchall()
        print (datos1)
        pez1.especie = datos1[0][0]
        pez1.cantidad = '50'
        pez1.precio = datos1[0][2]
        pez2.especie = datos1[1][0]
        pez2.cantidad = '50'
        pez2.precio = datos1[1][2]

    def guardar():
        cur.execute("DELETE FROM peces")
        cur.execute("INSERT INTO peces (especie, cantidad, precio) VALUES(?,?,?)", (pez1.especie, pez1.cantidad, pez1.precio))
        cur.execute("INSERT INTO peces (especie, cantidad, precio) VALUES(?,?,?)", (pez2.especie, pez2.cantidad, pez2.precio))
        conn.commit()

        conn.close()


class ventana:
    def __init__(self):

        
        raiz.title("Contavinos")

        raiz.resizable(False,False)

        raiz.iconbitmap("icono.ico")

        raiz.geometry("1000x600")

        raiz.config(bg="black")


    def Inicio():

        global miFrame , img

        frame, img = cam.read()

        img = img[160:405,0:]
        
        miFrame=Frame()

        miFrame.pack(fill="both", expand="True")

        miFrame.config(bg="light sky blue")

        #miFrame.config(width="850", height="600")

        Imagen1=PhotoImage(file="dibujo.png")
        Label(miFrame, image=Imagen1, bg=miFrame['bg']).place(x=150, y=0)

        botonNuevo=Button(miFrame, text="Nuevo", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[ventana.Nuevo()])
        botonNuevo.grid(row=1, column=0, padx=60, pady=400)

        botonPedidos=Button(miFrame, text="Pedidos", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[ventana.Pedidos()])
        botonPedidos.grid(row=1, column=1, padx=60, pady=400)

        botonInventario=Button(miFrame, text="Inventario", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[ventana.Inventario()])
        botonInventario.grid(row=1, column=2, padx=60, pady=400)

        botonEstadisticas=Button(miFrame, text="Estadisticas", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[ventana.Estadisticas()])
        botonEstadisticas.grid(row=1, column=3, padx=60, pady=400)

        mainloop()

    def Nuevo ():

        global Frame2

        miFrame.pack_forget()

        Frame2=Frame()

        Frame2.pack(fill="both", expand="True")

        Frame2.config(bg="azure4")

        cantidadPeces1.set("0")
        cantidadPeces2.set("0")
        contacto.set("numero de contacto")
        presioR1.set("Total a pagar")
        presioR2.set("Total a pagar")

        Especie1=Label(Frame2,text=pez1.especie,bg=Frame2['bg'],fg="black", font=("Rubik Italic",40))
        Especie1.grid(row=0, column=0, padx=130, pady=50)
        Especie2=Label(Frame2,text=pez2.especie,bg=Frame2['bg'],fg="black", font=("Rubik Italic",40))
        Especie2.grid(row=0, column=2, padx=130, pady=50)

        cantidadEspecie1=Entry(Frame2, textvariable = cantidadPeces1)
        cantidadEspecie1.grid(row=1, column=0, padx=130, pady=40)
        cantidadEspecie1.config(justify="center")
        cantidadEspecie2=Entry(Frame2, textvariable = cantidadPeces2)
        cantidadEspecie2.grid(row=1, column=2, padx=130, pady=40)
        cantidadEspecie2.config(justify="center")

        contactoCliente=Entry(Frame2, textvariable = contacto)
        contactoCliente.grid(row=5, column=1, padx=0, pady=40)
        contactoCliente.config(justify="center")

        presioEspecie1=Label(Frame2,text=("$", str(pez1.precio)),bg=Frame2['bg'],fg="black", font=("Rubik Italic",20))
        presioEspecie1.grid(row=2, column=0, padx=130, pady=20)
        presioEspecie2=Label(Frame2,text=("$", str(pez2.precio)),bg=Frame2['bg'],fg="black", font=("Rubik Italic",20))
        presioEspecie2.grid(row=2, column=2, padx=130, pady=20)

        presioFinal1=Entry(Frame2, textvariable = presioR1)
        presioFinal1.grid(row=3, column=0, padx=130, pady=10)
        presioFinal1.config(justify="center", state='disabled')
        presioFinal2=Entry(Frame2, textvariable = presioR2)
        presioFinal2.grid(row=3, column=2, padx=130, pady=10)
        presioFinal2.config(justify="center", state='disabled')

        disponiblesEspecie1=Label(Frame2,text = str(pez1.cantidad), bg=Frame2['bg'],fg="black", font=("Rubik Italic",20))
        disponiblesEspecie1.grid(row=4, column=0, padx=130, pady=20)
        disponiblesEspecie2=Label(Frame2,text = str(pez2.cantidad),bg=Frame2['bg'],fg="black", font=("Rubik Italic",20))
        disponiblesEspecie2.grid(row=4, column=2, padx=130, pady=20)
        
        Button(Frame2, text="Inicio", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[Frame2.pack_forget(),
                                                                                                    ventana.Inicio()]).grid(row=5, column=0, padx=100, pady=40)
        Button(Frame2, text="Precio", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[presioR1.set(str(int(cantidadPeces1.get())*int(pez1.precio))),
                                                                                                    presioR2.set(str(int(cantidadPeces2.get())*int(pez2.precio)))]).grid(row=3, column=1, padx=10, pady=0)
        Button(Frame2, text="listo", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[presioR1.set(str(int(cantidadPeces1.get())*int(pez1.precio))),
                                                                                                   presioR2.set(str(int(cantidadPeces2.get())*int(pez2.precio))),
                                                                                                   pedido(contacto.get(),
                                                                                                          cantidadPeces1.get(),
                                                                                                          cantidadPeces2.get(),
                                                                                                          str(int(presioR1.get())+int(presioR2.get()))),
                                                                                                   Frame2.pack_forget(),
                                                                                                   ventana.Nuevo()]).grid(row=5, column=2, padx=100, pady=40)

    def Pedidos ():

        global Frame3

        miFrame.pack_forget()

        Frame3=Frame()

        Frame3.pack(fill="both", expand="True")

        Frame3.config(bg="azure4")
        
        idSeleccionado.set("0")

        global srtLista
        srtLista= "   ".join(ele for sub in ListaPedidos for ele in sub)

        pedidoSelec=Entry(Frame3, textvariable = idSeleccionado)
        pedidoSelec.grid(row=0, column=1, padx=80, pady=100)
        pedidoSelec.config(justify="center")

        textoPedidos=Text(Frame3,fg=Frame3['bg'], width=39, height=11)
        textoPedidos.grid(row=2, column=2, padx=0, pady=10)
        textoPedidos.insert('1.0', "ID | #1 | #2 | Contacto | Total \n")
        for j in range(len(ListaPedidos) - 1, -1, -1):
            strPedido = "   ".join(ListaPedidos[j])
            strPedido += "\n"
            textoPedidos.insert('2.0', strPedido)

        scrollVert = Scrollbar(Frame3, command=textoPedidos.yview, bg=Frame3['bg'])
        scrollVert.grid(row=2, column=3, sticky="nsew")

        textoPedidos.config(yscrollcommand=scrollVert.set, state='disabled')

        Button(Frame3, text="Contar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[ventana.pagar(idSeleccionado.get())]).grid(row=1, column=0, padx=120, pady=40)
        Button(Frame3, text="modificar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[ventana.modificar(idSeleccionado.get())]).grid(row=1, column=1, padx=80, pady=40)
        Button(Frame3, text="cancelar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[pedido.cancelar(int(idSeleccionado.get())),
                                                                                                      Frame3.pack_forget(),
                                                                                                      ventana.Pedidos()]).grid(row=1, column=2, padx=0, pady=40)
        Button(Frame3, text="Inicio", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[Frame3.pack_forget(),
                                                                                                    ventana.Inicio()]).grid(row=2, column=0, padx=10, pady=40)

    def Inventario ():

        global Frame4

        miFrame.pack_forget()

        Frame4=Frame()

        Frame4.pack(fill="both", expand="True")

        Frame4.config(bg="azure4")

        Imagen1=PhotoImage(file="dibujo.png")
        imagen=Label(Frame4, image=Imagen1, bg=Frame4['bg'])
        imagen.place(x=230, y=100)

        nombreTexto=Label(Frame4,text="NOMBRE",bg=Frame4['bg'],fg="black", font=("Rubik Italic",20))
        nuevoNombre=Label(Frame4,text="NOMBRE NUEVO",bg=Frame4['bg'],fg="black", font=("Rubik Italic",20))
        precioTexto=Label(Frame4,text="PRECIO",bg=Frame4['bg'],fg="black", font=("Rubik Italic",20))
        nuevoPrecio=Label(Frame4,text="NUEVO PRECIO",bg=Frame4['bg'],fg="black", font=("Rubik Italic",20))
        nombreEscrito=Entry(Frame4, textvariable = nombre)
        nuevoNombreEscrito=Entry(Frame4, textvariable = newNombre)
        precioEscrito=Entry(Frame4, textvariable = precio)
        
        crearPez=Button(Frame4, text="Crear", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[precioEscrito.grid(row=1, column=2, padx=60, pady=40),
                                                                                                           precioTexto.grid(row=0, column=2, padx=60, pady=20),
                                                                                                            nombreTexto.grid(row=0, column=1, padx=60, pady=20),
                                                                                                            nombreEscrito.grid(row=1, column=1, padx=60, pady=40),
                                                                                                            atras.grid(row=3, column=3, padx=60, pady=40),
                                                                                                            quitarPez.grid_forget(),
                                                                                                            modificarPez.grid_forget(),
                                                                                                            contarM.grid_forget(),
                                                                                                            crearPez.grid_forget(),
                                                                                                            listoCrear.grid(row=2, column=0, padx=60, pady=40),
                                                                                                            imagen.place_forget()])
        crearPez.grid(row=2, column=0, padx=60, pady=70)
        quitarPez=Button(Frame4, text="Quitar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[nombreTexto.grid(row=0, column=1, padx=60, pady=20),
                                                                                                              nombreEscrito.grid(row=1, column=1, padx=60, pady=40),
                                                                                                              crearPez.grid_forget(),
                                                                                                              modificarPez.grid_forget(),
                                                                                                              contarM.grid_forget(),
                                                                                                              atras.grid(row=3, column=3, padx=60, pady=40),
                                                                                                                quitarPez.grid_forget(),
                                                                                                                listoQuitar.grid(row=2, column=1, padx=60, pady=40),
                                                                                                                imagen.place_forget()])
        quitarPez.grid(row=2, column=1, padx=60, pady=70)
        modificarPez=Button(Frame4, text="Modificar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[nombreTexto.grid(row=0, column=0, padx=35, pady=20),
                                                                                                                     nombreEscrito.grid(row=1, column=0, padx=50, pady=40),
                                                                                                                     nuevoNombre.grid(row=0, column=1, padx=35, pady=20),
                                                                                                                     nuevoNombreEscrito.grid(row=1, column=1, padx=50, pady=40),
                                                                                                                     nuevoPrecio.grid(row=0, column=2, padx=50, pady=20),
                                                                                                                     precioEscrito.grid(row=1, column=2, padx=50, pady=40),
                                                                                                                     atras.grid(row=3, column=4, padx=60, pady=40),
                                                                                                                     listoModificar.grid(row=2, column=2, padx=60, pady=40),
                                                                                                                     crearPez.grid_forget(),
                                                                                                                     quitarPez.grid_forget(),
                                                                                                                     contarM.grid_forget(),
                                                                                                                     modificarPez.grid_forget(),
                                                                                                                     imagen.place_forget()])
        modificarPez.grid(row=2, column=2, padx=60, pady=70)
        contarM=Button(Frame4, text="Conteo M.", bg="AntiqueWhite3", font=("Rubik Italic",20))
        contarM.grid(row=2, column=3, padx=60, pady=70)
        atras=Button(Frame4, text="atras", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[Frame4.pack_forget(),
                                                                                                        ventana.Inventario()])
        listoCrear=Button(Frame4, text="Listo", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[pez.crearPez(nombre.get(), precio.get()),
                                                                                                              Frame4.pack_forget(),
                                                                                                              ventana.Inventario()])
        listoQuitar=Button(Frame4, text="Listo", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[pez.quitarPez(nombre.get()),
                                                                                                               Frame4.pack_forget(),
                                                                                                               ventana.Inventario()])
        listoModificar=Button(Frame4, text="Listo", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[pez.modificarPez(nombre.get(), newNombre.get(), precio.get()),
                                                                                                                  Frame4.pack_forget(),
                                                                                                                  ventana.Inventario()])
        Button(Frame4, text="Inicio", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[Frame4.pack_forget(),
                                                                                                    ventana.Inicio()]).grid(row=3, column=0, padx=60, pady=160)
        mainloop()


    def Estadisticas():

        global Frame5

        miFrame.pack_forget()

        Frame5=Frame()

        Frame5.pack(fill="both", expand="True")

        Frame5.config(bg="azure4")

        Imagen1=PhotoImage(file="estadisticas.gif")
        Label(Frame5, image=Imagen1).place(x=15, y=0)

        Button(Frame5, text="Inicio", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[Frame5.pack_forget(),
                                                                                                    ventana.Inicio()]).grid(row=0, column=0, padx=180, pady=540)
        Button(Frame5, text="Historial_pagos", bg="AntiqueWhite3", font=("Rubik Italic",20)).grid(row=0, column=1, padx=180, pady=540)
        
        mainloop()


    def modificar (idSelec):

        global Frame7

        Frame3.pack_forget()

        Frame7=Frame()

        Frame7.pack(fill="both", expand="True")

        Frame7.config(bg="azure4")

        cantidadPeces1.set(ListaPedidos[int(idSelec)][1])
        cantidadPeces2.set(ListaPedidos[int(idSelec)][2])
        contacto.set(ListaPedidos[int(idSelec)][3])

        Especie1=Label(Frame7,text=pez1.especie,bg=Frame7['bg'],fg="black", font=("Rubik Italic",40))
        Especie1.grid(row=0, column=0, padx=130, pady=40)
        Especie2=Label(Frame7,text=pez2.especie,bg=Frame7['bg'],fg="black", font=("Rubik Italic",40))
        Especie2.grid(row=0, column=2, padx=130, pady=40)

        cantidadEspecie1=Entry(Frame7, textvariable = cantidadPeces1)
        cantidadEspecie1.grid(row=1, column=0, padx=130, pady=40)
        cantidadEspecie1.config(justify="center")
        cantidadEspecie2=Entry(Frame7, textvariable = cantidadPeces2)
        cantidadEspecie2.grid(row=1, column=2, padx=130, pady=40)
        cantidadEspecie2.config(justify="center")

        contactoCliente=Entry(Frame7, textvariable = contacto)
        contactoCliente.grid(row=5, column=1, padx=0, pady=40)
        contactoCliente.config(justify="center")

        presioR1.set(str(int(cantidadPeces1.get())*int(pez1.precio)))
        presioR2.set(str(int(cantidadPeces2.get())*int(pez2.precio)))

        presioFinal1=Entry(Frame7, textvariable = presioR1)
        presioFinal1.grid(row=3, column=0, padx=130, pady=10)
        presioFinal1.config(justify="center", state='disabled')
        presioFinal2=Entry(Frame7, textvariable = presioR2)
        presioFinal2.grid(row=3, column=2, padx=130, pady=10)
        presioFinal2.config(justify="center", state='disabled')

        presioEspecie1=Label(Frame7,text=("$", str(pez1.precio)),bg=Frame7['bg'],fg="black", font=("Rubik Italic",20))
        presioEspecie1.grid(row=2, column=0, padx=130, pady=20)
        presioEspecie2=Label(Frame7,text=("$", str(pez2.precio)),bg=Frame7['bg'],fg="black", font=("Rubik Italic",20))
        presioEspecie2.grid(row=2, column=2, padx=130, pady=20)

        disponiblesEspecie1=Label(Frame7,text = str(pez1.cantidad),bg=Frame7['bg'],fg="black", font=("Rubik Italic",20))
        disponiblesEspecie1.grid(row=4, column=0, padx=130, pady=20)
        disponiblesEspecie2=Label(Frame7,text = str(pez2.cantidad),bg=Frame7['bg'],fg="black", font=("Rubik Italic",20))
        disponiblesEspecie2.grid(row=4, column=2, padx=130, pady=20)
        
        Button(Frame7, text="Inicio", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[Frame7.pack_forget(),
                                                                                                    ventana.Inicio()]).grid(row=5, column=0, padx=100, pady=40)
        Button(Frame7, text="Precio", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[presioR1.set(str(int(cantidadPeces1.get())*int(pez1.precio))),
                                                                                                    presioR2.set(str(int(cantidadPeces2.get())*int(pez2.precio)))]).grid(row=3, column=1, padx=10, pady=0)
        Button(Frame7, text="modificar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[presioR1.set(str(int(cantidadPeces1.get())*int(pez1.precio))),
                                                                                                       presioR2.set(str(int(cantidadPeces2.get())*int(pez2.precio))),
                                                                                                       pedido.modificarPedido(idSelec,
                                                                                                                              cantidadPeces1.get(),
                                                                                                                              cantidadPeces2.get(),
                                                                                                                              contacto.get(),
                                                                                                                              presioR1.get(),
                                                                                                                              presioR2.get()), 
                                                                                                       Frame7.pack_forget(),
                                                                                                       Pedidos()]).grid(row=5, column=2, padx=100, pady=40)
        
    def pagar(idSelec):

        global Frame6

        Frame3.pack_forget()

        Frame6=Frame()

        Frame6.pack(fill="both", expand="True")

        Frame6.config(bg="azure4")

        Button(Frame6, text="contar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[clasecontador.Contar(idSelec)]).grid(row=0, column=1, padx=250, pady=50)
        
        Button(Frame6, text="Luz", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[clasecontador.luz()]).grid(row=1, column=1, padx=250, pady=50)


        Button(Frame6, text="pagar", bg="AntiqueWhite3", font=("Rubik Italic",20), command=lambda:[clasecontador.closing(),Frame6.pack_forget(),pedido.cancelar(int(idSelec)),ventana.Inicio()]).grid(row=2, column=1, padx=250, pady=50)


class pedido:
    def __init__(self, contacto, cantidadPeces1, cantidadPeces2, totalPagar):

        self.cantidadPeces1=cantidadPeces1
        self.cantidadPeces2=cantidadPeces2
        self.contacto=contacto
        self.totalPagar=totalPagar
        estado=StringVar()
        estado="pendiente"
        elPedido=[]
        global contador
        if ListaPedidos != []:
            if contador != int (ListaPedidos[-1][0]):
                contador = int (ListaPedidos[-1][0])
        else:
            contador=-1
        contador+=1
        elPedido.append(str(contador))
        elPedido.append(cantidadPeces1)
        elPedido.append(cantidadPeces2)
        elPedido.append(contacto)
        elPedido.append(totalPagar)
        ListaPedidos.extend([elPedido])

        strpedido= "   ".join(elPedido)
        
        global peczDisponible1
        global peczDisponible2
        peczDisponible1 = str(int(peczDisponible1) - int(ListaPedidos[contador][1]))
        peczDisponible2 = str(int(peczDisponible2) - int(ListaPedidos[contador][2]))

        cur.execute("INSERT INTO pedidos VALUES(?,?,?,?,?)", (elPedido))
        
        print (ListaPedidos)

        if int(peczDisponible1) < 0 or int(peczDisponible2) < 0:
            pedido.cancelar(contador)
        

    def cancelar(idSelec):
        global peczDisponible1
        global peczDisponible2
        peczDisponible1 = str(int(peczDisponible1) + int(ListaPedidos[int(idSelec)][1]))
        peczDisponible2 = str(int(peczDisponible2) + int(ListaPedidos[int(idSelec)][2]))
        ListaPedidos.pop(int(idSelec))
        
        for x in range(idSelec,len(ListaPedidos)):
            ListaPedidos[x].remove (ListaPedidos[x][0])
            print(ListaPedidos)
    
        for i in range(idSelec,len(ListaPedidos)):
            ListaPedidos[i].insert (0,str(i))
            print(ListaPedidos)

        cur.execute("DELETE FROM pedidos")
        for j in range(len(ListaPedidos)):
            cur.execute("INSERT INTO pedidos VALUES(?,?,?,?,?)", (ListaPedidos[j]))

    def modificarPedido(idSelec, cantidadPeces1, cantidadPeces2, contacto, presioR1, presioR2):
        global peczDisponible1
        global peczDisponible2
        peczDisponible1 = str(int(peczDisponible1) + int(ListaPedidos[int(idSelec)][1]) - int(cantidadPeces1))
        peczDisponible2 = str(int(peczDisponible2) + int(ListaPedidos[int(idSelec)][2]) - int(cantidadPeces2))
        
        pedidoSelc=ListaPedidos[int(idSelec)]
        ListaPedidos.pop(int(idSelec))
        pedidoSelc.pop(1)
        pedidoSelc.pop(1)
        pedidoSelc.pop(1)
        pedidoSelc.pop(1)
    
        pedidoSelc.append(cantidadPeces1)
        pedidoSelc.append(cantidadPeces2)
        pedidoSelc.append(contacto),
        pedidoSelc.append(str(int(presioR1)+int(presioR2))),
        ListaPedidos.insert(int(idSelec), pedidoSelc)
        
        cur.execute("DELETE FROM pedidos")
        for j in range(len(ListaPedidos)):
            cur.execute("INSERT INTO pedidos VALUES(?,?,?,?,?)", (ListaPedidos[j]))

class pez:
    def __init__(self, especie, cantidad, precio):
        self.especie=especie
        self.cantidad=cantidad
        self.precio=precio

    def crearPez(especie,precio):
        if pez1.especie == " ":
            pez1.especie = especie
            pez1.precio = int(precio)
            
        elif pez2.especie == " ":
            pez2.especie = especie
            pez2.precio = int(precio)

    def quitarPez(especie):
        if pez1.especie == especie:
            pez1.especie = " "
            pez1.precio = 0
            pez1.cantidad = 0
            
        elif pez2.especie == especie:
            pez2.especie = " "
            pez2.precio = 0
            pez2.cantidad = 0

    def modificarPez(especie, especiesNueva, precio):
        if pez1.especie == especie:
            pez1.especie=especiesNueva
            pez1.precio = int(precio)
            
        elif pez2.especie == especie:
            pez2.especie = especiesNueva
            pez2.precio = int(precio)
        

class clasecontador:
    

    def luz():
        global eLuz
        if eLuz == False:
            ardu.write(ledOn.encode('utf-8'))
            time.sleep(0.1)
            eLuz = True
        else :
            ardu.write(ledOff.encode('utf-8'))
            time.sleep(0.1)
            eLuz = False
    def Contar(idSelec):
        global img,entradaA,entradaC, salidaA,salidaC,frame6
        ardu.write(entradaA.encode('utf-8'))
        time.sleep(3)
        ardu.write(entradaC.encode('utf-8'))
        time.sleep(0.5)
        frame, img = cam.read()
        img = img[160:405,0:]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lRed = np.array([0,70,0])
        uRed = np.array([40,255,255])
        mask1 = cv2.inRange(hsv, lRed, uRed)
        lRed = np.array([170,70,0])
        uRed = np.array([180,255,255])
        mask2 = cv2.inRange(hsv, lRed, uRed)
        mask = mask1 + mask2
        rImage = cv2.bitwise_and(img.copy(),img.copy(),mask = mask)
        og = cv2.cvtColor(rImage, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(og,(5,5),0)
        ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        kernel1 = np.ones((4,4),np.uint8)
        kernel = np.ones((2,2),np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel1)
        dilation = cv2.dilate(closing,kernel,iterations = 2)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hierarchy = hierarchy[0]
        max_area = cv2.contourArea(contours[0])
        total = 0 # total contour size
        for con in contours:
            area = cv2.contourArea(con) # get contour area
            total += area
            if area > max_area:
                max_area = area
        diff = 0.5
        min_area = int(max_area * diff) 
        average = int(total / (len(contours)))
        #areas bigger than half of the largest are counted
        conto = tuple(x for x in contours if cv2.contourArea(x)> min_area)
        
        objects = str(len(conto))
        text = 'obj:'+str(objects)
        cv2.putText(dilation,text,(10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (240,0,0),1)
        cv2.imshow('img',img)
        cv2.imshow("red",rImage)       
        ardu.write(salidaA.encode('utf-8'))
        time.sleep(3)
        ardu.write(salidaC.encode('utf-8'))
        time.sleep(0.5)
        print(objects)
        if len(conto) >= int(ListaPedidos[int(idSelec)][1]):
            message =Label(Frame6,text = 'conteo exitoso',bg = Frame6["bg"],fg = 'black',font=("Rubik Italic",20))
            message.grid(row=2, column=0, padx=50, pady=50)
            
                
    def closing():
        
        cv2.destroyAllWindows()
        
        
eLuz = False      
contando = False
entradaA = '1'
entradaC = '2'
salidaA = '3'
salidaC ='4'
ledOn = '5'
ledOff = '6'   
pez1=StringVar()
pez2=StringVar()
precio1=StringVar()
precio2=StringVar()
cantidadPeces1=StringVar()
cantidadPeces2=StringVar()
contacto=StringVar()
idSeleccionado=StringVar()
srtLista=StringVar()
listaPedidos=StringVar()
contador=-1
presioR1=StringVar()
presioR2=StringVar()
ListaPedidos=[]
nombre=StringVar()
newNombre=StringVar()
precio=StringVar()
pez1 = pez(" ",0,0);
pez2 = pez(" ",0,0);
peczDisponible1= StringVar()
peczDisponible2= StringVar()
peczDisponible1 = '50'
peczDisponible2 = '50'
bdd()
ventana.Inicio()

raiz.mainloop()
raiz.wm_protocol("WM_DELETE_WINDOW", bdd.guardar()) 
