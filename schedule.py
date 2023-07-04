class Schedule:
    def __init__(self, _alg: str, instance, schedule_list: list):
        self.algorithm = _alg
        self.instance = instance
        self.schedule = schedule_list

    def print_schedule(self):
        for m in self.schedule:
            print(m)


class Bar:
    def __init__(self, job, setup: int):
        self.seq = -job.ID
        self.job = job
        self.machine = job.assignedMch
        self.start = job.start
        self.end = job.end
        self.setup = setup

    def __repr__(self):

        return 'Bar ' + str(self.seq)
