#importar librerias
import cv2
import os

#importar clase seguimiento manos
import SeguimientoManos as sm

# crear carpeta para almacenar los datos
letra = 'A'
nombre = 'Letra_'+letra
direccion = 'C:/Users/DELL/Desktop/CursoYoutubeVisionArtificial/dataSet'
carpeta = direccion + '/' + nombre
cont_cam = 0
cont_data = 0

#Si no esta creada la carpeta
if not os.path.exists(carpeta):
    print("La carpera esta creada: ",carpeta)

    #Creamos la carpeta
    os.makedirs(carpeta)

# Obtener una lista de los archivos en la carpeta
archivos = os.listdir(carpeta)

# Filtrar los archivos que tengan el formato deseado, por ejemplo, "A_0001.jpg"
archivos = [archivo for archivo in archivos if archivo.startswith(f"{letra}_") and archivo.endswith(".jpg")]

# Si hay archivos en la carpeta, encontrar el número más alto
if archivos:
    numeros = [int(archivo.split("_")[1].split(".")[0]) for archivo in archivos]
    cont_data = max(numeros) + 1
else:
    cont_data = 0

#Lectura de la camara
cap = cv2.VideoCapture(0)

#cambiar la resolucion de la camara
cap.set(3, 1280)
cap.set(4, 720)

# Declarar detector
detector = sm.detectormanos(Confdeteccion=0.9)

while True:
    # Lectura de la captura
    ret, frame = cap.read()

    # Extraer informacíon de la mano
    frame = detector.encontrarmanos(frame, dibujar=False)
    
    # Posicion de una sola mano
    lista1, bbox, mano = detector.encontrarposicion(frame, ManoNum=0, dibujar= False, color= [0,255,0])

    # Si hay mano
    if mano == 1:
        #Extraer la informacion del cuadro
        xmin, ymin, xmax, ymax = bbox

        # Asignamos margen
        xmin = xmin - 50
        ymin = ymin - 50
        xmax = xmax + 50
        ymax = ymax + 50
             
        # Dibujamos cuadro
        #cv2.rectangle(frame,(xmin, ymin), (xmax, ymax), [0,255,0],2)

        # Realizar recorte de nuestra mano
        recorte = frame[ymin:ymax, xmin:xmax]

        # Redimensionamiento
        #recorte = cv2.resize(recorte, (640,640), interpolation=cv2.INTER_CUBIC)

        # Almacenar nuestras imágenes
        #cv2.imwrite(carpeta + "/_{}.jpg".format(cont), recorte)
        cv2.imwrite(carpeta + f"/{letra}_{cont_data}.jpg", recorte)
        
        # Aumentamos el contador
        cont_data = cont_data + 1
        cont_cam = cont_cam + 1
        
        cv2.imshow("RECORTE", recorte)
    #Mostrar FPS
    cv2.imshow("Signos de vocales", frame)

    #Leer nuestro teclado
    t= cv2.waitKey(1)
    if t == 27 or cont_cam == 100:
        break 

cap.release()
cv2.destroyAllWindows()