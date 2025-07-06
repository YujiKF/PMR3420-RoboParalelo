/* 
 * File:      sensor.h
 * Author:    Jun Okamoto Jr.
 * Date:      11/03/2016
 * Comments:  Dá acesso aos sensores e buzzer do robô
 * Revision history:
 */

#ifndef SENSOR_H
#define SENSOR_H

void sensor_init(void); ///< inicializa sensores de linha e proximidade

void sensor_power(char state); ///< liga e desliga alimentação dos sensores e buzzer

char sensorLine_read(void); ///< faz as três leituras do sensor de linha

unsigned int sensorNear_read(void); ///< faz a leitura do sensor de distancia

#endif