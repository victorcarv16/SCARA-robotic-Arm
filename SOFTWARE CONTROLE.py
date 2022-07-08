from pyfirmata import Arduino, util
import time

placa=Arduino("COM6")# ESTABELECENDO CONEXÃO SERIAL  COM O ARDUINO 

placa.digital[5].write(1);
placa.digital[8].write(1);
placa.digital[2].write(1);

# ENVIANDO DADOS DE DIREÇÃO  
placa.digital[9].write(1); #MOTOR2
placa.digital[6].write(1); #MOTOR 3
placa.digital[3].write(1); #MOTOR 1

for i in range (10000000000001000000000000000):
   # placa.digital[7].write(1);
    time.sleep(0.0000000000001)
    #placa.digital[10].write(0);
    placa.digital[7].write(0);

