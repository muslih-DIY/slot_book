from datetime import datetime,date,time
from dataclasses import dataclass

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
    container:str
    job:str
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