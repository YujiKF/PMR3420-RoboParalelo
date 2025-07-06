/* 
 * File:     compass.h 
 * Authors:  Thiago Yukio Nagata Alves
 * Date:     28/04/2016
 * Comments: Controle do magnetômetro do robô
 * Revision history: 
 *  13/06/2024 - chama spi_init() no init daqui
 */

#ifndef COMPASS_C
#define COMPASS_C

#include <xc.h>
#include <stdint.h>
#include <math.h>
#include "always.h"
#include "compass.h"
#include "spi.h"

#define COMPASS_DEVICE_CODE 5

volatile int16_t Ycorr = 0, Xcorr = 0;   // Fator de correcao de leitura obtido na calibracao

///
/// Adquire o id do magnetometro
/// @return retorna o id do magnetometro em uint8
///
uint8_t compass_get_id() {
  uint8_t command_byte = (COMPASS_DEVICE_CODE << 5) + 0;
  spi_write(command_byte);  // envia comando para ler ID
  uint8_t compass_id = spi_read(); // recebe ID
  return compass_id;
}


///
/// Inicializa o magnetometro
///
void compass_init() {
  uint8_t command_byte;
  spi_init(); // [jo:240613] inicializa SPI
  command_byte = (COMPASS_DEVICE_CODE << 5) + 1;
  spi_write(command_byte);  // envia comando de inicializar
  
  compass_set_datarate(7);        // Inicializa com taxa de 80 Hz
  compass_set_operativemode(3);   // Inicializa precisao ultra high
  compass_set_scale(0);           // Seta a menor escala possivel: 4 gauss
  
  return;
}


///
/// Liga o magnetômetro
///
void compass_enable(){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 2;
  spi_write(command_byte);  // envia comando de ligar
  return;
}


///
/// Desliga o magnetômetro
///
void compass_disable(){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 3;
  spi_write(command_byte);  // envia comando de desligar
  return;
}


///
/// Habilita o sensor de temperatura
///
void compass_temperature_enable(){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 4;
  spi_write(command_byte);  // envia comando de ligar sensor de temperatura
  return;
}


///
/// Habilita o sensor de temperatura
///
void compass_temperature_disable(){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 5;
  spi_write(command_byte);  // envia comando de desligar sensor de temperatura
  return;
}


///
/// Configura o modo de operação do magnetometro
/// @param mode - 0 - low power, 1 - medium, 2 - high, 3 - ultra high
///
void compass_set_operativemode(uint8_t mode){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 6;
  spi_write(command_byte);
  spi_write(mode);
  return;
}


///
/// Configura o modo de conversão de dados
/// @param mode - 0 para conversao continua, 1 para conversao unica
///
void compass_set_conversionmode(uint8_t mode){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 7;
  spi_write(command_byte);
  spi_write(mode);
  return;
}


///
/// Configura a taxa de emissao de dados
/// @param mode - 0 - 0.625 Hz, 1 - 1.25 Hz, 2 - 2.5 Hz, 3 -  5 Hz
///               4 - 10    Hz, 5 - 20   Hz, 6 - 40  Hz, 7 - 80 Hz
///
void compass_set_datarate(uint8_t mode){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 8;
  spi_write(command_byte);
  spi_write(mode);
  return;
}


///
/// Habilita taxas de dados mais r·pidas
/// Modos possÌveis: 0 - 155 Hz,  1 - 300 Hz,  2 - 560 Hz,  3 - 1000 Hz
/// @param mode - determina o modo de velocidade rapida dos dados
///
void compass_set_fastdatarate(uint8_t mode){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 9;
  spi_write(command_byte);
  spi_write(mode);
  return;
}


///
/// Configura o fundo de escala (0 - 4 gauss; 1 - 8 gauss; 2 - 12 gauss; 3 - 16 gauss)
/// @param scale - opcao do fundo de escala
///
void compass_set_scale(uint8_t scale){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 10;
  spi_write(command_byte);
  spi_write(scale);
  return;
}


///
/// Reseta o magnetômetro
///
void compass_reset(){
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 11;
  spi_write(command_byte);  // envia comando de resetar
  return;
}


///
/// Informa se ha dados novos nos eixos X, Y, Z, ou qualquer um deles nos bits 0-3, respectivamente
/// e se os dados foram sobrescritos em X, Y, Z, ou qualquer um deles nos bits 4-7, respectivamente
/// @return retorna o status do magnetometro em uint8
///
uint8_t compass_get_status(){
  uint8_t data;
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 12;
  spi_write(command_byte);  // solicita status
  data = spi_read();
  return data;
}


///
/// Adquire os dados do magnetometro no eixo X em complemento de dois
/// @return retorna a leitura do eixo X em uint16
///
uint16_t compass_get_X(){
  uint16_t data;
  uint8_t command_byte; 
  command_byte = (COMPASS_DEVICE_CODE << 5) + 13;
  
  spi_write(command_byte);  // solicita leitura do eixo X
   
  data = spi_read();   // armazena os bits mais significativos primeiro
  data <<= 8;
 
  data |= spi_read();  // armazena os bits menos significativos
  
  return data - (uint16_t)Xcorr; // aplica-se o fator de correcao obtido na calibracao
}


///
/// Adquire os dados do magnetometro no eixo Y em complemento de dois
/// @return retorna a leitura do eixo Y em uint16
///
uint16_t compass_get_Y(){
  uint16_t data;
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 14;
  
  spi_write(command_byte);  // solicita leitura do eixo Y
   
  data = spi_read();   // armazena os bits mais significativos primeiro
  data <<= 8;
  
  data |= spi_read();  // bits menos significativos
  
  return data - (uint16_t)Ycorr; // Aplica-se o fator de correcao calculado na calibracao
}


///
/// Adquire os dados do magnetometro no eixo Z em complemento de dois
/// @return retorna a leitura do eixo Z em uint16
///
uint16_t compass_get_Z(){
  uint16_t data;
  uint8_t command_byte;
  command_byte = (COMPASS_DEVICE_CODE << 5) + 15;
  
  spi_write(command_byte);  // solicita leitura do eixo Z
   
  data = spi_read();   // armazena os bits mais significativos primeiro
  data <<= 8;
  
   
  data |= spi_read();  // le os bits menos significativos
  return data;
}


///
/// Adquire a leitura da temperatura do magnetometro
/// @return a leitura da temperatura em uint16
///
uint16_t compass_get_temperature(){
  uint16_t data, temp;
  uint8_t command_byte;
  
  command_byte = (COMPASS_DEVICE_CODE << 5) + 16;
  
  spi_write(command_byte);  // solicita leitura da temperatura
   
  data = (uint16_t)(spi_read()) << 8;   // armazena os bits mais significativos primeiro
  data |= (uint16_t)spi_read();
  
  temp = (data/8)+20;
  
  return temp;
}


///
/// le o angulo com o norte
/// @return retorna o angulo com o norte
///
uint16_t compass_get_heading(){
  uint16_t heading;
  int16_t Xread, Yread; //xRead
  
  // Primeira leitura para comparacao
  Xread = (int16_t)compass_get_X();
  Yread = (int16_t)compass_get_Y();
    
  // Faz mais 7 medidas
  for(int i = 1; i < 8; i++){
    Xread = (Xread + (int16_t)compass_get_X()) / 2;  // Tira a medias das medidas
    Yread = (Yread + (int16_t)compass_get_Y()) / 2;  // Tira a medias das medidas
    __delay_ms(1);
  }
  
  float angle;  // Angulo em radianos
  angle = (float)atan((float)Yread/(float)Xread);
  angle *= 180. / M_PI;
  
  // Tratamento trigonometrico
  if (Xread > 0){    
    if(Yread > 0){      // Primeiro quadrante
      heading = (uint16_t) angle;                  
    }
    else {              // Quarto quadrante
      heading = (uint16_t) (360. + angle);
    }
  } 
  
  else {          // Caso a leitura de X seja negativa
      // Para o segundo e terceiro quadrante o tratamento e'igual
      heading = (uint16_t) (180. + angle);
  }
  
  return heading;
}


///
/// Calibra a bussola
///
//void compass_calibrate(){
//  int16_t Xmax, Xmin, Ymax, Ymin, reading;
//  
//  Xmax = compass_get_X();    // Adquire leitura de X para comparacao
//  Xmin = Xmax;
//  
//  Ymax = compass_get_Y();    // Adquire leitura de Y para comparacao
//  Ymin = Ymax;
//  
//  // Robo vai girar para colher medidas
//  pwm_direction(3);         // gira cw
//  pwm_set(1, 150);          // Aciona os motores
//  pwm_set(2, 150);
//  
//  
//  for(uint16_t i=0; i < 10000 ; i++){   // Gira por um tempo determinado
//    reading = compass_get_X();   // faz a leitura do Eixo X
//    
//    if(reading > Xmax)           // Salva valores maximo e minimo encontrado
//      Xmax = reading;           
//    if(reading < Xmin)           
//      Xmin = reading;           
//    
//    reading = compass_get_Y();   // Salva valores maximo e minimo encontrado
//    
//    if(reading > Ymax)
//      Ymax = reading;
//    if(reading < Ymin)
//      Ymin = reading;
//    
//    delay_ms(1);
//  }
//  
//  // Para os motores
//  pwm_set(1, 0);         
//  pwm_set(2, 0);
//          
//  // Uma vez adquiridos extremos, calcula-se a amplitude da senoide
//  int16_t Ax, Ay;
//  Ax = Xmax - Xmin;
//  Ay = Ymax - Ymin;
//  
//  // Com a amplitude e' possivel calcular o fator de correcao da leitura
//  Xcorr = Xmax - Ax/2;
//  Ycorr = Ymax - Ay/2;
//  
//}


// funções de interrupção - não implementadas
uint8_t compass_get_interruptsource();

void compass_configure_interrupts(uint8_t config);

#endif
