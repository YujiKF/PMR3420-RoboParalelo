#ifndef MULTITASKING_H
#define MULTITASKING_H

volatile long tsk_timeStamp;

/* define Task como uma funcao void */
typedef void (*Task)(void);

/* interface publica */
extern void initTasks(void);
extern void createTask(int taskID, Task t, int scheduleInterval);
extern void executeTasks(void);

/* interface voltada ao uso pela rotina de interrupcao */
extern void updateTasksTimers(void);


#endif