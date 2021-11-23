from globals import Globals
from task_a import TaskA
from task_b import TaskB
from task_d import TaskD

if __name__ == '__main__':

    globals = Globals()
    task_A = TaskA()
    task_B = TaskB()
    task_D = TaskD()

    if globals.getTask() == 0:
        task_A.main()

    if globals.getTask() == 1:
        task_B.main()

    if globals.getTask() == 2:
        task_D.main()
        