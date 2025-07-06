/* 
 * File:     adc.c
 * Author:   Jun Okamoto Jr.
 * Date:     27/02/2016
 * Comments: Configura e faz leitura de canais analógicos
 * Revision history: 
 */

#ifndef ADC_C
#define ADC_C

#include "adc.h"
#include "always.h" // para usar definições de INPUT e OUTPUT e union

///
/// Inicializa um canal analógico
///
/// @param adc_channel número do canal (0-4, 8-13 para PIC16F886)
///
void adc_init (unsigned char adc_channel) {

  switch (adc_channel) { // configura entrada e canal analógico
    case 0: // AN0
      TRISA0 = INPUT; // entrada
      ANS0 = ANALOG;  // canal analógico
      break;
    case 1: // AN1
      TRISA1 = INPUT; // entrada
      ANS1 = ANALOG;  // canal analógico
      break;
    case 2: // AN2
      TRISA2 = INPUT; // entrada
      ANS2 = ANALOG;  // canal analógico
      break;
    case 3: // AN3
      TRISA3 = INPUT; // entrada
      ANS3 = ANALOG;  // canal analógico
      break;
    case 4: // AN4
      TRISA5 = INPUT; // entrada
      ANS4 = ANALOG;  // canal analógico
      break;
    case 8: // AN8
      TRISB2 = INPUT; // entrada
      ANS8 = ANALOG;  // canal analógico
      break;
    case 9: // AN9
      TRISB2 = INPUT; // entrada
      ANS9 = ANALOG;  // canal analógico
      break;
    case 10: // AN10
      TRISB1 = INPUT; // entrada
      ANS10 = ANALOG; // canal analógico
      break;
    case 11: // AN11
      TRISB4 = INPUT; // entrada
      ANS11 = ANALOG; // canal analógico
      break;
    case 12: // AN12
      TRISB0 = INPUT; // entrada
      ANS12 = ANALOG; // canal analógico
      break;
    case 13: // AN13
      TRISB5 = INPUT; // entrada
      ANS13 = ANALOG; // canal analógico
      break;
    default:  // senão for canal analógico válido 
      return; // sai
  }
  ADCON0bits.ADCS = 2;  // clock de conversão FOSC/32 em 20MHz dá 1.6us
  // configura tensão de referência
  ADCON0bits.CHS = adc_channel; // canal analógico de 0 a 13 
  ADCON1bits.ADFM = 1;          // justificado à direita
  ADON = 0; // desabilita canal analógico para não consumir energia
  ADIE = 0; // desabilita interrupção, não é usada nessa biblioteca
} 

///
/// Faz a leitura de um canal ADC e retorna o valor de 10-bits
/// numa variável inteira
///
/// @param adc_channel número do canal (0-4, 8-13 para PIC16F886)
///
unsigned int adc_read(unsigned char adc_channel) {
	
  union wordtype adc_result; // resultado da conversão

  // Para PIC16F886 são válidos canais 0-4 e 8-13, fora disso sai 
  if ((adc_channel > 4 && adc_channel < 8) || adc_channel > 13) return (0);
 
  // continua processo
  ADCON0bits.CHS = adc_channel; // seleciona canal do ADC
  ADON = 1;    // liga canal analógico
  ADIF = 0;    // reseta flag de final de conversão
  ADRESL = 0;  // limpa registrador de resultado da conversão (LSB)
  ADRESH = 0;  // limpa registrador de resultado da conversão (MSB)				 

  GO = 1;                         // dispara processo de conversão
  while(!ADIF) continue;          // espera conversão terminar
  adc_result.byte.low = ADRESL;   // LSB do resultado da conversão
  adc_result.byte.high = ADRESH;  // MSB do resultado da conversão
  ADON = 0;                       // desliga canal analógico
  return (adc_result.word);       // retorna valor da conversão
}

#endif
