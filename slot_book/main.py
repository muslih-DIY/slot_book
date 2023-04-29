from slots import Container,ObdCampaign,MarkedJOb
import resource
import settings

if __name__=='__main__':

    print(settings.PARAMETERS.MAIN_SLOT_NO)
    print(settings.PARAMETERS.SUB_SLOT_NO)
    c1 = Container('C1',10000)
    c2 = Container('C2',10000)
    obsc1 = ObdCampaign('OBS1',20000,0,0,0)
    obsc2 = ObdCampaign('OBS2',20000,0,0,0)
    print(c1,c2,c1.call_rate_per_minute)
    print(obsc1,obsc2)
    print(resource.get_campaign('ABC1'))
    # print(resource.initialise_schedules())
    schedule = resource.load_schedule_data()
    resource.print_schedule(schedule)
    print(resource.available_slots())