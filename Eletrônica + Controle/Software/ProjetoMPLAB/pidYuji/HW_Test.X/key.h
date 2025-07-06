/* 
 * File:     key.h 
 * Author:   Jun Okamoto Jr.
 * Date:     7/02/2016
 * Comments: Controla leitura de chave
 * Revision history: 
 */

#ifndef KEY_H
#define	KEY_H

#include <xc.h> // include processor files - each processor file is guarded.
#include <stdint.h>

void key_init(void); ///< Inicializar chave

void key_debounce(int cycles); ///< faz o debounce da chave, deve ser chamada na interrupção periódica

void key_read(char port); ///< faz a leitura da chave, deve ser chamada no I-O-C do Port B

char key_pressed(void); ///< determina de a chave foi pressionada

#endif	/* KEY_H */

