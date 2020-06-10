""" File name:   Logistics-LNS.py
    Author:      Rui Qiu
    Date:        April 26, 2018
    Description: This file should implement a Large Neighborhood Search (LNS)
                 for the Logistics Problem for Q4 of Assignment 2.
                 See the assignment notes for a description of its contents.
"""

import argparse
import random
import time
from subprocess import Popen, PIPE, STDOUT

# Complete the file with your LNS solution

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_filename', help='problem file')
    parser.add_argument('start_solution_filename',
                        help='file describing the solution to improve')
    args = parser.parse_args()
    start_solution_filename = args.start_solution_filename
    problem_filename = args.problem_filename

    # ================== READ GIVEN SOLUTION FOR META DATA ==================
    s0 = open(start_solution_filename, 'r')  # read starting solution as s0
    start_header = s0.readlines()[0].strip('\n').replace(' ', '').split(',')
    T = int(start_header[0])
    C = int(start_header[1])
    # the solution we need to update
    best_solution = 'best-solution-{0}-{1}.csv'.format(T, C)
    my_other_file = 'Logistics-Q4.mzn'

    # ====================== STOPPING CONDITION OF LNS ======================
    # A timer. But I also keep track of iteration numbers, just in case we
    # want to have a visual indication.
    start_time = time.time()
    runtime = 0
    iteration = 1

    if T < 20:
        lapse = 60
    else:
        lapse = 120

    # ======================== LOOP OF LNS ========================
    while runtime <= lapse:
        if iteration == 1:
            # read the start_solution_file
            sfile = open(start_solution_filename, 'r')
        else:
            # starting from the 2nd iter, no more read start_solution_file;
            # instead, we read the best solution so far
            sfile = open(best_solution, 'r')

        solution = sfile.readlines()
        meta = solution[0].strip('\n').replace(' ', '').split(',')

        # Although printing slows down the algorithm a little bit,
        # it assures me to see it is working,
        # For the first three instances, print every 10 iterations;
        # while for the last one, print every iter.
        if T < 20:
            if iteration % 10 == 0:
                print('iter={0}, cost={1}, '
                      'time={2}'.format(iteration, meta[2], round(runtime, 3)))
        else:
            print('iter={0}, cost={1}, time={2}'.format(iteration, meta[2],
                                                        round(runtime, 3)))

        # write into keep.dzn
        pfile = open(problem_filename, 'r').readlines()
        keep = open('keep.dzn', 'w')
        for line in pfile:
            keep.write(line)
        keep.write('a_seq = array2d(trucks,1..5*C,[')

        # ====================== SIMULATED ANNEALING ======================
        # Create a list of T lists, and each of them has an amount of 5*C
        # zeros, which is consistent with our previous design.
        phases = [([0] * 5*C) for i in range(T)]

        ##################################
        # ACTION 1: DESTROY time_step_id #
        ##################################

        for i in range(T):
            for j in range(C):
                phases[i][5*j] = i+1      # record truck_id
                phases[i][5*j+2] = j+1    # record customer_id
                if T < 20:
                    phases[i][5*j+1] = '_'
                # Large instance like 21-8, only forget half of the
                # information so as to speed up
                elif random.random() < 0.5:
                    phases[i][5*j+1] = '_'

        #######################################
        # ACTION 2: DESTROY order information #
        #######################################

        for line in solution[1:]:
            line = line.strip('\n').replace(' ', '').split(',')
            t = int(line[0])
            c = int(line[2])
            # in order to destroy order number, have to destroy time_step_id
            # as well
            phases[t-1][5*c-4] = '_'
            if random.random() > 0.5:
                # record chilled order number, destroy ambient order number
                phases[t-1][5*c-2] = int(line[3])
                phases[t-1][5*c-1] = '_'
            else:
                # destroy chilled order number, record ambient order number
                phases[t-1][5*c-2] = '_'
                phases[t-1][5*c-1] = int(line[4])

        ########################################
        # ACTION 3: DESTROY random information #
        ########################################

        for i in range(20):
            phases[random.randint(0, T-1)][random.randint(0, 5*C-1)] = '_'

        # write the destroyed into keep.dzn
        keep_line = str(phases).replace('[', '').replace(']', '')\
            .replace("'", '')  # transform list to string form
        keep.write(keep_line)
        keep.write("\n]);")   # for ".dzn" format
        keep.close()

        # execute shell
        Popen("minizinc {0} keep.dzn --soln-sep \"\" --search-complete-msg"
              " \"\" > {1}".format(my_other_file, best_solution),
              shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT).stdout.read()

        iteration = iteration + 1
        runtime = time.time()-start_time
