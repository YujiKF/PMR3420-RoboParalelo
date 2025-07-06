/* 
 * File:     adc.h
 * Author:   Jun Okamoto Jr.
 * Date:     27/02/2016
 * Comments: configura e faz leitura de canais analógicos
 * Revision history: 
 */

#ifndef ADC_H
#define ADC_H

#include <xc.h>  // compilador XC8

extern void adc_init (unsigned char ADC_Channel); ///< inicializa canal analógico

extern unsigned int adc_read(unsigned char ADC_Channel); ///< faz a leitura de um canal analógico

#endif
