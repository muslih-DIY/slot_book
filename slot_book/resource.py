
from typing import List,Dict,Any
from datetime import datetime,timedelta,time,date
from .slots import Job,Container,ObdCampaign,Worker
from .settings import PARAMETERS





def init_schedule(schedule_date=None):
    
    if not schedule_date :
        schedule_date = datetime.today().date()

    containers:Dict[str,Container] = get_container_data()

    return {schedule_date:{
        PARAMETERS.START_TIME+i:{
            cid:Worker(PARAMETERS.START_TIME+i,schedule_date,c) for cid,c in containers.items()}
        for i in range(PARAMETERS.MAIN_SLOT_NO)}
        }

def print_schedule(schedule:dict[date | Any, dict[int, dict[str, Worker]]]):
    "print schedule"
    line = '--'*50+'\n'
    for day in schedule:
        line +=f"{day}\t" 
        tab=''       
        for slot in schedule.get(day):
            line +=f"{tab}{slot}\t"
            tab = '\t'
            for cont in schedule[day].get(slot):
                cjobs = schedule[day][slot][cont]
                line +=f"{tab}{cont}:[FREE:{cjobs.available}]\n"
                tab='\t\t\t\t\t\t'
                for cjob in cjobs.jobs:
                    line +=f"{tab}{cjob}\t\n"
                    tab = '\t\t\t\t\t\t'
                
                tab = '\t\t\t\t'
                line+=f"\n{tab}{'--'*30}\n"
            line+='\n'
            tab = '\t\t'                                   
    print(line)                

def load_schedule_data(schedule_date=None,jobs:List[Job]=None):
    "Load the scheduled data from database to schedule variable"
    if not jobs:
        jobs:List[Job] = get_schedule_details(schedule_date)

    
    schedules = init_schedule()
    for job in jobs:        
        # schedules[job.date][job.slot][job.container.id].append(job)
        containerjobs = schedules[job.date][job.slot][job.container.id]
        containerjobs.add_jobs(job,PARAMETERS.SUB_SLOT_NO)

    
    return schedules

def available_slots(schedule_date=None):
    if not schedule_date :
        schedule_date = datetime.today().date()
    schedules = load_schedule_data(schedule_date)           
    slots = schedules.get(schedule_date)
    containers = get_container_data()
    slot_capacity = {}
    for slot,conts in slots.items():
        slot_capacity[slot] = 0
        for cont_id,Cont in conts.items():
            slot_capacity[slot]+=Cont.available

    return slot_capacity

def get_available_slots(schedule:dict):
    free_slot = lambda workers:sum([worker.available for c,worker in workers.items()])
    return {day:{slot:free_slot(workers) for slot,workers in slots.items()} for day,slots in schedule.items() }            
    
def get_campaign(obd_id:str)->ObdCampaign:
    "collect the campaign details from database"
    return get_dummy_Campaign(obd_id=obd_id)

def get_dummy_Campaign(obd_id:str):
    return ObdCampaign(obd_id,5000,0,0,0)

def get_container_data():
    "collect containers informatioon from database"
    return get_dummy_container_data()

def get_dummy_container_data():
    "dummy_data create locally"
    return {'C1':Container('C1',10000),'C2':Container('C2',10000)}
def get_schedule_details(schedule_date=None):
    "collect data from database"
    if not schedule_date :
        schedule_date = datetime.today().date()  
    return get_dummy_schedule_data()

def get_dummy_schedule_data():
    "dummy_data_create locally"
    containers = get_container_data()
    return [
            Job(
                8,
                date.today(),
                time(8,30,0),
                time(9,0,0),
                containers['C1'],get_campaign('OBCMP1'),1,3000),
            Job(
                8,
                date.today(),
                time(8,15,0),
                time(8,30,0),
                containers['C1'],get_campaign('OBCMP2'),1,5000),
            Job(
                10,
                date.today(),
                time(10,0,0),
                time(10,30,0),
                containers['C2'],get_campaign('OBCMP1'),2001,5000)
            ]
