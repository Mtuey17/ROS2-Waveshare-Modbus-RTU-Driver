import rclpy
from rclpy.node import Node
from textwrap import wrap
from modbus_msgs.msg import RelayBank32CH
import crcmod
from crcmod.predefined import *
import serial


class ThirtyTwoRelay(Node):

    def __init__(self):
        super().__init__('thirty_two_relay')
        self.subscription = self.create_subscription(
            RelayBank32CH, 
            '/Relay_Bank_32', 
            self.Analog32ChCallback, 
            1)
        
        self.ser = serial.Serial( 
            port= '/dev/serial/by-id/usb-WCH.CN_USB_Quad_Serial_BC622AABCD-if02', #change to your port!
            baudrate= 9600,
            timeout =0.1       
            )
        
        self.First_byte_relays = 0
        self.Second_byte_relays= 0
        self.Third_byte_relays= 0
        self.Fourth_byte_relays= 0
        self.crc_func = crcmod.predefined.mkCrcFun('modbus')

        
    def Analog32ChCallback(self, msg):

        #calculating first byte of relays 
        self.First_byte_relays = (int(msg.relay1)*1) #relay1
        self.First_byte_relays += (int(msg.relay2)*2) #relay2
        self.First_byte_relays += (int(msg.relay3)*4) #relay3
        self.First_byte_relays += (int(msg.relay4)*8)#relay4
        self.First_byte_relays += (int(msg.relay5)*16)#relay5
        self.First_byte_relays += (int(msg.relay6)*32)#relay6
        self.First_byte_relays += (int(msg.relay7)*64)#relay7
        self.First_byte_relays += (int(msg.relay8)*128)#relay8


        #calculating second byte of relays 
        self.Second_byte_relays = (int(msg.relay9)*1) #relay9
        self.Second_byte_relays += (int(msg.relay10)*2) #relay10
        self.Second_byte_relays += (int(msg.relay11)*4) #relay11
        self.Second_byte_relays += (int(msg.relay12)*8)#relay12
        self.Second_byte_relays += (int(msg.relay13)*16)#relay13
        self.Second_byte_relays += (int(msg.relay14)*32)#relay14
        self.Second_byte_relays += (int(msg.relay15)*64)#relay15
        self.Second_byte_relays += (int(msg.relay16)*128)#relay16


        #calculating third byte of relays 
        self.Third_byte_relays = (int(msg.relay17)*1) #relay17
        self.Third_byte_relays += (int(msg.relay18)*2) #relay18
        self.Third_byte_relays += (int(msg.relay19)*4) #relay19
        self.Third_byte_relays += (int(msg.relay20)*8)#relay20
        self.Third_byte_relays += (int(msg.relay21)*16)#relay21
        self.Third_byte_relays += (int(msg.relay22)*32)#relay22
        self.Third_byte_relays += (int(msg.relay23)*64)#relay23
        self.Third_byte_relays += (int(msg.relay24)*128)#relay24


        #calculating fourth byte of relays 
        self.Fourth_byte_relays = (int(msg.relay25)*1) #relay25
        self.Fourth_byte_relays += (int(msg.relay26)*2) #relay26
        self.Fourth_byte_relays += (int(msg.relay27)*4) #relay27
        self.Fourth_byte_relays += (int(msg.relay28)*8)#relay28
        self.Fourth_byte_relays += (int(msg.relay29)*16)#relay29
        self.Fourth_byte_relays += (int(msg.relay30)*32)#relay30
        self.Fourth_byte_relays += (int(msg.relay31)*64)#relay31
        self.Fourth_byte_relays += (int(msg.relay32)*128)#relay32

        cmd = [0x01, 0x0F, 0x00, 0x00, 0x00, 0x20, 0x04, 0, 0, 0, 0]
        cmd[7] = self.Fourth_byte_relays
        cmd[8] = self.Third_byte_relays
        cmd[9] = self.Second_byte_relays
        cmd[10]= self.First_byte_relays
        CRC = self.crc_func(bytes(cmd))
        CRC = CRC.to_bytes(2,'little')
        self.ser.write(cmd)
        self.ser.write(CRC)
      
        self.get_logger().info('Relays updated!')



def main(args=None):
    rclpy.init(args=args)

    thirty_two_relay = ThirtyTwoRelay()

    rclpy.spin(thirty_two_relay)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    thirty_two_relay.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()






