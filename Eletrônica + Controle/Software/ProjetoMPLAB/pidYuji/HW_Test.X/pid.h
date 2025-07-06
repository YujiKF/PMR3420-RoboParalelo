#ifndef PID_H
#define PID_H

#define _PID_MATH float

extern void pid_init(void);
extern void pid_clearError(void);
extern void pid_setProportionalGain ( _PID_MATH gain);
extern void pid_setIntegralGain ( _PID_MATH gain);
extern void pid_setDerivativeGain ( _PID_MATH gain);
extern void pid_setPoint ( _PID_MATH position);
extern void pid_pid(void);

// Adicionadas as declarações das funções getter
extern _PID_MATH pid_getProportionalGain(void);
extern _PID_MATH pid_getIntegralGain(void);
extern _PID_MATH pid_getDerivativeGain(void);

#endif