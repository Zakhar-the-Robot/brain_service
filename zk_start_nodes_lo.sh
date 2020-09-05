#!/bin/bash

#### interfaces
rosrun zakhar_i2c i2c.py &

#### hardware
rosrun zakhar_i2c_devices face_platform.py &
rosrun zakhar_i2c_devices moving_platform.py &
rosrun zakhar_i2c_devices sensor_platform.py &

# #### basic mind structures
rosrun zakhar_mind concept_translator.py &
rosrun zakhar_mind sensor_interpreter.py &

# #### instincts
# rosrun zakhar_mind instinct_bird_panic.py &

# #### egos (better to have only one ego on)
# # rosrun zakhar_mind ego_shivering_robot.py &
# rosrun zakhar_mind ego_small_researcher.py &

while :
do
	echo "."
	sleep 5
done
