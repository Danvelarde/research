# Virtual Serial Server node
from time import sleep
import rclpy
from rclpy.node import Node
import serial
from std_msgs.msg import String


class VirtualSerialFlashlightServer(Node):
	def __init__(self):
		super().__init__('virtual_serial_flashlight_server')
		#Default Value declarations of ros2 params:
		self.declare_parameters(
		namespace='',
		parameters=[
			('transmitting_device', '/dev/ttyS0'), #device we are trasmitting messages to
		    ('recieving_device', '/dev/ttyS3'), #device we are recieving messages from
		  ('LED_on', 'o'),
		  ('LED_off','f'),
		  
		
		)
		)
		self.turn_on = self.get_param_str('LED_on')
		self.turn_off = self.get_param_str('LED_off')
		self.serial_send = serial.Serial(self.get_param_str('transmitting_device'),
				9600, #Note: Baud Rate must be the same in the arduino program, otherwise signal is not recieved!
				timeout=.1)
		self.serial_recieve = serial.Serial(self.get_param_str('recieving_device'),
				9600, #Note: Baud Rate must be the same in the arduino program, otherwise signal is not recieved!
				timeout=.1)
		
		self.subscriber = self.create_subscription(String, 
                                              self.get_param_str('LED_instructions_topic'), 
                                              self.serial_listener_callback, 
                                              10)
		self.subscriber # prevent unused variable warning
	def get_param_float(self, name):
		try:
			return float(self.get_parameter(name).get_parameter_value().double_value)
		except:
			pass
	def get_param_str(self, name):
		try:
			return self.get_parameter(name).get_parameter_value().string_value
		except:
			pass
	def send_cmd(self, cmd):
		print("Sending: " + cmd)
		self.serial_send.write(bytes(cmd,'utf-8'))
	def recieve_cmd(self):
		try:
			#try normal way of recieving data
			sleep(.01) #sleep to allow time for serial_data to arrive. Otherwise this might return nothing
			line = self.serial_recieve.readline().decode('utf-8').rstrip()
		except:
			#if normal way doesn't work, try getting binary representation to see what went wrong
			line = str(self.serial_recieve.readline())
		print("Recieved: " + line)
	def serial_listener_callback(self, msg):
		#NOTE: 
		# For some reason, arduino sends back null byte (0b'' or Oxff) back after the first call to ser.write
		# If the statement in "try" executes when this happens, it causes this error which crashes the program:
		# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
		# To prevent this, I added the try-except blocks to prevent the program from crashing
		# If a null byte is sent, "except" is called which prevents the program from crashing
		"""ON"""
		if msg.data == self.turn_on:
			self.send_cmd(self.LED_on)
			self.recieve_cmd()
		"""OFF"""
		if msg.data == self.turn_off:
			self.send_cmd(self.LED_off)
			self.recieve_cmd()
		

def main(args=None):
	rclpy.init(args=args)
	virtual_serial_flashlight_server = VirtualSerialFlashlightServer()
	rclpy.spin(virtual_serial_flashlight_server)

if __name__ == '__main__':
	main()
