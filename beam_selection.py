def beam_selection(atl, beamNum):
    #flag_values: 0, 1, 2; flag_meanings : backward forward transition
    #
    #beamNum = 1: strong
    #beamNum = 2: weak
    #beamNum = 3: strong
    #beamNum = 4: weak
    #beamNum = 5: strong
    #beamNum = 6: weak
    orientation_flag = atl['orbit_info']['sc_orient'][:]

    if (orientation_flag==0):
        print('Backward orientation')
        beamStrs=['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']

    elif (orientation_flag==1):
        print('Forward orientation')
        beamStrs=['gt3r', 'gt3l', 'gt2r', 'gt2l', 'gt1r', 'gt1l']

    elif (orientation_flag==2):
        print('Transitioning, do not use for science!')

    gt = beamStrs[beamNum-1]
    return gt

