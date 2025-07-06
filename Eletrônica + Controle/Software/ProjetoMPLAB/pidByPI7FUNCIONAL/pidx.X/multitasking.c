/*
  MULTITASKING IMPLEMENTATION

*/
#include "multitasking.h"

#define NUM_TASKS 3

typedef struct {
   Task taskFunction;
   int   scheduleInterval;
   long   lastActivation;
} TaskControlBlock;

static TaskControlBlock tsk_tasks[NUM_TASKS];
static Task tsk_task;
static long tsk_elapsedTime;

void createTask(int taskID, Task t, int scheduleInterval) {
    tsk_tasks[taskID].taskFunction = t;
    tsk_tasks[taskID].scheduleInterval = scheduleInterval;
    tsk_tasks[taskID].lastActivation = 0;
}  // createTask

void executeTasks(void) {
    unsigned char i;

    for (i=0; i < NUM_TASKS; i++) {
       tsk_elapsedTime = tsk_timeStamp - tsk_tasks[i].lastActivation;
       if (tsk_elapsedTime > tsk_tasks[i].scheduleInterval) {
          tsk_task = tsk_tasks[i].taskFunction;
          tsk_task();
          tsk_tasks[i].lastActivation = tsk_timeStamp;
       }
    } // for each task
} // executeTasks

