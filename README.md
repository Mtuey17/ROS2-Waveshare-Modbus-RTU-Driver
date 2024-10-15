ROS2 Drivers Made For

Modbus RTU 32-Ch: https://www.waveshare.com/modbus-rtu-relay-32ch.htm

Industrial 8-Ch Analog Acquisition Module: https://www.waveshare.com/modbus-rtu-analog-input-8ch.htm

--------------------------------------------
**Running for the first time**

cd ROS2_MODBUS_CARDS

colcon build

source install/setup.bash

ros2 run 32channel_relay 32CH_relay

ros2 run analog_input_8ch 8CH_Status

--------------------------------------------
**use RQT to test the 32Ch relay driver**

navigate to: plugins->topics-message publisher

Topic:

/Relay_Bank_32





















