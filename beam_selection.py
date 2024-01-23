def beam_selection(atl):
    #flag_values: 0, 1, 2; flag_meanings : backward forward transition
    orientation_flag = atl['orbit_info']['sc_orient'][:]

    if (orientation_flag==0):
        print('Backward orientation')
        beamStrs=['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']

    elif (orientation_flag==1):
        print('Forward orientation')
        beamStrs=['gt3r', 'gt3l', 'gt2r', 'gt2l', 'gt1r', 'gt1l']

    elif (orientation_flag==2):
        print('Transitioning, do not use for science!')

    beamStr=beamStrs[beamNum-1]
    return beamStr

