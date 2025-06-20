//#include <htc.h>
#include <xc.h>

void pwm_init (void){

//configuracao pwm
//1 configurar o periodo da pwm escrevendo em PMR2
	PR2=249;			//configurando PMR2 249

//2 Configurar o ciclo de trabalho da PWM escrevendo no registro CCPR1L e nos bits CCP1CON<5:4>
CCPR1L = 0b00000000;
CCP1CON = 0b00001100; //aqui ja esta configurando ccp1 para PWM

//3 Configurar o pin CCP1 como saida (output) clareando o bit TRISC<2>
  TRISC2=0;

// 4 Configurar o valor do TMR2 prescale e habilitar Timer2 escrevendo em T2CON.  
  T2CON = 4; //valore em bit 00000100
// 5 Configure the CCP1 module for PWM operation
//foi feito no passo 2
}
