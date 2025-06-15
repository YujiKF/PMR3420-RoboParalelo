#ifndef MOTOR_H
#define MOTOR_H

/*
  Modulo de acionamento do motor CC.
  Utiliza 2 PWM, CCP1 e CCP2.
  A excitacao do motor eh dada por um valor entre
  -1000 (-100,0%) e + 1000 (+100,0%)
*/

#define _EXCITATION int
#define MAX_EXCITATION 1000
#define MIN_EXCITATION -1000

extern void mot_init(void);
extern void mot_setExcitation ( _EXCITATION excitation);    // para uso com driver do PI-7 (usa PWM1 com PWM2)
extern void mot_setExcitationRobot(_EXCITATION excitation); // para testes com o robô de PMR3406 (usa PWM1 com DIR1)

#endif