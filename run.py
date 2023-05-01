from slot_book.scheduler import scheduler
from slot_book.resource import get_campaign,init_schedule,print_schedule,available_slots
from slot_book import resource
from datetime import date,time

campaign_a = get_campaign('OBCMP1') #5000 campaign
campaign_b = get_campaign('OBCMP2')
campaign_c = get_campaign('OBCMP3')
campaign_a.size = 32000
campaign_a.retry_count=1
campaign_a.set_ratios()
print(campaign_a.capacity_diminish_ratio,campaign_a.size_enhancement_ratio)
schedule = scheduler(campaign_a,date.today(),[time(8,0,0),time(9,0,0),time(12,0,0),time(13,0,0)],init_schedule(date.today()))
# schedule = scheduler(campaign_b,date.today(),[time(11,0,0)],schedule)
# schedule = scheduler(campaign_c,date.today(),[time(12,0,0)],schedule)
# schedule = scheduler(get_campaign('OBCMP4'),date.today(),[time(9,0,0)],schedule)
# schedule = scheduler(get_campaign('OBCMP5'),date.today(),[time(9,0,0),time(11,0,0)],schedule)
print(resource.get_available_slots(schedule))
print_schedule(schedule)