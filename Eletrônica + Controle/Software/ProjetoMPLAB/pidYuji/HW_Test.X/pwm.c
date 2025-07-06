/* 
 * File:     pwm.c 
 * Author:   Bianca Ângelo da Rocha Barreto e Caio Yuji Kina Fujimoto
 * Date:     12/05/2025 
 * 
 * Comments: Gera PWM para acionamento dos motores.
 *           As funções pwm_init e pwm_set foram implementadas para a Atividade 6.
 * 
 * Revision history:
 * 29/05/2025 - bugs fixed
 * 
 */

#ifndef PWM_C
#define PWM_C

// #include <stdio.h>
#include "always.h"
#include "pwm.h"

#define DIR1 RA5  // direção do PWM 1 
#define DIR2 RA6  // direção do PWM 2 

///
/// Inicializa a função de PWM com uma frequência 19.53 kHz
///
void pwm_init(void) {
    TRISC2 = 1;  // Desabilita saída, configurando-o para entrada (CCP1 - enhanced)
    TRISC1 = 1;  // Desabilita saída, configurando-o para entrada (CCP2)

    // Cálculo do período desejado do PWM
    // Fosc = 20 MHz, Fpwm = 19.53 kHz, TMR2 pre-scaler -> 4
    // Período da PWM = (PR2 + 1) * 4 * Tosc * TMR2Prescale
    // 51.2us = (PR2 + 1) * 4 * 0.05us * 1  => PR2 = 255
    PR2 = 255;
    T2CONbits.T2CKPS = 0b00;        // Prescaler do Timer2 = 1:1 

    // CCP1 (Enhanced PWM) - Saída em RC2/P1A
    CCP1CONbits.P1M = 0b00;         // Single output em P1A (RC2) 
    CCP1CONbits.CCP1M = 0b1100;     // Configurando o modo de PWM para P1A
                                
    CCPR1L = 0;                     // Inicializa duty cycle CCP1 em 0
    CCP1CONbits.DC1B1 = 0;          // DC1B1 e DC1B0 (LSBs do duty cycle) são 0.
    CCP1CONbits.DC1B0 = 0;         


    // CCP2 - não apresenta as funções avançadas entao não existe CCP2M
    CCP2CONbits.CCP2M = 0b1100;     // Configurando o modo de PWM para P1A                  
    
    CCPR2L = 0;                     // Inicializa duty cycle CCP2 em 0
    CCP2CONbits.DC2B1 = 0;          // DC2B1 e DC2B0 (LSBs do duty cycle) são 0.
    CCP2CONbits.DC2B0 = 0;         
    
    // Setup do TMR2, iniciando Timer2
    TMR2IF = 0;                     // Limpa flag do TMR2
    T2CONbits.T2CKPS = 0;           // Configura pre-scaler em 1:1
    TMR2ON = 1;                     // Liga o TMR2

    while (!TMR2IF);                // Espera o overflow de TMR2 para 
                                    // iniciar o ciclo de PWM

    TRISC2 = 0;                     // Habilita saída (CCP1 - enhanced)
    TRISC1 = 0;                     // Habilita saída (CCP2)

    ANS4 = 0;                       // RA5 como digital 
    TRISA5 = 0;                     // RA5 como saída para DIR1
    DIR1 = 0;                       // Direção inicial para frente

                                    // RA6 não tem ANSEL, é digital por padrão
    TRISA6 = 0;                     // RA6 como saída para DIR2
    DIR2 = 0;                       // Direção inicial para frente

}

///
/// Define o duty cycle da saida PWM
/// @param channel - canal do PWM (1: motor 1; 2: motor 2)
/// @param duty_cycle - porcentagem do duty cycle x 10 (valor de 0 a 1000)
///
void pwm_set(int channel, int duty_cycle) {
    if (duty_cycle < 0) duty_cycle = 0;         // Limita duty_cycle a 0
    if (duty_cycle > 1000) duty_cycle = 1000;   // Limita duty_cycle a 1000

    if (channel == 1) {                               // CCP1
        CCPR1L = (unsigned char)((duty_cycle) >> 2);  // Desloca o valor para 
                                                      // selecionar apenas os
                                                      // 8 bits mais significativos
        CCP1CONbits.DC1B = duty_cycle & 3;            // 2 bits - significativos

    }

    if (channel == 2) {                               // CCP2
        CCPR2L = (unsigned char)((duty_cycle) >> 2);  // Desloca o valor para 
                                                      // selecionar apenas os
                                                      // 8 bits mais significativos
        CCP2CONbits.DC2B1 = (duty_cycle & 0b10) >> 1; // Bit 1 
        CCP2CONbits.DC2B0 = duty_cycle & 0b01;        // Bit 0 
    }
}

///
/// Altera a direção de movimento
/// @param dir - código de direção
///              0 - para frente (ou qualquer outro valor)
///              1 - para trás
///              2 - gira para a esquerda
///              3 - gira para a direira
///
void pwm_direction(int dir) {
  switch (dir) {
    case 1:     // Para trás
      DIR1 = 1;
      DIR2 = 1;
      break;
    case 2:     // Para a esquerda
      DIR1 = 1;
      DIR2 = 0;
      break;
    case 3:     // Para a direita
      DIR1 = 0;
      DIR2 = 1;
      break;
    default:    // Para frente
      DIR1 = 0;
      DIR2 = 0;
  } 
}

#endif
