from datetime import datetime,date,time
from dataclasses import dataclass,field



class PARAMETERS:
        MARGIN_BETWEEN = 3 # minutes
        START_TIME = 8  # 24 hr scale
        END_TIME = 20   # 24 hr scale
        MAIN_SLOT_UNIT = 1 # hr
        SUB_SLOT_UNIT = 1/4  # hr
        MAIN_SLOT_NO = int((END_TIME - START_TIME)/MAIN_SLOT_UNIT)
        SUB_SLOT_NO  = int(MAIN_SLOT_UNIT/SUB_SLOT_UNIT )
        RETRY_BOOST = 70/100
        SURVEY_BOOST = 30/100



@dataclass
class Container:
    id:str  
    call_rate:int # one slot capacity of container
    sub_slot:int = 1 # division of slot
    def __post_init__(self):
        
        self.call_rate_per_minute = int(self.call_rate/60)
        self.sub_slot_call_rate = int(self.call_rate/self.sub_slot)

        


@dataclass
class ObdCampaign:
    id:str
    size:int
    job_type:int     = 0  # service campaign,commercial
    service_type:int = 0 # simple announcement , survey
    retry_count:int  = 0
    answering_perc:int  = 30/100
    survey_drop:int = 30/100 # expecting 30% drop in the call speed

    def __post_init__(self):

        self.set_ratios()
        
    def set_ratios(self):

        """
            r = expected unanswered_percentage
            
            sd = expected reduction in capacity due to survey
            
            enhance_size = [[(1-r)^n]/(1-r)]*1/(1-sd)

            diminish_capacity = [(1-r)/(1-r)^n]*(1-sd)

        """
        r = 1-self.answering_perc
        sd = self.survey_drop if self.service_type!=0 else 0
        n = self.retry_count+1
        print("n :",n)
        self.capacity_diminish_ratio = (((1-r)**n)/(1-r))/(1-sd)
        self.size_enhancement_ratio = ((1-r)/(1-r)**n)*(1-sd)
        

@dataclass
class Job:
    slot:int
    date:date
    start_time:time
    end_time:time
    container:Container
    Campaigns:ObdCampaign
    start_record:int
    end_record:int
    
    @property
    def size(self):
        return self.end_record-self.start_record+1
    
    @property
    def effective_size(self):
        return self.size


    def __str__(self) -> str:
        return f"{self.Campaigns.id}({self.effective_size})@{self.start_time}-{self.end_time}"

    def __repr__(self) -> str:
        return self.__str__()

def highest_multiple(number:int,ref:int):
    "return highest multiplier of reference above number"
    q,mod = divmod(number,ref)
    if mod!=0: return (q+1)*ref
    return number


    
@dataclass
class Worker:
    slot:int
    date:int
    cont:Container
    jobs:list[Job] = field(default_factory=list)
    available:int = 0
    lost:int = 0
    end_time:time = field(init=False)
    
    def __post_init__(self):
        
        self.available = self.cont.call_rate
        self.end_time = time(self.slot,0,0)
        if self.jobs:self.end_time = self.last_job.end_time   

    def add_jobs(self,job:Job):
        self.jobs.append(job)
        self.available -= int(highest_multiple(job.effective_size,self.cont.call_rate/self.cont.sub_slot))
        self.end_time = job.end_time

    @property
    def last_job(self):
        return max(self.jobs,key=lambda x:x.end_time)

    
