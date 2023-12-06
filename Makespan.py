import pulp as pl

setup_times = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 100, 100, 2, 1, 100],
    [0, 7, 0, 1, 100, 100, 100],
    [0, 6, 5, 0, 3, 6, 100],
    [0, 5, 3, 9, 0, 7, 100],
    [0, 100, 100, 8, 100, 0, 1],
    [0, 3, 100, 100, 7, 9, 0]
]
num_jobs = len(setup_times)
prob = pl.LpProblem("Sequence-Dependent Setup Times")

x = pl.LpVariable.dicts("x", [(i, j) for i in range(num_jobs) for j in range(num_jobs) if i != j], 0, 1, pl.LpBinary)
u = pl.LpVariable.dicts("u", [i for i in range(1, num_jobs)], 0, num_jobs - 1, pl.LpInteger)
prob += pl.lpSum([setup_times[i][j] * x[i, j] for i in range(num_jobs) for j in range(num_jobs) if i != j])

for i in range(num_jobs):
    prob += pl.lpSum([x[i, j] for j in range(num_jobs) if i != j]) == 1

for j in range(num_jobs):
    prob += pl.lpSum([x[i, j] for i in range(num_jobs) if i != j]) == 1

for i in range(num_jobs):
    for j in range(num_jobs):
        if i != j and i and j != 0:
            prob += u[i] - u[j] + 1 <= num_jobs * (1 - x[i, j])

prob.solve()
if pl.LpStatus[prob.status] == "Optimal":
    print("Optimal solution found.")

    start_job = 0
    for i in range(1, num_jobs):
        if pl.value(x[start_job, i]) == 1:
            start_job = i
            break

    sequence = [start_job]

    current_job = start_job
    while True:
        next_job_candidates = [j for j in range(num_jobs) if j != current_job and pl.value(x[current_job, j]) == 1]

        next_job_candidates = [j for j in next_job_candidates if j != start_job]
        if not next_job_candidates:
            break

        next_job = next_job_candidates[0]
        sequence.append(next_job)

        current_job = next_job

    print("Optimal Sequence:", sequence)
else:
    print("Problem couldn't be solved.")
