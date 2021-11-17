# from task import TaskA, TaskB, TaskD
from globals import Globals
from task_a import TaskA
from task_b import TaskB
from task_d import TaskD
from task import TaskTest
# from task_e import TaskE

if __name__ == '__main__':

    globals = Globals()
    task_A = TaskA()
    task_B = TaskB()
    task_D = TaskD()
    taskTest = TaskTest()

    if globals.task_type[globals.task] == 0:
        task_A.main()

    if globals.task_type[globals.task] == 1:
        task_B.main()

    if globals.task_type[globals.task] == 2:
        task_D.main_task_D()

    if globals.task_type[globals.task] == 3:
        taskTest.main()
        