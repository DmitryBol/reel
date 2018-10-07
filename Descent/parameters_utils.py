def get_parameters_from_dict(params):
    base_rtp = params['base_rtp']
    rtp = params['rtp']
    sdnew = params['sdnew']
    hitrate = params['hitrate']
    err_base_rtp = params['err_base_rtp']
    err_rtp = params['err_rtp']
    err_sdnew = params['err_sdnew']
    err_hitrate = params['err_hitrate']
    return base_rtp, rtp, sdnew, hitrate, err_base_rtp, err_rtp, err_sdnew, err_hitrate
