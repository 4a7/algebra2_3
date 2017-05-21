import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tres
#import os

colorTema   = {"fondo":"#ADD8E6","entradas":"#CAE6EF"};
tamanoImg   = 400,400;
imgDefault  = "vacia.png"
fontDefault = ("Eras Light ITC",10)

def intro(ventana):
	#global marco
	marco        = tk.Frame(ventana, width=1000, height=1000, bg=colorTema["fondo"]);
	label_nombre = tk.Label(marco,text="Transformaciones Lineales Aplicadas a\nImágenes Digitales",fg="red", 
		bg=colorTema["fondo"],font=(fontDefault[0],30));
	boton_main   = tk.Button(marco,text="Iniciar",command=lambda: abrirMain(ventana,marco),height=2,width=12,font=("Arial",20));
	label_nombre.place(x=150,y=100);
	boton_main.place(x=400, y=300);
	marco.pack();
	return



def abrirMain(ventana,marco):
	marco.destroy();
	main(ventana);
	return



def abrirImagen(marco):
	path_imagen = filedialog.askopenfilename(title="Seleccionar imagen");
	print(path_imagen);

	marco.path_imagenStringVar.set(path_imagen);
	marco.path_imagen = path_imagen;

	marco.boton_cargarImagen.configure(state=tk.NORMAL);
	colocarImagen(marco)
	return path_imagen;



def colocarImagen(marco):
	image = Image.open(marco.path_imagen);
	image = image.resize(tamanoImg, Image.ANTIALIAS);
	img = ImageTk.PhotoImage(image);

	marco.panelImagenOriginal.configure(image=img);
	marco.panelImagenOriginal.image = img;
	return



def validar(accion, indice, valorHipotetico, valorPrevio, valorInsertado, tipoValidacion, tipoTrigger, nombreWidget):
	if accion != "0":
		if valorInsertado in "-0123456789":
			return True
		return False;
	return True;



def aplicarTransformacion(marco):
	matricita = [[marco.texto_matrizEntradas[0].get(),marco.texto_matrizEntradas[1].get()],
				 [marco.texto_matrizEntradas[2].get(),marco.texto_matrizEntradas[3].get()]];

	if matricita[0][0] == "":
		matricita[0][0] = 0;
	else:
		int(matricita[0][0]);

	if matricita[0][1] == "":
		matricita[0][1] = 0;
	else:
		int(matricita[0][1]);

	if matricita[1][0] == "":
		matricita[1][0] = 0;
	else:
		int(matricita[1][0]);

	if matricita[1][1] == "":
		matricita[1][1] = 0;
	else:
		int(matricita[1][1]);

	print(matricita);

	tres.transformar(matricita,marco.path_imagen,0,0,False)

	image = Image.open("res.png");
	image = image.resize(tamanoImg, Image.ANTIALIAS);
	img = ImageTk.PhotoImage(image);

	marco.panelImagenTransformada.configure(image=img);
	marco.panelImagenTransformada.image = img;


	"""
	FALTA UN TRY CATCH PARA CUANDO LA MATRIZ DE TR ES NULA
	"""


	return



def main(ventana):
	ventana.geometry("1000x700+100+0");
	marco = tk.Frame(ventana, width=1000, height=1000, bg=colorTema["fondo"]);
	marco.pack();
	###############################################################################
	#Coloca imagenes vacias
	label_nombreImagenOriginal = tk.Label(marco, text = "Imagen Original", bg=colorTema["fondo"],font=fontDefault);
	label_nombreImagenOriginal.place(x=140,y=0);

	
	img = Image.open("vacia.png");
	img = img.resize(tamanoImg, Image.ANTIALIAS);
	img = ImageTk.PhotoImage(img);
	panelImagenOriginal = tk.Label(marco, image=img, bg=colorTema["fondo"]);
	panelImagenOriginal.image = img;
	panelImagenOriginal.place(x=50,y=20);
	marco.panelImagenOriginal = panelImagenOriginal;

	label_nombreImagenTransformada = tk.Label(marco, text = "Imagen Transformada", bg=colorTema["fondo"],font=fontDefault);
	label_nombreImagenTransformada.place(x=720,y=0);
	img = Image.open("vacia.png");
	img = img.resize(tamanoImg, Image.ANTIALIAS);
	img = ImageTk.PhotoImage(img);
	panelImagenTransformada = tk.Label(marco, image=img, bg=colorTema["fondo"]);
	panelImagenTransformada.image = img;
	panelImagenTransformada.place(x=550,y=20);
	marco.panelImagenTransformada = panelImagenTransformada;

	###############################################################################
	#Colocar separadores
	separador_horizontal1 = tk.Frame(relief=tk.RIDGE, bg="black",width=1000, height=1);
	separador_horizontal2 = tk.Frame(relief=tk.RIDGE, bg="black",width=1000, height=1);
	separador_vertical    = tk.Frame(relief=tk.RIDGE, bg="black",width=1,height=440);
	separador_horizontal1.place(x=0,y=440);
	separador_horizontal2.place(x=0,y=540);
	separador_vertical.place(x=500, y=0);
	###############################################################################
	#Colocar buscar imagen
	label_buscarImagen = tk.Label(marco, text="Buscar Archivo de Imagen:", bg=colorTema["fondo"], font=fontDefault);
	label_buscarImagen.place(x=20,y=460);

	path_imagenStringVar = tk.StringVar();
	entry_buscarImagen = tk.Entry(marco, textvariable=path_imagenStringVar,font=fontDefault,
		state=tk.DISABLED,width=81,bd=5,bg=colorTema["entradas"],selectbackground=colorTema["entradas"]);
	entry_buscarImagen.place(x=20,y=480);
	marco.path_imagenStringVar = path_imagenStringVar;

	boton_buscarImagen = tk.Button(marco,text="Examinar", font=fontDefault, bg=colorTema["fondo"], 
		command=lambda:abrirImagen(marco));
	boton_buscarImagen.place(x=765,y=480);
	boton_cargarImagen = tk.Button(marco,text="Cargar Imagen", font=fontDefault, bg=colorTema["fondo"], 
		command=lambda:colocarImagen(marco), state=tk.DISABLED);
	boton_cargarImagen.place(x=860,y=480);
	marco.boton_cargarImagen = boton_cargarImagen;

	###############################################################################
	#Colocar zona matriz
	label_buscarImagen = tk.Label(marco, text="Insertar Matriz de la Transformación", bg=colorTema["fondo"], font=fontDefault);
	label_buscarImagen.place(x=20,y=560);

	texto_matrizEntradas = [tk.StringVar() for i in range(4)];

	matrizEntradas = [tk.Entry(marco, validate = 'key', width=3, font=fontDefault, justify=tk.CENTER, 
		textvariable=texto_matrizEntradas[i]) for i in range(4)];

	marco.texto_matrizEntradas = texto_matrizEntradas;

	for i in matrizEntradas:
		i['validatecommand'] = (i.register(validar),"%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W");

	matrizEntradas[0].place(x=100,y=580);
	matrizEntradas[1].place(x=135,y=580);
	matrizEntradas[2].place(x=100,y=605);
	matrizEntradas[3].place(x=135,y=605);

	boton_aplicarTransformacion = tk.Button(marco, text="Aplicar Transformación", bg=colorTema["fondo"], font=fontDefault, 
		command=lambda:aplicarTransformacion(marco));
	boton_aplicarTransformacion.place(x=300,y=590);

	###############################################################################
	#Menu
	menubar = tk.Menu(ventana);
	filemenu = tk.Menu(menubar, tearoff=0);
	filemenu.add_command(label="Abrir Imagen", command=lambda:abrirImagen(marco));
	filemenu.add_separator();
	filemenu.add_command(label="Salir", command=ventana.quit);
	menubar.add_cascade(label="File", menu=filemenu);
	ventana.config(menu=menubar);

	return



#if os.name == 'nt':


ventana=tk.Tk();
ventana.geometry("1000x400+100+100");
ventana.title("Transformaciones Lineales Aplicadas a Imágenes Digitales.");
ventana.config(bg=colorTema["fondo"]);
ventana.resizable(width=False, height=False);
#Imagenes Cargadas#
#ropa=load_image("ropa.png") #Para cargar imagen#
####
intro(ventana);
ventana.mainloop();