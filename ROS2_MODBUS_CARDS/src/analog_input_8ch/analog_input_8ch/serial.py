import rclpy
from rclpy.node import Node
from textwrap import wrap
from modbus_msgs.msg import AnalogInput8Ch
import serial


class Analog_IP_EightCH(Node):

    def __init__(self):
        super().__init__('Analog_EightCH')
      
        self.ser = serial.Serial( 
            port= '/dev/serial/by-id/usb-WCH.CN_USB_Quad_Serial_BC622AABCD-if00', #change to your port
            baudrate= 9600,
            parity= serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout =0.1       
            )

        self.publisher_Channels= self.create_publisher(AnalogInput8Ch, 'Analog_Input_Card', 1)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.serial = 0

    
    def timer_callback(self):
      
        fData = AnalogInput8Ch()
        try: 
            message = [0x01,0x04,0x00,0x00,0x00,0x08,0xF1,0xCC]
            self.ser.write(message)
            data = self.ser.read(42).hex()
            data= (data.split('410',1))

            try:
                data=data[1]
                Channel_data= wrap(data,4)
                fData.ai1= (int((Channel_data[0]), 16))/1000 
                fData.ai2= (int((Channel_data[1]), 16))/1000 
                fData.ai3= (int((Channel_data[2]), 16))/1000 
                fData.ai4= (int((Channel_data[3]), 16))/1000 
                fData.ai5= (int((Channel_data[4]), 16))/1000 
                fData.ai6= (int((Channel_data[5]), 16))/1000 
                fData.ai7= (int((Channel_data[6]), 16))/1000 
                fData.ai8= (int((Channel_data[7]), 16))/1000 
                self.publisher_Channels.publish(fData)
                self.get_logger().info('sucessfuly read from card')

            except: 
                 self.get_logger().info('device returning unexpected data')

        except:
            self.get_logger().info('could not read from device')


def main(args=None):
    rclpy.init(args=args)
    Analog_EightCH = Analog_IP_EightCH()
    rclpy.spin(Analog_EightCH)
    Analog_EightCH.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()




