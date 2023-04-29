from slot_book.scheduler import simple_schedule
from slot_book.resource import get_campaign,init_schedule,print_schedule
from datetime import date,time

campaign_a = get_campaign('OBCMP1')
schedule = simple_schedule(campaign_a,date.today(),[time(8,0,0)],init_schedule(date.today()))
print_schedule(schedule)