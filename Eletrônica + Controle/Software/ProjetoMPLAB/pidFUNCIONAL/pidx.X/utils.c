/* Includes genericos */
#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include "always.h"
#include "delay.h"

/* includes especificos */
#include "utils.h"
#include "protocol.h"
#include "serial.h"

_PID_MATH convertToReal(unsigned char* chars) {
  _PID_MATH value = 0.0;
  _PID_MATH temp = 0.0;
  _PID_MATH potDez = 1.0;
  _PID_MATH signal = 1.0;
  unsigned char decimal = FALSE;
  unsigned char i = 0;

  if (chars[0] == '-') {
     signal = -1.0;
     i = 1;
  }
  for (; i<MAX_LEN; i++) {
    if (chars[i] == 0)
      break;
    if ( (chars[i] < '0') &&
         (chars[i] > '9') &&
         (chars[i] != '.')) {
      break;
    }
    if (chars[i] == '.') {
       potDez = 0.1;
       decimal = TRUE;
    } else {
        temp = (chars[i] & 0x0f);
        if ( decimal != TRUE ) {
          value = (value * 10.0f) + temp;
        } else {
          value = value + (temp * potDez);
          potDez = potDez * 0.1f;      
        }
    }
  }
  return value * signal;
} // convertToReal

void printReal( _PID_MATH value) {
  // [jo:240322] não dá pa imprimir float.
  // nada do que está comentado abaixo funciona
//  char buffer[20];
//  int status;
//  char *ip;
//  ip = buffer;
//  printf("%7.2f", value);
//  sprintf(buffer, "%f", value);
//  ip = ftoa(value, &status);
//  putst(buffer);
  
  // [jo:240322] Solução atual: finge real imprimindo 2 inteiros com número fixo
  //                            de decimais
  int integerPart = 0;
  unsigned int decimalPart = 0;
  signed char signal = 1;    // inicialmente marca como positivo
  if (value < 0) {           // se o número for negativo
    signal = -1;             // armazena o sinal
    value *= (float) signal; // deixa o número positivo
  }
  integerPart = (int)value;  // parte inteira sem sinal 
  decimalPart = (unsigned int)((value - (float)integerPart) * 10000.0f); // cálculo da parte decimal
  if (signal < 0) putch('-');
  printf("%d.%d", integerPart, decimalPart);
} // printReal