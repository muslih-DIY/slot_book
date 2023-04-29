from datetime import datetime,time,date
from typing import List,Dict
from collections import OrderedDict
from .slots import ObdCampaign,Containerjob,MarkedJOb
from .resource import load_schedule_data

def Choose_Worker(containerjobs:List[Containerjob]):
    "return The Containerjob with maximum capacity"
    return max(containerjobs,key=lambda worker:worker.available)


def simple_schedule(
        job:ObdCampaign,
        schedule_date:date,
        schedule_time:list[time],scheduled_data:dict=None):
    """
    It will take the obd job deatils and the time and schedule the job in various slot(container and time space)

    """
    schedules = scheduled_data
    if not scheduled_data:
        schedules = load_schedule_data(schedule_date)

    slots = schedules.get(schedule_date)

    for t in schedule_time:
        Workers = slots[t.hour].values()
        ContWorker = Choose_Worker(Workers)
        
        ContWorker.add_jobs(MarkedJOb(t.hour,schedule_date,))

    return schedules