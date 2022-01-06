/*

VERMELHO = A+
AZUL = B-
VERDE = A-
AMARELO = B+

*/
#define QUANTIDADE_MOTORES 3
#define ANGULO_POR_PASSO 1.8 // em graus
#define MOTOR_BASE 0
#define MOTOR_INTERMEDIARIO 1
#define MOTOR_EFETUADOR 2

int pino_motor_controle_pulso[QUANTIDADE_MOTORES] = {7, 0, 0};
int pino_motor_controle_direcao[QUANTIDADE_MOTORES] = {6, 0, 0};
int pino_motor_controle_enable[QUANTIDADE_MOTORES] = {5, 0, 0};
float posicao_angular_motor[QUANTIDADE_MOTORES] = {0.0, 0.0, 0.0};
int tempo = 1000;

void configuracao_inicial(int *pino_motor_controle_pulso, int *pino_motor_controle_direcao, int *pino_motor_controle_enable);
void controle_sentido_rotacao(float angulo_desejado, int pino_motor_controle_direcao);

// -------------------------------------------------------------------------------------------------------------
void setup() 
{
  Serial.begin(9600);
  configuracao_inicial(pino_motor_controle_pulso, pino_motor_controle_direcao, pino_motor_controle_enable);
}

void loop() 
{
  
  /*
  if (Serial.available() > 0){
    velocidade = Serial.readString().toInt();
    Serial.println(velocidade);
    Serial.println("teste");
  }   

  tone(pino_controle_pulso, velocidade);
   */
  
  posicao_angular_motor[MOTOR_BASE] = -180.0;
  controle_posicao_motor(posicao_angular_motor[MOTOR_BASE], pino_motor_controle_pulso[MOTOR_BASE], pino_motor_controle_direcao[MOTOR_BASE], tempo);

  delay(500);

  posicao_angular_motor[MOTOR_BASE] = 180.0;
  controle_posicao_motor(posicao_angular_motor[MOTOR_BASE], pino_motor_controle_pulso[MOTOR_BASE], pino_motor_controle_direcao[MOTOR_BASE], tempo);

  delay(500);

  posicao_angular_motor[MOTOR_BASE] = 360.0;
  controle_posicao_motor(posicao_angular_motor[MOTOR_BASE], pino_motor_controle_pulso[MOTOR_BASE], pino_motor_controle_direcao[MOTOR_BASE], tempo);

  delay(500);

  posicao_angular_motor[MOTOR_BASE] = -360.0;
  controle_posicao_motor(posicao_angular_motor[MOTOR_BASE], pino_motor_controle_pulso[MOTOR_BASE], pino_motor_controle_direcao[MOTOR_BASE], tempo);

  delay(500);
  
}
// -------------------------------------------------------------------------------------------------------------

void controle_sentido_rotacao(float angulo_desejado, int pino_motor_controle_direcao)
{

  /* 
   
   Function that controls the rotation direction of a joint, if will clockwise or ...
   
  */

  digitalWrite(pino_motor_controle_direcao, LOW); // sentido anti-horario
  if (angulo_desejado < 0.0) 
  {
    digitalWrite(pino_motor_controle_direcao, HIGH); // sentido horario
  }

}

// void controle_posicao_motores(float *posicao_angular_motor)

void controle_posicao_motor(float angulo_desejado, int pino_motor_controle_pulso, int pino_motor_controle_direcao, int tempo)
{

  /*
   Function that setups angular position of a motor. Doing the correct rotation of the same.
   */
  
  // 1 - passo = 1.8º
  static int quantidade_passos = 0;
  static int i = 0;  

  controle_sentido_rotacao(angulo_desejado, pino_motor_controle_direcao);
  quantidade_passos = abs((int) (angulo_desejado/ANGULO_POR_PASSO));
  
  for(i = 0; i < quantidade_passos; i++)
  {
    digitalWrite(pino_motor_controle_pulso, HIGH);
    delayMicroseconds(tempo);
    digitalWrite(pino_motor_controle_pulso, LOW);
    delayMicroseconds(tempo);
  }

}

void configuracao_inicial(int *pino_motor_controle_pulso, int *pino_motor_controle_direcao, int *pino_motor_controle_enable)
{
  static int i = 0;
  
  for(i = 0; i < QUANTIDADE_MOTORES; i++)
  {  
    pinMode(pino_motor_controle_pulso[i], OUTPUT);
    pinMode(pino_motor_controle_direcao[i], OUTPUT);
    pinMode(pino_motor_controle_enable[i], OUTPUT);

    digitalWrite(pino_motor_controle_pulso[i], 1);
    digitalWrite(pino_motor_controle_direcao[i], 1);
    digitalWrite(pino_motor_controle_enable[i], 0);        
  }

}
