/* 
 * File:     pwm_sim.c 
 * Author:   Jun Okamoto Jr.
 * Date:     7/02/2016 
 * Comments: Gera PWM para acionamento dos motores.
 *           O Timer 1 é utilizado para simular um sinal de PWM com
 *           50% de duty cycle.
 *           Esta implementação é só para testes do hardware, as funções
 *           pwm_init e pwm_set deverão ser implementados na Atividade 6.
 * Revision history:
 * 14/09/2022
 * 12/05/2023 - pwm.c adaptado para simulador
 * 13/05/2023 - #defines movidos para cá para poder usar .h no simulador e no robô
 */

#ifndef PWM_C
#define PWM_C

//#include <stdio.h>
#include "always.h"
#include "pwm.h" // [jo:230513] usa o mesmo .h do robô

#define PWM1 RC2  // somente para teste de hw [jo:230513] estava comentado
#define PWM2 RC1  // somente para teste de hw [jo:230513] estava comentado
#define DIR1 RB1  // direção do PWM 1 [jo:230513] movido do .h para cá
#define DIR2 RB2  // direção do PWM 2 [jo:230513] movido do .h para cá

///
/// Inicializa a função de PWM com uma determinada frequencia
///
void pwm_init(void){
  // Para os testes é usado o Timer 1 e as saídas dos sinais de PWM para 
  // os motores são configuradas diretamente nos pinos.
  // Deverá ser re-implementada utilizando os PWM's com saídas como CCP1 e CCP2
  // naAtividade 6
  
  // Configuração do Timer 1
  TMR1ON = 1;   // habilita Timer 1
  TMR1CS = 0;   // usa clock interno FOSC/4
  T1OSCEN = 0;  // oscilador LP desligado
  T1CKPS0 = 0;  // prescaler 1:1
  T1CKPS1 = 0;  // prescaler 1:1
  TMR1GE = 0;   // Timer 1 está sempre contando
  TMR1 = 0xffff - 1000; // contagem
  TMR1IE = 0; // inicialmente interrupção está desligada para Timer 1
  PEIE = 1;   // habilita interrupções de periféricos para poder usar Timer 1
  
  // Saída dos sinais de PWM
  TRISC1 = 0; // RC1 é saída para PWM2
  TRISC2 = 0; // RC2 é saída para PWM1
  PWM1 = 0;   // saída do PWM1 é zero inicialmente
  PWM2 = 0;   // saída do PWM2 é zero inicialmente
  
  // Saída dos sinais de direção
  // PWM1_DIR (RB1) [jo:230512] sinais alterados para simulador
  ANS10 = 0;  // RB1 é digital
  TRISB1 = 0; // RB1 é saída
  DIR1 = 0;   // direção do motor 1 (RB1)
  // PWM2_DIR (RB2) [jo:230512] sinais alterados para imulador
  ANS8 = 0;   // RB2 é digital
  TRISB2 = 0; // RB2 é saída
  DIR2 = 0;   // direção do motor 2 (RB2)
}

///
/// Define o duty cycle da saida PWM
/// @param channel - canal do PWM (1: motor 1; 2: motor 2)
/// @param duty_cycle - porcentagem do duty cycle x 10 (valor de 0 a 1000)
///
void pwm_set(int channel, int duty_cycle){
  // Não implementado para os testes  
  // deverá ser implementado pelos alunos na Atividade 6
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
    case 1: // para trás
      DIR1 = 1;
      DIR2 = 1;
      break;
    case 2: // para a esquerda
      DIR1 = 1;
      DIR2 = 0;
      break;
    case 3: // para a direita
      DIR1 = 0;
      DIR2 = 1;
      break;
    default: // para frente
      DIR1 = 0;
      DIR2 = 0;
  } 
}

// Funções somente para teste de hardware, não devem ser implementadas na Atividade 6

// Desliga os motores
void pwm_off(void) {
  TMR1IE = 0; // desliga Timer 1 que para o sinal nas saídas PWM
  PWM1 = 0;   // para motor 1
  PWM2 = 0;   // para motor 2
}

// Liga os motores com duty cycle fixo determinado pelo Timer 1
void pwm_on(void) {
  TMR1IE = 1; // ligando a interrupção do Timer 1 produz sinal com 50% de duty cycle nas duas saídas para os motores
}

// Controle das saídas de PWM para interrupção do Timer 1
void pwm_output_control(void) {
  PWM1 = ~PWM1;  // inverte a saída do PWM1
  PWM2 = ~PWM2;  // inverte a saída do PWM2
  TMR1 = 0xffff - 1000; // recarrega a constante do Timer 1
  TMR1IF = 0;  // limpa o flag de interrupção  
} 

#endif
