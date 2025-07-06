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

#endif