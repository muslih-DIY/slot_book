from datetime import datetime,date,time
from dataclasses import dataclass,field

@dataclass
class Container:
    id:str  
    call_rate:int # one slot capacity of container

    def __post_init__(self):
        
        self.call_rate_per_minute = int(self.call_rate/60)
        


@dataclass
class ObdCampaign:
    id:str
    size:int
    job_type:int # service campaign,commercial 
    service_type:int # simple announcement , survey
    retry_count:int



@dataclass
class MarkedJOb:
    slot:int
    date:date
    start_time:time
    end_time:time
    container:Container
    job:ObdCampaign
    start_record:int
    end_record:int
    
    @property
    def size(self):
        return self.end_record-self.start_record+1
    
    @property
    def effective_size(self):
        return self.size


    def __str__(self) -> str:
        return f"{self.job.id}({self.effective_size})@{self.start_time}-{self.end_time}"

    def __repr__(self) -> str:
        return self.__str__()

def highest_multiple(number:int,ref:int):
    "return highest multiplier of reference above number"
    q,mod = divmod(number,ref)
    if mod!=0: return (q+1)*ref
    return number


    
@dataclass
class Containerjob:
    cont:Container
    jobs:list[MarkedJOb] = field(default_factory=list)
    available:int = 0
    
    def __post_init__(self):
        
        self.available = self.cont.call_rate
    

    def add_jobs(self,job:MarkedJOb,no_sub_slot:int):
        self.jobs.append(job)
        self.available -= int(highest_multiple(job.effective_size,self.cont.call_rate/no_sub_slot))



    
