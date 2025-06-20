#ifndef POSITION_SENSOR_H
#define POSITION_SENSOR_H

#include <xc.h>

/*
   INTERFACE
*/
#define _POSITION long // 24-bits

void pos_init(void);

///
/// Atualiza a contagem do encoder.
///
/// @param char port - conteúdo do PORTB (usando I-o-C)
/// @param char init - bit inicial de 2-bits de estado de port
/// @param char dir  - usar 0 ou 1 para contagem positiva no sentido desejado
///
void pos_UpdatePosition(char port, char init, char dir);

void pos_setCurrentPosition(_POSITION pos);

_POSITION pos_getCurrentPosition(void);

#endif