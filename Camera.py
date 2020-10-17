import cv2
import pynput
import numpy as np
import _thread
from time import sleep

#função para pintar as regiões dos sensores na imagem capturadas
def Pintar(Imagem, x, y):
    for i in range(y[0], y[1]):
        for j in range(x[0], x[1]):
            Imagem[j][i]= (0,0,255)

#função que executa os comandos para o dinossauro
def acao(time, tecla):
    teclado.press(tecla)
    sleep(time)
    teclado.release(tecla)

#imagem totalmente branca para fazer a comparação dos sensores
Sensor = np.ones([1000,1000], dtype=np.uint8)*255

#inicialização do objeto que simula o teclado
teclado = pynput.keyboard.Controller()

#variavel com o endereço da camera usada
index = 0

#loop que busca a camera alvo caso ela não seja a webcam do notebook
while(1):
    index += 1
    captura = cv2.VideoCapture(index)
    
    if captura.isOpened():
        break

#loop que seria a função main do código
while(1):

    #captura dos frames da camera
    _, real = captura.read()
    
    #Posição sensores - o primeiro fica a 80 pixel do topo da tela e o segundo fica no centro da tela
    PSensor1 = [[80,90],[int(real.shape[1]/2)-20, int(real.shape[1]/2)+20]]
    PSensor2 = [[int(real.shape[0]/2)-5,int(real.shape[0]/2)+5],[int(real.shape[1]/2)-20,int(real.shape[1]/2)+20]]
    
    #converção dos frames da camera para escala de cinza
    frame = cv2.cvtColor(real,cv2.COLOR_BGR2GRAY)

    #pintura das regiões dos sensores
    Pintar(real, PSensor1[0],PSensor1[1])
    Pintar(real, PSensor2[0],PSensor2[1])

    #binarização da imagem, a ideia é facilitar o processamento
    ret,frame = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
    
    #Exibição do video e da imagem binaria
    cv2.imshow("Video", real)
    cv2.imshow("Binario", frame)

    #captura das condições para executar os comandos
    if(not(np.array_equal(frame[PSensor1[0][0]:PSensor1[0][1],PSensor1[1][0]:PSensor1[1][1]], Sensor[PSensor1[0][0]:PSensor1[0][1],PSensor1[1][0]:PSensor1[1][1]]))):
        _thread.start_new_thread(acao, (0.2, pynput.keyboard.Key.up))

    if(np.array_equal(frame[PSensor2[0][0]:PSensor2[0][1],PSensor2[1][0]:PSensor2[1][1]], Sensor[PSensor2[0][0]:PSensor2[0][1],PSensor2[1][0]:PSensor2[1][1]])):
        _thread.start_new_thread(acao, (0.2, pynput.keyboard.Key.down))

    #aperta exc para fechar o jogo
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

captura.release()
cv2.destroyAllWindows()

