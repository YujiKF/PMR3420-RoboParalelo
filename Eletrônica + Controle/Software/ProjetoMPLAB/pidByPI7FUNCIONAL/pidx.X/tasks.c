/* TASKS
 */

#define PID_TASK_ID 0
#define PROTOCOL_TASK_ID 1
#define LED_TASK_ID 2
#define PID_INTERVAL 100
#define PROTOCOL_INTERVAL 1
#define LED_INTERVAL 2000

/* Includes genericos */
#include <xc.h>
#include <stdlib.h>
#include "always.h"
#include "delay.h"

/* Includes especificos */
#include "position_controller.h"
#include "serial.h"
#include "multitasking.h"
#include "motor.h"
#include "protocol.h"
#include "position_sensor.h"
#include "pid.h"
#include "utils.h"

/*================================================
  Definicao dos tasks
 */

/* PID TASK
 */
void pid_task(void) {
  pid_pid();
} // pid_task

/* PROTOCOL TASK
 */
static _PID_MATH value;
static _MESSAGE message;
void protocol_task(void) {

   message = pro_getMessage();
   if (message.messageType != PRO_NO_MESSAGE) {
      value = convertToReal(message.value);
   }
   switch(message.messageType) {
     case PRO_NO_MESSAGE:
        break;
     case PRO_SET_POSITION:
        pid_setPoint(value);
        break;
     case PRO_SET_HOME:
        pos_setCurrentPosition(0);
        pid_clearError();
        break;
     case PRO_SET_PROPORTIONAL_GAIN:
        pid_setProportionalGain(value);
        break;
     case PRO_SET_INTEGRAL_GAIN:
        pid_setIntegralGain(value);
        break;
     case PRO_SET_DERIVATIVE_GAIN:
        pid_setDerivativeGain(value);
        break;  
   } // switch

} // protocol_task

/* LED TASK 
 */
void led_task(void) {
  LED = ~LED;
} // led_task


/*===============================================
 Criacao dos tasks
 */
void initTasks(void) {
   /* init modules */
   pid_init();
   mot_init();
   pos_init();
   pro_init();
   pro_setMyId('a');

   /* create tasks */
   createTask(PID_TASK_ID, &pid_task, PID_INTERVAL);
   createTask(PROTOCOL_TASK_ID, &protocol_task, PROTOCOL_INTERVAL);
   createTask(LED_TASK_ID, &led_task, LED_INTERVAL);
} // criarTasks
