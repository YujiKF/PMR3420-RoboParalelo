/* POSITION CONTROLLER
   O controlador de posicao deve fazer 4 tarefas:
   - ler encoder
   - realizar o controle PID
   - receber setpoints pela serial
   - piscar o led de heartbeat

   O encoder é lido por Interrupt-on-Change (I-o-C) do port B, por isso
   precisa incluir position_sensor.h

   As demais tarefas, fora da leitura do encoder, serao realizadas por
   uma multitasking simplificado, com tick de 1 ms marcado pela 
   interrupção do Timer 0. 
   Cada uma das tarefas serah acionada em seu tempo correto;
   as tarefas estao criadas no arquivo tasks.c

*/

/* TaskId e intervalo para scheduling de cada uma das tarefas */
#define POLLING_PERIOD 39                    // 998,4 us (~1 ms))
#define TMR0_SETTING (0xff - POLLING_PERIOD) // valor inicial da contagem do Timer 0

/* Includes genericos */
#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include "always.h"
#include "delay.h"

/* Includes especificos */
#include "position_controller.h"
#include "multitasking.h"
#include "position_sensor.h" // para i-o-c

/* Configuracao do PIC */
#pragma config FOSC=EC
#pragma config WDTE=OFF
#pragma config LVP=OFF
#pragma config BOREN=OFF
#pragma config PWRTE=OFF
#pragma config MCLRE=ON
#pragma config CP=OFF
#pragma config CPD=OFF
#pragma config IESO=OFF
#pragma config FCMEN=OFF
#pragma config WRT=OFF
#pragma config DEBUG=OFF

void pic_init() {
  TRISA &= 0b11001111;  // RA4 é saída para debug do PID, RA5 é DIR1 para testes no robô de PMR3406
  ANSEL &= 0b11100001;
  PORTA &= 0b11001111;  // RA4 e RA5 são zero inicalmente
  
  TRISB  = 0b01011111;  // [jo:231025] RB3 e RB4 são entradas para encoder e RB6 é entrada da chave
                        // [jo:231025] RB5 é saida para piscar o LED
  ANSELH = 0;           // [jo:231025] RB0-RB5 são todos digitais
  IOCB  = 0b01011000;   // [jo:231025] interrupt on change
  RBIE = 1;             // [jo:231025] habilita interrupção do port B
  
  TRISC = 0b10011110;   //bit 0 (EN) = output (enable do L298)
                        //bit 1 (pwm) = input (vai ser configurado no motor)
                        //bit 2 (pwm) = input (vai ser configurado no motor)
                        //bit 3 (livre) input
                        //bit 4 (livre) input
                        //bit 5 (livre) output
                        //bit 6 (tx serial) = output 
                        //bit 7 (rx serial)= input
  
  TMR0 = TMR0_SETTING;
  OPTION_REG = 0b01000110;  // programa Timer 0 prescaler 1:128, nRBPU (bit7) habilitado
  WPUB = 0b01000000;
  T0IE = 1;             // habilita interrupção do Timer 0
} // initPic

/*================================================
  INTERRUPCAO
 */
#define TICK_COUNT 500 // 500 ms   

void __interrupt() isr(void) {
  
  static int interruptCounter = 0;
  
  if (T0IE && T0IF) {  // se for interrupção do Timer 0
    interruptCounter++; // heartbeat counter
    if (interruptCounter > TICK_COUNT) { // [jo:240315] 500 ms
//      LED = ~LED;       // heartbeat LED (comentar se não teste)
      interruptCounter = 0;
    }

    tsk_timeStamp++;           // update multitasking timer, [jo:240315] ~1 ms
    TMR0 = TMR0_SETTING;       // recarrega contagem no Timer 0
    T0IF = 0;                  // limpa interrupção
  } 
  
  if (RBIE && RBIF) { // I-o-C para encoder
    char portB = PORTB;
    pos_UpdatePosition(portB, 3, 1);
    RBIF = 0;
  }
} // interrupt isr

/***********************************************
  Main to test encoder
 */
#include "motor.h"
#include "serial.h"

void main() {
  _POSITION main_position;
  _POSITION prev_position;
  pic_init();
  ser_init();
  mot_init();
  pos_init();
  ei();      
  RA5 = 1;
  mot_setExcitation(-500);
  while (TRUE) {
    main_position = pos_getCurrentPosition();
    if (prev_position != main_position) {
      printf("%d\n", main_position);
      prev_position = main_position;
    }
    DelayMs(20);
  }
} // main
