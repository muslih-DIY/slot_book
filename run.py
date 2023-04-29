from slot_book.scheduler import scheduler
from slot_book.resource import get_campaign,init_schedule,print_schedule,available_slots
from slot_book import resource
from datetime import date,time

campaign_a = get_campaign('OBCMP1')
campaign_b = get_campaign('OBCMP2')
campaign_c = get_campaign('OBCMP3')
schedule = scheduler(campaign_a,date.today(),[time(8,0,0)],init_schedule(date.today()))
schedule = scheduler(campaign_b,date.today(),[time(8,0,0)],schedule)
schedule = scheduler(campaign_c,date.today(),[time(8,0,0)],schedule)
schedule = scheduler(get_campaign('OBCMP4'),date.today(),[time(8,0,0)],schedule)
schedule = scheduler(get_campaign('OBCMP5'),date.today(),[time(10,0,0)],schedule)
print(resource.get_available_slots(schedule))

