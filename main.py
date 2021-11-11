from task import TaskA, TaskB
from globals import Globals

if __name__ == '__main__':

    globals = Globals()
    task_A = TaskA()
    task_B = TaskB()
    #task_D = TaskA()

    if globals.task_type[globals.task] == 0:
        task_A.main()

    if globals.task_type[globals.task] == 1:
        task_B.main()
        