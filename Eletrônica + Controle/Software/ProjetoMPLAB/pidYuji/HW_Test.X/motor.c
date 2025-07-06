#include <xc.h>
#include "always.h"
#include "pwm.h"
#include "motor.h"

#define DIR1 RA5  // direção do PWM 1 
#define DIR2 RA6  // direção do PWM 2 

void mot_init(void) {
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

// Para a sua fiação específica (PWM1 em IN1/IN3, PWM2 em IN2/IN4, DIR1/RA5 em ENABLE)
void mot_setExcitation (_EXCITATION excitation) {
    // Certifica que o ENABLE está HIGH (assumindo que RA5 é DIR1/ENABLE)
    // RA5 já é configurado como saída e setado para HIGH em pic_init(), o que está correto.
    // Se por algum motivo RA5 for redefinido, garanta que ele permaneça HIGH.
    RA5 = 1; // Não necessário aqui se já está em pic_init()

    if (excitation > 0) { // Motor gira em uma direção (e.g., "para frente")
        // Aplica PWM1 (RC2) e desativa PWM2 (RC1)
        pwm_set(1, excitation); // Seta duty cycle para PWM1 (RC2)
        pwm_set(2, 0);          // Zera duty cycle para PWM2 (RC1)
    } else if (excitation < 0) { // Motor gira na direção oposta (e.g., "para trás")
        // Aplica PWM2 (RC1) e desativa PWM1 (RC2)
        pwm_set(1, 0);              // Zera duty cycle para PWM1 (RC2)
        pwm_set(2, -excitation);    // Seta duty cycle para PWM2 (RC1), usando valor absoluto
    } else { // excitation == 0, motor para
        pwm_set(1, 0); // Zera duty cycle para PWM1 (RC2)
        pwm_set(2, 0); // Zera duty cycle para PWM2 (RC1)
    }
}