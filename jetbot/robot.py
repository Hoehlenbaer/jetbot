import time
import traitlets
from traitlets.config.configurable import SingletonConfigurable
from Adafruit_MotorHAT import Adafruit_MotorHAT
from .motor import Motor


class Robot(SingletonConfigurable):
    
    left_motor = traitlets.Instance(Motor)
    right_motor = traitlets.Instance(Motor)
    # 2021-04-07: add vertical motor & bln
    vertical_motor = traitlets.Instance(Motor)
    bln = traitlets.Instance(Motor)
    # end edit

    # config
    i2c_bus = traitlets.Integer(default_value=1).tag(config=True)
    left_motor_channel = traitlets.Integer(default_value=1).tag(config=True)
    left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    right_motor_channel = traitlets.Integer(default_value=2).tag(config=True)
    right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    # 2021-04-07: add vertical motor & bln
    vertical_motor_channel = traitlets.Integer(default_value=3).tag(config=True)
    vertical_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    bln_channel = traitlets.Integer(default_value=4).tag(config=True)
    bln_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    # end edit
    
    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        self.motor_driver = Adafruit_MotorHAT(i2c_bus=self.i2c_bus)
        self.left_motor = Motor(self.motor_driver, channel=self.left_motor_channel, alpha=self.left_motor_alpha)
        self.right_motor = Motor(self.motor_driver, channel=self.right_motor_channel, alpha=self.right_motor_alpha)
        # 2021-04-07: add vertical motor & bln
        self.vertical_motor = Motor(self.motor_driver, channel=self.vertical_motor_channel, alpha=self.vertical_motor_alpha)
        self.bln = Motor(self.motor_driver, channel=self.bln_channel, alpha=self.bln_alpha)
         # end edit

    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed
        self.right_motor.value = right_speed
    # 2021-04-07: add vertical motor & bln
    def set_vertical_motors(self, vertical_speed):
    	self.vertical_motor.value = vertical_speed
    def set_bln(self, bln_brightness):
    	self.bln.value = bln_brightness
    # end edit
        
    def forward(self, speed=1.0, duration=None):
        self.left_motor.value = speed
        self.right_motor.value = speed

    def backward(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = -speed

    def left(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = speed

    def right(self, speed=1.0):
        self.left_motor.value = speed
        self.right_motor.value = -speed
    # 2021-04-07: add vertical motor & bln    
    def up(self, speed=1.0):
        self.vertical_motor.value = -speed
    def down(self, speed=1.0):
        self.vertical_motor.value = speed
    def vertical_motors_stop(self):
        self.vertical_motor.value = 0
    # end edit

    def stop(self):
        self.left_motor.value = 0
        self.right_motor.value = 0
