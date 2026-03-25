import numpy as np

def build_input(area, bedroom, bathroom, month, year,
                loc_code, prop_code, slug_code, prov_code):

    return np.array([[
        area,
        np.log1p(area),
        bedroom,
        bathroom,
        bedroom/area if area>0 else 0,
        bathroom/area if area>0 else 0,
        month,
        year,
        loc_code,
        prop_code,
        slug_code,
        prov_code,
        1 if month in [3,4,5,9,10] else 0
    ]])