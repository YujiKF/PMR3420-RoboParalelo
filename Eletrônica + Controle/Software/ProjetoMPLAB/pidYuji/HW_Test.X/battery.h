/* 
 * File:   battery.h
 * Author:   Jun Okamoto Jr.
 * Date:     9/02/2016
 * Comments: Faz leitura no nível da bateria do robô
 * Revision history: 
 */

// This is a guard condition so that contents of this file are not included
// more than once.  
#ifndef BATTERY_H
#define	BATTERY_H

#include <xc.h>      // include processor files - each processor file is guarded.
#include <stdint.h>

void battery_init(void); ///< Inicializa leitura de bateria

uint8_t battery_level(void); ///< faz a leitura do nível de bateria

#endif	/* BATTEY_H */

