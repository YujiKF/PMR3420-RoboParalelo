# 1 "multitasking.c"
# 1 "<built-in>" 1
# 1 "<built-in>" 3
# 285 "<built-in>" 3
# 1 "<command line>" 1
# 1 "<built-in>" 2
# 1 "C:\\Program Files\\Microchip\\xc8\\v3.00\\pic\\include/language_support.h" 1 3
# 2 "<built-in>" 2
# 1 "multitasking.c" 2




# 1 "./multitasking.h" 1



volatile long tsk_timeStamp;


typedef void (*Task)(void);


extern void initTasks(void);
extern void createTask(int taskID, Task t, int scheduleInterval);
extern void executeTasks(void);


extern void updateTasksTimers(void);
# 6 "multitasking.c" 2



typedef struct {
   Task taskFunction;
   int scheduleInterval;
   long lastActivation;
} TaskControlBlock;

static TaskControlBlock tsk_tasks[3];
static Task tsk_task;
static long tsk_elapsedTime;

void createTask(int taskID, Task t, int scheduleInterval) {
    tsk_tasks[taskID].taskFunction = t;
    tsk_tasks[taskID].scheduleInterval = scheduleInterval;
    tsk_tasks[taskID].lastActivation = 0;
}

void executeTasks(void) {
    unsigned char i;

    for (i=0; i < 3; i++) {
       tsk_elapsedTime = tsk_timeStamp - tsk_tasks[i].lastActivation;
       if (tsk_elapsedTime > tsk_tasks[i].scheduleInterval) {
          tsk_task = tsk_tasks[i].taskFunction;
          tsk_task();
          tsk_tasks[i].lastActivation = tsk_timeStamp;
       }
    }
}
