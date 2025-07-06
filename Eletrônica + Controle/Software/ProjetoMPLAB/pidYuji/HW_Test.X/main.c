/* 
 * File:     pwm.c 
 * Author:   Bianca Ângelo da Rocha Barreto e Caio Yuji Kina Fujimoto
 * Date:     05/07/2025 
 * 
 * Comments: Controla a posição do motor conforme comando na serial, mais informações em protocol.c, além disso,
 * muda o estado do LED através do botão
 *           
 * 
 */
#include <xc.h>

// #pragma config statements should precede project file includes.

// CONFIG1
#pragma config FOSC = EC       // Oscillator Selection bits (EC: I/O function on RA6/OSC2/CLKOUT pin, CLKIN on RA7/OSC1/CLKIN)
#pragma config WDTE = OFF      // Watchdog Timer Enable bit (WDT disabled and can be enabled by SWDTEN bit of the WDTCON register)
#pragma config PWRTE = ON      // Power-up Timer Enable bit (PWRT enabled)
#pragma config MCLRE = ON      // RE3/MCLR pin function select bit (RE3/MCLR pin function is MCLR)
#pragma config CP = OFF        // Code Protection bit (Program memory code protection is disabled)
#pragma config CPD = OFF       // Data Code Protection bit (Data memory code protection is disabled)
#pragma config BOREN =OFF      // Brown Out Reset Selection bits (BOR disabled)
#pragma config IESO = ON       // Internal External Switchover bit (Internal/External Switchover mode is enabled)
#pragma config FCMEN = ON      // Fail-Safe Clock Monitor Enabled bit (Fail-Safe Clock Monitor is enabled)
#pragma config LVP = OFF       // Low Voltage Programming Enable bit (RB3 pin has digital I/O, HV on MCLR must be used for programming)

// CONFIG2
#pragma config BOR4V = BOR40V  // Brown-out Reset Selection bit (Brown-out Reset set to 4.0V)
#pragma config WRT = OFF       // Flash Program Memory Self Write Enable bits (Write protection off)
// <------------ Até aqui -->

// Includes do projeto
// <------------ incluir sempre <-- daqui -->
#include "always.h"   // defines (obrigatórios), estruturas e unions úteis (incluir sempre)
#include <stdio.h>    // para poder usar sprintf()
// <------------ incluir sempre <-- até aqui -->
// <------------ incluir se for usar <-- daqui -->
#include "pwm.h"      // PWM para testes, os alunos devem alterar para a Atividade 6
#include "serial.h"   // para utilizar canal de comunicação serial
#include "key.h"      // para utilizar chave da placa
#include "motor.h"
#include "position_sensor.h"
#include "protocol.h" // Adicionado para o protocolo de comunicação serial 
#include "utils.h"    // Adicionado para funções utilitárias como conversão para float 
#include "pid.h"      // Adicionado para funções do controlador PID 
// <------------ incluir ser for usar <-- até aqui -->

// Definições
// Saídas
#define LED RB5      // bit de saída para o LED

// Macros para manipular bits
#define testbit(var, bit) ((var) & (1 << (bit)))
#define setbit(var, bit) ((var) |= (1 << (bit)))
#define clrbit(var, bit) ((var) &= ~(1 << (bit)))

// Variáveis globais
// Todas as variáveis globais usadas em interrupção precisam ser "volatile"
// é necessário colocar a descrição de cada variável

// Função de tratamento de interrupções
//     Ela é chamada somente na ocorrencia de uma interrupção.
//     No caso deste programa, o Timer 0 é programado para gerar um pedido de
//     interrupção a cada ~1 ms.
void __interrupt() isr(void) {  // Função geral de tratamento de interrupção
  
  // variáveis locais declaradas static mantém o valor
  static int tick = 0;     // contador de vezes que o Timer 0 interrompe
  
  // Timer 0
  // Interrompe a cada 5 ms aproximadamente.
  // Faz pisca o LED a cada 1 seg aproximadamente.
  // Controla o tempo de debounce da chave em conjunto com o I-O-C do PORT B
  if (TMR0IE && TMR0IF) {    // se for interrupção do Timer 0
    
    // inverte o LED a cada segundo
    if (++tick >= 2000) { // se interromper 2000x é ~2 s
      tick = 0;          // então zera o contador
      //LED = ~LED;        // inverte LED      
    } // fim - contagem de vezes que ocorre interrupção
        
    // Debounce da chave. Deve ser incluído na interrupção periódica de Timer.
    // São 2 ciclos para debounce entre 5 e 10 ms para interrupção de ~5ms. 
    // Deve ser alterado de acordo com o tempo dado pela interrupção do Timer.
    // Por exemplo, se a interrupção for a cada 1 ms, o parâmetro deve ser 10
    // o que resulta num debounce de 9 a 10 ms.
    key_debounce(2); // 2 é o número de ciclos para dar 5 a 10 ms 
    
    TMR0 = 0xff - 39;   // recarrega contagem no Timer 0 p/ 998,4 us (~1 ms) 
    TMR0IF = 0;         // limpa interrupção [cite: 16]
  } // fim - tratamento do Timer 0
  
  // Interrupt-on-change do PORT B usado pela chave
  // O tempo de debounce é controlado pelo Timer 0. A mudança de estado da chave
  // dispara uma contagem de tempo pelo Timer 0 de 5 a 10 ms. Toda a vez que 
  // houver mudança de estado da chave a contagem de tempo de debounce é 
  // zerada.
  if (RBIE && RBIF) { // se for mudança estado do Port B
    char portB = PORTB; // faz a leitura do Port B, isso reseta a condição de interrupção junto com RBIF = 0
    pos_UpdatePosition(portB, 3, 1); // Atualiza a posição do encoder [cite: 16]
    key_read(portB);    // faz a leitura da chave [cite: 16]
    RBIF = 0;           // reseta o flag de interrupção para poder receber outra interrupção [cite: 16]
  } // fim - tratamento I-O-C PORT B
} // fim - Tratamento de todas as interrupções

// inicializa Timer 0
void t0_init(void) {
  // o Timer 0 é utilizado para interrupção periódica a cada 5 ms aproximadamente
  OPTION_REGbits.T0CS = 0; // usa clock interno FOSC/4 
  OPTION_REGbits.PSA = 0;  // Prescaler é para Timer 0 e não para WDT 
  OPTION_REGbits.PS = 7;   // ajusta Prescaler para 1:256 
  TMR0 = 0xff - 39;        // valor inicial do Timer 0 p/ 998,4 us
  TMR0IE = 1;              // habilita interrupção do Timer 0 
}

// inicializa LED
void led_init(void) {
  TRISB5 = 0;  // RB5 é saída para LED
  ANS13 = 0;   // RB5/AN13 é digital  
  LED = 0;
}

void pic_init() {
  TRISA &= 0b11001111;  // RA4 é saída para debug do PID, RA5 é ENABLE
  ANSEL &= 0b11100001;
  PORTA &= 0b11101111;  // RA4 é zero inicalmente
  
  TRISB  = 0b01011111;  // [jo:231025] RB3 e RB4 são entradas para encoder e RB6 é entrada da chave
                        // [jo:231025] RB5 é saida para piscar o LED
  ANSELH = 0;           // [jo:231025] RB0-RB5 são todos digitais
  IOCB  = 0b01011000;   // [jo:231025] interrupt on change
  RBIE = 1;             // [jo:231025] habilita interrupção do port B
  
  TRISC = 0b10011111;   //bit 0 (livre) input
                        //bit 1 (pwm) = input (vai ser configurado no motor)
                        //bit 2 (pwm) = input (vai ser configurado no motor)
                        //bit 3 (livre) input
                        //bit 4 (livre) input
                        //bit 5 (livre) output
                        //bit 6 (tx serial) = output 
                        //bit 7 (rx serial)= input
  
  TMR0 = 0xff - 39;
  OPTION_REG = 0b01000110;  // programa Timer 0 prescaler 1:128, nRBPU (bit7) habilitado
  WPUB = 0b01000000;
  T0IE = 1;             // habilita interrupção do Timer 
} // initPic
  
void main() {
  _MESSAGE receivedMessage; // Variável para armazenar a mensagem recebida 
  _PID_MATH parsedValue;    // Variável para armazenar o valor numérico do comando 

  pic_init();         // Inicializa a PIC
  ser_init();         // Inicializa a serial
  mot_init();         // Inicializa o motor
  pos_init();         // Inicializa o módulo para cálculo de posição do motor
  key_init();         // Inicializa a chave da placa PIC
  pid_init();         // Inicializa o controlador PID 
  pro_init();         // Inicializa o módulo de protocolo 
  pro_setMyId('a');   // Define o ID do PIC para 'a' (ou o caractere desejado) 
 
  ei(); // Habilita as interrupções globais

  //mot_setExcitation(500); // Removido: Acionamento de motor para teste inicial 
  
  while (TRUE) {
    // Tenta obter uma mensagem da serial. pro_getMessage() é não-bloqueante. 
    receivedMessage = pro_getMessage();

    // Se uma mensagem válida foi recebida, processe-a 
    if (receivedMessage.messageType != PRO_NO_MESSAGE) {
      // Converte a string de valor recebida para um tipo numérico float (_PID_MATH) 
      parsedValue = convertToReal(receivedMessage.value);

      // Processa o comando com base no tipo de mensagem 
      switch(receivedMessage.messageType) {
        case PRO_SET_POSITION:
          pid_setPoint(parsedValue); // Define o setpoint do PID 
          putst("SetPoint: ");
          printReal(parsedValue); // Imprime o valor no serial para feedback 
          putlf; // Nova linha 
          break;
        case PRO_SET_HOME:
          pos_setCurrentPosition(0); // Define a posição atual como 'home' (0) 
          pid_clearError(); // Limpa erros do PID ao redefinir a posição 
          putst("Home set. Position cleared.");
          putlf;
          break;
        case PRO_SET_PROPORTIONAL_GAIN:
          pid_setProportionalGain(parsedValue); // Define o ganho Proporcional 
          putst("Kp: ");
          printReal(parsedValue);
          putlf;
          break;
        case PRO_SET_INTEGRAL_GAIN:
          pid_setIntegralGain(parsedValue); // Define o ganho Integral 
          putst("Ki: ");
          printReal(parsedValue);
          putlf;
          break;
        case PRO_SET_DERIVATIVE_GAIN:
          pid_setDerivativeGain(parsedValue); // Define o ganho Derivativo 
          putst("Kd: ");
          printReal(parsedValue);
          putlf;
          break;
        default:
          putst("Comando desconhecido.");
          putlf;
          break;
      }
    }
    
    char keyIn = key_pressed();             // Variável para armazenar estado da chave
    if (keyIn) {                            // se detectar que a chave foi pressionada
        LED = ~LED;                         // Muda estado do LED
    }     

    // O controle PID deve ser executado periodicamente.
    pid_pid();
    
    __delay_ms(10); // Reduzindo o delay para dar mais tempo para o loop principal,
                    // mas ainda controlando a velocidade de execução. Ajustar conforme necessário.
  }
} // main