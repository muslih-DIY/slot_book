from datetime import datetime,time,date,timedelta
from typing import List,Dict
from collections import OrderedDict
from .slots import ObdCampaign,Worker,Job,highest_multiple
from .resource import load_schedule_data
from .settings import PARAMETERS

def Choose_Worker(containerjobs:List[Worker]):
    "return The Worker with maximum capacity"
    return max(containerjobs,key=lambda worker:worker.available)


class Schedule_Algo:

    @classmethod
    def vertical_fill(cls,Workers:List[Worker],Campaign:ObdCampaign,marked_task:int=0):
        if marked_task>=Campaign.size:
            # all the task(call) are marked
            return marked_task
        worker = Choose_Worker(Workers) # choose larger capacity worker(container)
        available_cap = int(worker.available*Campaign.capacity_diminish_ratio)
        sub_slot_cap = int(worker.cont.sub_slot_call_rate*Campaign.capacity_diminish_ratio)
        print(available_cap,sub_slot_cap)
        if available_cap < sub_slot_cap:
            #The Slot capacity is filled collect next slot
            return marked_task
        start_record = marked_task+1
        tasks = available_cap
        balance_task = Campaign.size - marked_task
        if balance_task<available_cap:
            tasks = balance_task
        end_record =  start_record+tasks-1            
        dt = timedelta(minutes=int(highest_multiple(tasks,sub_slot_cap)/sub_slot_cap)*60*PARAMETERS.SUB_SLOT_UNIT)
        
        end_time = (datetime.combine(worker.date,worker.end_time)+dt).time()
        
        worker.add_jobs(Job(worker.slot,worker.date,worker.end_time,end_time,worker.cont,Campaign,start_record,end_record))
        marked_task +=tasks
        return cls.vertical_fill(Workers,Campaign,marked_task)

                

def scheduler(
        Campaign:ObdCampaign,
        schedule_date:date,
        schedule_time:list[time],scheduled_data:dict=None):
    """
    It will take the obd Campaign deatils and the time and schedule the Campaign in various slot(container and time space)

    """
    schedules = scheduled_data
    if not scheduled_data:
        schedules = load_schedule_data(schedule_date)

    slots = schedules.get(schedule_date)
    marked_task = 0
    for t in schedule_time:
        workers = slots[t.hour].values()
        marked_task = Schedule_Algo.vertical_fill(workers,Campaign,marked_task)
        if marked_task>=Campaign.size:
            break
    if marked_task<Campaign.size:
        raise ValueError("Campaign scheduling is not finished panding ",Campaign.size-marked_task)
    return schedules