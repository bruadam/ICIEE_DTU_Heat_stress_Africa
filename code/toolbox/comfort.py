# Define a functions that calculates the apparent temperature
def apparent_temperature(T_a, e, ws=0.0):
    return T_a + 0.33 * e - 0.7 * ws - 4.0

def absolute_humidity(T_a, rh):
    return rh/100 * 6.105 * np.exp(17.27 * T_a / (237.7 + T_a))