from module import *
from milp import *
from cp import *
import heuristic


if __name__ == '__main__':
    test_instance = generate_prob(numJob=3, numMch=2)
    schedule = heuristic.scheduling(test_instance, 'SPT')
    schedule.print_schedule()
    draw_gantt_chart(schedule, test_instance)

    schedule = milp_scheduling(test_instance)
    #schedule.print_schedule()
    #draw_gantt_chart(schedule, test_instance)


    schedule = cp_scheduling(test_instance)
    schedule = milp_scheduling_ortools(test_instance)
    schedule = cp_scheduling_ortools(test_instance)
