/* 
 * File:     compass.h 
 * Authors:  Thiago Yukio Nagata Alves
 * Date:     28/04/2016
 * Comments: Controle da bússola do robô
 * Revision history: 
 *           [jo:160608] comentários acertados para 2017 e documentação Doxygem
 */

#ifndef COMPASS_H
#define COMPASS_H

#include <xc.h>
#include <stdint.h>

void compass_init(void); ///< inicializa bussola

uint8_t compass_get_id(void); ///< lê identificador da bussola (0x3d)

uint8_t compass_get_status(void); ///< lê status da bussola

uint16_t compass_get_X(void); ///< lê intensidade do campo no eixo x

uint16_t compass_get_Y(void); ///< lê intensidade do campo no eixo y

uint16_t compass_get_Z(void); ///< lê intensidade do campo no eixo z

uint16_t compass_get_temperature(void); ///< lê temperatura

uint16_t compass_get_heading(void); ///< le o angulo com o norte

void compass_calibrate(void); ///< calibra a bussola, movimenta robô, requer pwm

void compass_enable(void); ///< liga o bussola

void compass_disable(void); ///< desliga o bussola

void compass_temperature_enable(void); ///< habilita o sensor de temperatura

void compass_temperature_disable(void); ///< desabilita o sensor de temperatura

void compass_set_operativemode(uint8_t mode); ///< configura o modo de operação
                                              //   0 - low power, 1 - medium, 2 - high, 3 - ultra high

void compass_set_conversionmode(uint8_t mode); ///< configura o modo de conversão
                                               //   0 - conversão contínua, 1 - conversão única

void compass_set_datarate(uint8_t mode); ///< configura a taxa de dados de saÌda
                                         //   0 - 0.625Hz, 1 - 1.25Hz, 2 - 2.5Hz ..., 7 - 80Hz

void compass_set_fastdatarate(uint8_t mode); ///< habilita taxas de dados mais rápidas
                                             //   0 - 155Hz,  1 - 300Hz,  2 - 560Hz,  3 - 1000Hz

void compass_set_scale(uint8_t scale); ///< configura o fundo de escala
                                       //   0 - 4 gauss, 1 - 8, 2 - 12, 3 - 16

void compass_reset(void); ///< reseta bussola

uint8_t compass_get_interruptsource(void); ///< lê fonte de interrupção (não implementado)

void compass_configure_interrupts(uint8_t config); ///< configura interrupções (não implementado))

#endif