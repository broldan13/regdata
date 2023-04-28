from tkinter import*
from tkinter import messagebox
import sqlite3

#---------------------------FUNCIONES------------------------
def conexionBD ():
    miConexion=sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()
    try:
        miCursor.execute('''
            CREATE TABLE DATOS_USUARIOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CURP TEXT UNIQUE,
            NOMBRE_USUARIO VARCHAR(50),
            APELLIDO VARCHAR(20),
            PASSWORD VARCHAR(50),
            DIRECCION VARCHAR(50),
            COMENTARIOS VARCHAR (100))
            ''')
        #Mensaje de base de datos creada
        messagebox.showinfo("Base Datos","Se creo la Base de Datos.")
    except:
        messagebox.showwarning("Error","Base de datos ya existente.")


def salirBD():
    decision=messagebox.askquestion("Salir","¿Desea salir de la aplicación?")
    if decision== "yes":
        raiz.destroy()


def limpiarCampos ():
    miID.set("")
    curp.set("")
    miNombre.set("")
    miApellido.set("")
    miClave.set("")
    miDirec.set("")
    #Limpiar ci}uadro de texto comentario
    cuadro_comentario.delete(1.0,END)#Borrar desde el primer caracter hasta el final


def crear():
    miConexion=sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()
    
    if curp.get()=="" and miNombre.get()=="" and miApellido and miClave.get()=="" and miDirec.get()=="":
        messagebox.showerror("Error","No puede haber campos vacios.")
    else:
        datosRegistro=curp.get(),miNombre.get(),miApellido.get(),miClave.get(),miDirec.get(),cuadro_comentario.get("1.0",END)
        try:
            miCursor.execute("INSERT INTO DATOS_USUARIOS VALUES(NULL,?,?,?,?,?,?)",(datosRegistro))
            miConexion.commit()
            messagebox.showinfo("Base de Datos", "Campos registrados")
        except sqlite3.IntegrityError:
            messagebox.showerror("IntegrityError","Clave CURP ya existente en la base de datos.")


def buscar():
    miConexion=sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()

    miCursor.execute("SELECT * FROM DATOS_USUARIOS WHERE ID="+ miID.get())
    existe=miCursor.fetchall()
    miConexion.close()

    if existe:
        for usuario in existe:
            miID.set(usuario[0])
            curp.set(usuario[1])
            miNombre.set(usuario[2])
            miApellido.set(usuario[3])
            miClave.set(usuario[4])
            miDirec.set(usuario[5])
            cuadro_comentario.insert(1.0,usuario[6])

    else:
        limpiarCampos()
        messagebox.showerror("Base de Datos","ID no encontrado en la base de datos.")
    

def actualizar ():
    miConexion=sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()

    miCursor.execute("UPDATE DATOS_USUARIOS SET CURP='" + curp.get() + 
                    "', NOMBRE_USUARIO='" + miNombre.get() +
                    "', APELLIDO='" + miApellido.get() +
                    "', PASSWORD='" + miClave.get() +
                    "', DIRECCION='" + miDirec.get() +
                    "', COMENTARIOS='" + cuadro_comentario.get("1.0",END) +
                    "' WHERE ID=" + miID.get())
    
    miConexion.commit()
    messagebox.showinfo("Base de datos","Los datos fueron actualizados correctamente.")

def borrarRegistros ():
    miConexion=sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()

    miCursor.execute("DELETE FROM DATOS_USUARIOS WHERE ID="+ miID.get())
    miConexion.commit()
    messagebox.showinfo("Base Datos","Registros borrados con exito.")





#----------------------DISEÑO GRAFICO-----------------------
raiz=Tk()
raiz.title("Formulario")
raiz.config(bg="#454546")
 
formTitulo=Label(raiz,text="RegData")
formTitulo.config(font=("Impact",30),fg="#018031",bg="#454546")
formTitulo.pack()


#Barra menu
barraOpciones=Menu(raiz)
raiz.config(menu=barraOpciones,width=300,height=400)

#Nombre de opciones de menu
BaseDatos=Menu(barraOpciones,tearoff=0)
BaseDatos.add_command(label="Conectar",command=conexionBD)
BaseDatos.add_separator()
BaseDatos.add_command(label="Salir",command=salirBD)

Limpiar=Menu(barraOpciones,tearoff=0)
Limpiar.add_command(label="Limpiar campos",command=limpiarCampos)

Crud=Menu(barraOpciones,tearoff=0)
Crud.add_command(label="Crear",command=crear)
Crud.add_command(label="Buscar",command=buscar)
Crud.add_command(label="Actualizar",command=actualizar)
Crud.add_command(label="Eliminar",command=borrarRegistros)

ayuda=Menu(barraOpciones,tearoff=0)
ayuda.add_command(label="Licencia")
ayuda.add_command(label="Acerca de..")
ayuda.add_separator()
ayuda.add_command(label="Ayuda y comentarios")

#Asignar numbre a las opciones en la barra menu
barraOpciones.add_cascade(label="BBDD",menu=BaseDatos)
barraOpciones.add_cascade(label="Limpiar",menu=Limpiar)
barraOpciones.add_cascade(label="Opciones",menu=Crud)
barraOpciones.add_cascade(label="Ayuda",menu=ayuda)
#FIN BARRA MENU

#LABEL Y CUADRO DE TEXTO

primFrame=Frame(raiz)
primFrame.config(width=300,height=400,bg="#dcdcdc")
primFrame.pack()


miID=StringVar()
curp=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miClave=StringVar()
miDirec=StringVar()


id_text=Label(primFrame,text="Buscar ID:")
id_text.config(font=("Calibri",14),bg="#dcdcdc")
id_text.grid(row=0,column=0,sticky="w",padx=8,pady=8)

id_cudrotext=Entry(primFrame,textvariable=miID)
id_cudrotext.grid(row=0,column=1,padx=5,pady=5)

curp_text=Label(primFrame,text="CURP")
curp_text.config(font=("Calibri",12),bg="#dcdcdc")
curp_text.grid(row=1,column=2,sticky="w",padx=8,pady=8)

curp_cuadro=Entry(primFrame,textvariable=curp)
curp_cuadro.grid(row=1,column=3,padx=5,pady=5)

nombre=Label(primFrame,text="Nombre")
nombre.config(font=("Calibri",12),bg="#dcdcdc")
nombre.grid(row=2,column=2,sticky="w",padx=8,pady=8)

nombre_cuadro=Entry(primFrame,textvariable=miNombre)
nombre_cuadro.grid(row=2,column=3,padx=5,pady=5)



apellido=Label(primFrame,text="Apellido")
apellido.config(font=("Calibri",12),bg="#dcdcdc")
apellido.grid(row=3,column=2,sticky="w",padx=8,pady=8)

apellido_cuadro=Entry(primFrame,textvariable=miApellido)
apellido_cuadro.grid(row=3,column=3,padx=5,pady=5)



clave_text=Label(primFrame,text="Contraseña")
clave_text.config(font=("Calibri",12),bg="#dcdcdc")
clave_text.grid(row=4,column=2,sticky="w",padx=8,pady=8)


clave_cuadro=Entry(primFrame,textvariable=miClave)
clave_cuadro.grid(row=4,column=3,padx=5,pady=5)
clave_cuadro.config(show="•")



direc_text=Label(primFrame,text="Dirección")
direc_text.config(font=("Calibri",12),bg="#dcdcdc")
direc_text.grid(row=5,column=2,sticky="w",padx=8,pady=8)

direc_cuadro=Entry(primFrame,textvariable=miDirec)
direc_cuadro.grid(row=5,column=3,padx=5,pady=5)



text_comentario=Label(primFrame,text="Comentario")
text_comentario.config(font=("Calibri",12),bg="#dcdcdc")
text_comentario.grid(row=6,column=2,sticky="w",padx=8,pady=8)

cuadro_comentario=Text(primFrame,width=15,height=5)
cuadro_comentario.grid(row=6,column=3,padx=15,pady=15)
scrollVert=Scrollbar(primFrame,command=cuadro_comentario.yview)
scrollVert.grid(row=6,column=4,sticky="nsew")
cuadro_comentario.config(yscrollcommand=scrollVert.set)

btnLimpiar=Button(primFrame,text="Clean",width=5,height=2,command=limpiarCampos)
btnLimpiar.grid(row=6,column=0,padx=10,pady=10)


#_-_--------_-------_-----------------------------BOTONES ---------------------------------------------------------------
frameBotones=Frame(raiz)
frameBotones.config(bg="#454546")
frameBotones.pack()

btnCrear=Button(frameBotones,text="Registrar",width=7,command=crear)
btnCrear.grid(row=7,column=0,padx=10,pady=10)

btnBuscar=Button(frameBotones,text="Buscar",width=7,command=buscar)
btnBuscar.grid(row=7,column=1,padx=10,pady=10)

btnActualizar=Button(frameBotones,text="Actualizar",width=7,command=actualizar)
btnActualizar.grid(row=7,column=2,padx=10,pady=10)

btnEliminar=Button(frameBotones,text="Eliminar",width=7,command=borrarRegistros)
btnEliminar.grid(row=7,column=3,padx=10,pady=10)






raiz.mainloop()