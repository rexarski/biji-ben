import os

domain = "domain.pddl"
bm1 = "blocks"  # blocks domain has no problem 1-3
problem1 = {"problem04.pddl": "4", "problem05.pddl": "5",
            "problem06.pddl": "6", "problem07.pddl": "7",
            "problem08.pddl": "8", "problem09.pddl": "9",
            "problem10.pddl": "10", "problem11.pddl": "11",
            "problem12.pddl": "12", "problem13.pddl": "13"}
bm2 = "miconic"
bm3 = "depot"
# remark: file extension of problem05 in miconic lost a "l" in ".pddl" (typo)
problem23 = {"problem01.pddl": "1", "problem02.pddl": "2",
             "problem03.pddl": "3", "problem04.pddl": "4",
             "problem05.pddl": "5", "problem06.pddl": "6",
             "problem07.pddl": "7", "problem08.pddl": "8",
             "problem09.pddl": "9", "problem10.pddl": "10"}

plangraph = {"-p false -l both": "noplan", "-p true -l fmutex": "fmutex",
             "-p true -l reachable": "reach", "-p true -l both": "both"}
semantics = {"-x parallel": "para", "-x serial": "se"}

# sample command:
# gtimeout 100 python3 -u planner.py benchmarks/miconic/domain.pddl
# benchmarks/miconic/problem05.pddl miconic_temp 1:30:1 -x parallel -l both
# -p false -q ramp | tee log-miconic-1-05

if not os.path.exists("logs"):
    os.makedirs("logs")


def run_commend(bm, problems, plangraph, semantics):
    """ input, a str, a dict, a dict, and a dict."""
    run_these = list()
    combinations = [(prob, pg, s) for prob in problems.keys()
                    for pg in plangraph.keys() for s in semantics.keys()]
    for combo in combinations:
        prob = combo[0]
        pg = combo[1]
        s = combo[2]
        commend = "gtimeout 100 python3 -u planner.py benchmarks/" + bm + \
                  "/domain.pddl benchmarks/" + bm + "/" + prob + " " + bm + \
                  "_temp 15:50:5" + " " + pg + " -q ramp | tee logs/log-" \
                  + bm + "-" + problems[prob] + "-" + plangraph[pg] + "-" +\
                  semantics[s]
        run_these.append(commend)
        os.system(commend)


# execute on different domains separately for progressive output files
run_commend(bm1, problem1, plangraph, semantics)
run_commend(bm2, problem23, plangraph, semantics)
run_commend(bm3, problem23, plangraph, semantics)
