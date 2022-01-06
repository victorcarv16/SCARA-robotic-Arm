from tkinter import*
import tkinter as tk
import math
from functools import*
import numpy as np
import matplotlib.pyplot as plt
from pyfirmata import Arduino, util
import time

placa=Arduino("COM3")# ESTABELECENDO CONEXÃO SERIAL  COM O ARDUINO 
direção1 = 1
direção2 = 1
direção3 = 1
maior = 0
menor = 0
p=0
b1 = 200 #TAMANHO DO PRIMEIRO BRAÇO DO ROBÔ
b2 = 200 #TAMANHO DO SEGUNDO BRAÇO DO ROBÔ
t = [0,0,0,0,0,0,0] # VETOR QUE IRÁ RECEBER OS ANGULOS DOS BRAÇOS (ANGULO ATUAL E ANTERIOR )
janela = tk.Tk() #CRIANDO ABA COM JANELA 



def bt1():  #DEFININDO FUNÇÃO AUXILIAR 
    x = float(str(ed1.get()))  #variavel X
    y = float(str(ed2.get()))  #variavel Y
    z = float(str(ed3.get()))  #variavel Z                 
    amp = (x **2 + y **2) ** .5 #VARIAVEL QUE RECEBE O MODULO DO VETOR (xy)

    if(y>=0 and amp <=400 and z<=200 and z>=0):	

       #TESTANDO SE A COORDENADA ESCOLHIDA ESTA DENTRO DO RAIO DE ALCANSE DO BRAÇO
        if x>0:
            t.insert(0,(math.acos((x**2+y**2-b1**2-b2**2)/(2*b1*b2))))     
        if x<=0:
            t.insert(0,-(math.acos((x**2+y**2-b1**2-b2**2)/(2*b1*b2))))
        b = y*(b1+b2*math.cos(t[0]))-(x*b2*math.sin(t[0]))
        a = x*(b1+b2*math.cos(t[0]))+(y*b2*math.sin(t[0]))
        t.insert(1,(math.atan2(b,a)))
        t.insert(2,z*72) 
        lb7["text"] = round (math.degrees(t[1]),2) #TETA1
        lb8["text"] = round (math.degrees(t[0]),2) #TETA2
        lb9["text"] = z*72                         #TETA3
        lb10["text"] = round (math.degrees(t[1]-t[4]),2) #∆TETA1
        lb11["text"] = round (math.degrees(t[0]-t[3]),2) #∆TETA2
        lb12["text"] = z*72-t[5]                         #∆TETA3
        lb['text'] = '          CONVERTER COORDENADAS!!'

        # DEFININDO O SENTIDO DE ROTAÇÃO DO EIXO DE CADA MOTOR DE PASSO    
        if (round (math.degrees(t[1]-t[4]),2)) >0:
            direção1 = 1
            print('Ө1 sentido horário')            
        else:
            direção1 = 0
            print('Ө1 sentido anti horário')
        if (round (math.degrees(t[0]-t[3]),2)) >0:
            direção2 = 1
            print('Ө2 sentido horário')  
        else:
            direção2 = 0
            print('Ө2 sentido anti horário')    
        if (z*72-t[5]) >0:
            direção3 = 0
            print('Ө3 sentido anti horário\n')
        else:
            direção3 = 1
            print('Ө3 sentido horário\n')  
        # DEFININDO A QUANTIDADE DE PASSOS DE CADA MOTOR DE PASSO    
        passos1 = abs(round ((math.degrees(t[1]-t[4]))/0.9))  # QUANTIDADE DE PASSOS DO MOTOR1
        passos2 = abs(round ((math.degrees(t[0]-t[3]))/0.9)) #QUANTIDADE DE PASSOS DO MOTOR2
        passos3 = abs(round(((z*72-t[5])/0.9))) # QUANTIDADE DE PASSOS DO MOTOR3
        print('posição angular das juntas\n Ө1  Ө2  Ө3')
        print(round (math.degrees(t[1])),round (math.degrees(t[0])),round (t[2]),round (math.degrees(t[3])),round (math.degrees(t[4])),round (t[5]))
        print('\n')
        print('passos do motores')
        print((passos1),(passos2),(passos3))
        print('\n')
        if(passos1 >= passos2):
            maior = passos1
            p=4
            menor = passos2
            
        else:
            menor = passos1
            maior = passos2
            p=7
            
        print('maior dos numeros', maior)
        print('menor dos numeros', menor)
        # ENVIANDO DADOS DE ENABLE
        placa.digital[2].write(0);
        placa.digital[5].write(0);
        placa.digital[8].write(0);
        
        # ENVIANDO DADOS DE DIREÇÃO  
        placa.digital[3].write(direção1);
        placa.digital[6].write(direção2);
        placa.digital[9].write(direção3);
# ESTABELECENDO CONEXÃO SERIAL  COM O ARDUINO E ENVIANDO DADOS DE PULSOS
        for i in range (menor):
            placa.digital[4].write(1);
            placa.digital[7].write(1);
            time.sleep(0.1)
            placa.digital[7].write(0);
            placa.digital[4].write(0);
        i=0
        for j in range (maior-menor):
            placa.digital[p].write(1);
            time.sleep(0.1)
            placa.digital[p].write(0);
            time.sleep(0.1)
        j=0
        for k in range (passos3):
            placa.digital[10].write(1);
            time.sleep(0.1)
            placa.digital[10].write(0);
            time.sleep(0.1)            
        k=0
        # PLOTANDO GRÁFICO 2D 
        plt.plot( x, y, 'go')  # green bolinha
        plt.title("LOCALIZAÇÃO DO PONTO ALVO")
        plt.show()         
    else:
        lb['text'] = 'VALORES INFORMADOS INVÁLIDOS!!'

ed1 = Entry(janela)
ed1.place(x=20, y=70)
ed2 = Entry(janela)
ed2.place(x=20, y=100)
ed3 = Entry(janela)
ed3.place(x=20, y=130)
ed4 = Entry(janela)
ed4.place(x=140,y=2)

bt = Button(janela, text= 'CONVERTER COORDENADAS', width=30, command=bt1)
bt.place(x=40, y=160)


lb16 = Label (janela, text='INFORME A PORTA: \n ').place(x=10,y=2)


lb = Label (janela, text='INSIRA AS COORDENADAS DO OBJETO ALVO \n EM MILIMETROS')
lb.place(x=40,y=34)
lb1 = Label (janela, text='X')
lb1.place(x=10,y=70)
lb2 = Label (janela, text='Y')
lb2.place(x=10,y=100)
lb3 = Label (janela, text='Z')
lb3.place(x=10,y=130)
lb4 = Label (janela, text='°---- Ө1')
lb4.place(x=220,y=70)
lb5 = Label (janela, text='°---- Ө2')
lb5.place(x=220,y=100)
lb6 = Label (janela, text='°---- Ө3')
lb6.place(x=220,y=130)
lb7 = Label (janela, text='0')
lb7.place(x=170,y=70)
lb8 = Label (janela, text='0')
lb8.place(x=170,y=100)
lb9 = Label (janela, text='0')
lb9.place(x=170,y=130)
lb10 = Label (janela, text='0')
lb10.place(x=170,y=190)
lb11 = Label (janela, text='0')
lb11.place(x=170,y=220)
lb12 = Label (janela, text='0')
lb12.place(x=170,y=250)
lb13 = Label (janela, text='°---- ∆Ө1')
lb13.place(x=220,y=190)
lb14 = Label (janela, text='°---- ∆Ө2')
lb14.place(x=220,y=220)
lb15 = Label (janela, text='°---- ∆Ө3')
lb15.place(x=220,y=250)



janela.title("INTERFACE GRÁFICA ROBÔ SCARA")

janela.geometry('300x300+200+200')
janela.mainloop()
