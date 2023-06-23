# if user doesn't press the force sensors and there is no movement for 10 seconds
def has_paused(pauses_list, frc_list1, frc_list2):
    zeros = True

    for x in pauses_list:
        if x != 0:
            zeros = False
    for x in frc_list1:
        if x != 0:
            zeros = False
    for x in frc_list2:
        if x != 0:
            zeros = False

    return zeros


def has_stressed(force_sensor_list, avg_frc):
    counter = 1
    last_val = 0
    for x in force_sensor_list:
        if counter == 3 and last_val >= avg_frc:
            return True
        if x >= last_val and x >= avg_frc:
            counter += 1
        last_val = x
    return False

# print(has_stressed([1,2,3,4,5,6,7,7,7,9,5,10], 7))
