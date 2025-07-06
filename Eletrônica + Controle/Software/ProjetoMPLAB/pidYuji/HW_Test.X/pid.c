#define DEBUG // comentar se não debug

#include <xc.h>
#include "always.h"
#include "serial.h"
#include "stdio.h"

#include "pid.h"
#include "motor.h"
#include "position_sensor.h"

static _EXCITATION excitation;

static _PID_MATH currentPosition;
static _PID_MATH setPoint;
static _PID_MATH integralError;
static _PID_MATH previousError;
static _PID_MATH kProportional;
static _PID_MATH kIntegral;
static _PID_MATH kDerivative;

_EXCITATION pid_scaleExcitation ( _PID_MATH activation) {
   
   excitation = ( _EXCITATION ) activation;
   if (excitation > 0)
     excitation = 150 + excitation;
   else if (excitation < 0)
     excitation = -150 + excitation;
   if (excitation > MAX_EXCITATION)
     excitation = MAX_EXCITATION;
   if (excitation < MIN_EXCITATION)
     excitation = MIN_EXCITATION;
   return excitation;   
} // scaleExcitation

// Variáveis duplicadas no arquivo original, removidas as redundantes
// static _PID_MATH activation;
// static _PID_MATH error;
// static _EXCITATION excitation; // Esta já está declarada globalmente no topo.

void pid_pid(void) {

#ifdef DEBUG
  RA4 = ~RA4; // usado para saber quanto tempo o controle demora, ver pino 6 do PIC no osciloscópio
#endif
  currentPosition = (_PID_MATH)pos_getCurrentPosition();
  _PID_MATH error = (currentPosition/5) - setPoint; // Definido localmente
  _PID_MATH activation = kProportional * error; // Definido localmente

  excitation = pid_scaleExcitation(activation);
  di(); 
  mot_setExcitation(excitation);
  ei(); 
#ifdef DEBUG
  RA4 = ~RA4;
#endif
} // pid_pid

void pid_setPoint(_PID_MATH position) {
   setPoint = position;
} // pid_setPoint

void pid_setDerivativeGain(_PID_MATH gain) {
  kDerivative = gain;
} // pid_setDerivativeGain

void pid_setIntegralGain(_PID_MATH gain) {
  kIntegral = gain;
} // pid_setIntegralGain

void pid_setProportionalGain(_PID_MATH gain) {
  kProportional = gain;
} // pid_setProportionalGain

void pid_clearError(void) {
  integralError = 0.0f;
  previousError = 0.0f;
} // pid_clearError

void pid_init(void) {
   integralError = 0.0f;
   previousError = 0.0f;
   currentPosition = 0.0f;
   kProportional = 1.0f;
   kDerivative = 0.0f;
   kIntegral = 0.0f;
} // pid_init

// Adicionadas as implementações das funções getter
_PID_MATH pid_getProportionalGain(void) {
  return kProportional;
}

_PID_MATH pid_getIntegralGain(void) {
  return kIntegral;
}

_PID_MATH pid_getDerivativeGain(void) {
  return kDerivative;
}