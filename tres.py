import sys
import numpy as np
from PIL import Image

TL=[[6,-1],[1,-1]]
IMG_PATH="C:\\Users\\Juan\\Desktop\\prueba.png"


def sign(p1, p2, p3):
  return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


def PointInAABB(pt, c1, c2):
  return c2[0] <= pt[0] <= c1[0] and \
         c2[1] <= pt[1] <= c1[1]

def PointInTriangle(pt, v1, v2, v3):
  b1 = sign(pt, v1, v2) < 0
  b2 = sign(pt, v2, v3) < 0
  b3 = sign(pt, v3, v1) < 0

  return ((b1 == b2) and (b2 == b3)) and \
         PointInAABB(pt, list(map(max, v1, v2, v3)), list(map(min, v1, v2, v3)))
#dice si un punto esta dentro de un cuadrilatero
def punto_adentro(point,a,b,c,d,):
    return PointInTriangle(point,a,b,c) and PointInTriangle(point,c,d,a)

#multiplica la TL de una coordenada cartesiana
def multiplicar(matriz,puntos):
    resultado=[0,0]
    for fila in range(len(matriz)):
        for valor in range(len(matriz[fila])):
            resultado[fila]+=(matriz[fila][valor]*puntos[valor])
    return (resultado)
#aplica la tecnica del vecino mas cercano
def vecinos(imagen,buffer,oldwidth,oldheight,informacion,width,height,k):
    print(width,height)
    a = (buffer[0,0,0],buffer[0,0,1])
    b = (buffer[0,oldheight-1,0],buffer[0,oldheight-1,1])
    c = (buffer[oldwidth-1,oldheight-1,0],buffer[oldwidth-1,oldheight-1,1])
    d = (buffer[oldwidth-1,0,0],buffer[oldwidth-1,0,1])
    for fila in range(width):
        print(fila)
        for columna in range(height):
            if(not informacion[fila][columna]):
                punto=(fila,columna)
                if(not punto_adentro(punto,a,b,c,d)):
                    encontradas=0
                    valores=0
                    separacion=1
                    while(encontradas<k):
                        for i in range(-1*separacion,separacion):
                            for j in range(-1*separacion,separacion):
                                if(fila+i>=0 and fila+i<width and columna+j>=0 and columna+j<height):
                                    if(informacion[fila+i][columna+j]):
                                       valores+=imagen[fila+i,columna+j]
                                       encontradas+=1
                        separacion+=1
                    
                    valores=valores//encontradas
                    imagen[fila,columna]=valores
    return imagen
#x0,y0 son los puntos que se tomaran como el punto 0,0
#interpolar es un booleano que indica si se aplicara interpolacion a la imagen transformada
#tl es la matriz de orden 2
#img_path es el path de la imagen
def transformar(tl,img_path,x0,y0,interpolar):
    img = Image.open(img_path).convert('L')
    img.load()
    imagen=np.asarray(img,dtype="int32")
    width,height=imagen.shape[0],imagen.shape[1]
    buffer=np.zeros((width,height,2),dtype="int32")
    xmax=ymax=-1
    xmin=ymin=sys.maxsize
    for fila in range(width):
        for columna in range(height):
            transformacion=multiplicar(tl,(fila-x0,columna-y0))
            x=int(transformacion[0])
            y=int(transformacion[1])
            if(x>xmax):
                xmax=x
            if(x<xmin):
                xmin=x
            if(y>ymax):
                ymax=y
            if(y<ymin):
                ymin=y
            buffer[fila,columna]=[x,y]
    nuevowidth=xmax-xmin
    nuevoheight=ymax-ymin
    informacion_interpolacion=[[False for j in range(nuevoheight)] for i in range(nuevowidth)]
    transformada=np.zeros((nuevowidth,nuevoheight),dtype="int32")
    for fila in range(width):
        for columna in range(height):
            #lo normaliza para que quede en un valor>=0
            nx=buffer[fila,columna,0]-xmin-1
            ny=buffer[fila,columna,1]-ymin-1
            color=imagen[fila,columna]
            transformada[nx,ny]=color
            informacion_interpolacion[nx][ny]=True
    if(interpolar):
        transformada=vecinos(transformada,buffer,width,height,informacion_interpolacion,nuevowidth,nuevoheight,2)
    im=Image.fromarray(transformada)
    im.show()
    im=im.convert("L")
    im.save("res.png")
transformar(TL,IMG_PATH,0,0,False)

        
    










