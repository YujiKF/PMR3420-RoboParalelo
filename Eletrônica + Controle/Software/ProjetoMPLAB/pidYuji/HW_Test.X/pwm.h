/* 
 * File:     pwm.h 
 * Author:   Jun Okamoto Jr.
 * Date:     7/02/2016
 * Comments: Gera PWM para acionamento dos motores
 * Revision history: 
 * 13/05/2023 - #defines movidos para pwm.c para poder usar no simulador e no robô
 */

#ifndef PWM_H
#define PWM_H

#include <xc.h>

//#define DIR1 RA5  // direção do PWM 1
//#define DIR2 RA6  // direção do PWM 2

void pwm_init(void); ///< inicializa a funcao de PWM com uma determinada frequencia

void pwm_set(int channel, int duty_cycle); ///< define o duty cycle para cada motor

void pwm_direction(int dir); ///< altera a direção do movimento

// Somente para testes de hardware, não incluir para a Atividade 6 daqui para baixo

//#define PWM1 RC2
//#define PWM2 RC1

void pwm_off(void); // desliga os motores.

void pwm_on(void); // liga motores com duty cycle fixo.

void pwm_output_control(void); // controle das saídas PWM para interrupção de Timer 1

// Fim inclusão para testes de hardware

#endif