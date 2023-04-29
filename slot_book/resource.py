
# day 
#  slot1<start-time>
#    Markedslots1 :start-time,end_time<start-time+SUB_SLOT_UNIT>
#    Markedslots1 :start-time,end_time<start-time+SUB_SLOT_UNIT>
#  slot2<start-time+MAIN_SLOT_UNIT>

#  slot3<start-time+(3-1)MAIN_SLOT_UNIT>
from typing import List,Dict,Any
from datetime import datetime,timedelta,time,date
from slots import MarkedJOb,Container,ObdCampaign
from settings import PARAMETERS


def highest_multiple(number,ref):
    "return highest multiplier of reference above number"
    q,mod = divmod(number,ref)
    if mod!=0: return (q+1)*ref
    return number



def init_schedule(schedule_date=None):
    
    if not schedule_date :
        schedule_date = datetime.today().date()

    containers:Dict[str,Container] = get_container_data()

    return {schedule_date:{
        PARAMETERS.START_TIME+i:{
            c:[] for c in containers}
        for i in range(PARAMETERS.MAIN_SLOT_NO)}
        }

def print_schedule(schedule):
    "print schedule"
    line = '--'*50+'\n'
    for day in schedule:
        line +=f"{day}\t" 
        tab=''       
        for slot in schedule.get(day):
            line +=f"{tab}{slot}\t"
            tab = '\t'
            for cont in schedule[day].get(slot):
                line +=f"{tab}{cont}\t"
                tab='\t'
                for job in schedule[day][slot].get(cont):
                    line +=f"{tab}{job}\t\n"
                    tab = '\t\t\t\t\t\t'
                
                tab = '\t\t\t\t'
                line+=f"\n{tab}{'--'*30}\n"
            line+='\n'
            tab = '\t\t'                                   
    print(line)                

def load_schedule_data(schedule_date=None,jobs:List[MarkedJOb]=None):
    "Load the scheduled data from database to schedule variable"
    if not jobs:
        jobs:List[MarkedJOb] = get_schedule_details(schedule_date)

    
    schedules:dict[date | Any, dict[int, dict[str, List[MarkedJOb]]]] = init_schedule()
    for job in jobs:        
        schedules[job.date][job.slot][job.container.id].append(job)
    
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
        for cont_id,jobs in conts.items():
            C = containers.get(cont_id)
            slot_capacity[slot]+=C.call_rate
            sub_slot_call_rate = C.call_rate/PARAMETERS.SUB_SLOT_NO
            for job in jobs:
                slot_capacity[slot]-= highest_multiple(job.effective_size,sub_slot_call_rate)
    return slot_capacity
            

    
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
            MarkedJOb(
                8,
                date.today(),
                time(8,30,0),
                time(9,0,0),
                containers['C1'],get_campaign('OBCMP1'),1,2000),
            MarkedJOb(
                8,
                date.today(),
                time(8,15,0),
                time(8,30,0),
                containers['C1'],get_campaign('OBCMP2'),1,10000),
            MarkedJOb(
                10,
                date.today(),
                time(10,0,0),
                time(10,30,0),
                containers['C2'],get_campaign('OBCMP1'),2001,5000)
            ]
