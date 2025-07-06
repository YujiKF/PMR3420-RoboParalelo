/* 
 * File:      sensor.c
 * Author:    Jun Okamoto Jr.
 * Date:      11/03/2016
 * Comments:  Dá acesso aos sensores e buzzer do robô
 * Revision history:
 *   13/06/2024 - altera delay para usar built-in do XC8
 */

#ifndef SENSOR_C
#define SENSOR_C

#include <xc.h> 
#include "always.h"
#include "adc.h"

#define SENS_PWR RA1

///
/// Liga e desliga alimentação dos sensores de buzzer
///
/// @param state 0 - (OFF) desligado, 1 - (ON) ligado
///
void sensor_power(char state) {
  if(state == ON) {  // se comando for para ligar
    SENS_PWR = ON;   // liga o sensor
    __delay_ms(50);    // o sensor de proximidade demora ~50 ms para dar uma resposta válida
  } else SENS_PWR = OFF; // senão desliga o sensor
}
///
/// Inicializa sensores.
/// Configura RA1 para saída digital para energia de sensores e buzzer
///           RA0 como canal A/D para sensor de proximidade
///           RA4, RA3, RA2 como digital para sensor de linha
///
void sensor_init(void) {

  // Alimentação dos sensores e buzzer
  ANS1 = 0;            // sensor power é digital
  TRISA1 = 0;          // sensor power é saída
  SENS_PWR = OFF;      // alimentação dos sensores desligada
  
  // Sensor de linha
  ANSEL &= 0b11100011; // 3 bits de dados digitais RA4, RA3 e RA2
  
  // Sensor de proximidade
  ANS0 = 1;           // canal analógico 0
  TRISA0 = 1;         // é entrada
  adc_init(0);        // inicializa conversor A/D para canal 0

}

///
/// Faz a leitura dos 3 bits do sensor de linha
///
char sensorLine_read(void) {
  
  // tem que manipular diretamente a porta A, bits 2, 3 e 4
  TRISA &= 0b11100011; // primeiro configura como saida
  PORTA |= 0b00011100; // coloca as saída em HIGH
  
  __delay_us(100);       // espera 100us para carregar capacitor do sensor
  
  TRISA |= 0b00011100; // configura como entrada
  __delay_us(800);     // espera 800 us antes de ler [jo:160503] atualizado para 800 pois o chão do lab é mais escuro
  char line_reading = (PORTA & 0b00011100) >> 2; // lê o valor da porta e reposiciona os bits como menos significativos
   
  return (line_reading); // retorna valor lido do sensor
}

///
/// Faz leitura do sensor de proximidade
///
unsigned int sensorNear_read(void) {
  return (adc_read(0)); // retorna leitura do canal A/D 0
}

#endif
