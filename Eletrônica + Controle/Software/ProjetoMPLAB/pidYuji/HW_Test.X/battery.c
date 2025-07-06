/* 
 * File:   battery.c
 * Author:   Jun Okamoto Jr.
 * Date:     9/02/2016
 * Comments: Faz leitura no nível da bateria do robô
 * Revision history: 
 *  13/06/2024 - chama spi_init() no init daqui
 */

// This is a guard condition so that contents of this file are not included
// more than once.  
#ifndef BATTERY_C
#define	BATTERY_C

#include "battery.h"
#include "spi.h"

///
/// Inicializa leitura de nível de bateria.
///
void battery_init() {
  // Supondo que o SPI já foi incializado, não há nada para fazer,
  // é só ler o nível da bateira direto, senão o SPI deve ser incializado aqui.
  // TODO: achar um jeito de saber se o SPI está inicializado e se não estiver, inicializar SPI
  spi_init(); // [jo:240613] inicializa SPI aqui
}

///
/// Faz a leitura do nível da bateria
/// @return: nível da bateria
///
uint8_t battery_level(void) {
  uint8_t level;       // nível a bateria
  spi_write(0x80);  // envia comando para leitura do nível de bateria pelo SPI
  level = spi_read();  // envia 0x00 para ler um byte e recebe nível
  return level; // retorna o nível da bateria
}

#endif
