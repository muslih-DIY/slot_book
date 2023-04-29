from .resource import ObdJobs


def simple_schedule(
        job:ObdJobs,
        time:list=None,
        containers:list=None,
        schedules:list=None):
    """
    It will take the obd job deatils and the time and schedule the job in various slot(container and time space)

    """
    return schedules