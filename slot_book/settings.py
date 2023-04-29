""" __settings__
"""

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
