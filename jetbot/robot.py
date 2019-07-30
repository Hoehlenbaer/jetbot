# Written by SparkFun Electronics June 2019
# Author: Wes Furuya
# *Shell scripts were taken from original jetbot stats.py code.
#
# Do you like this code?
#
# Help support SparkFun and buy a SparkFun jetbot kit!
# https://www.sparkfun.com/products/15365
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

import time
import traitlets
from traitlets.config.configurable import SingletonConfigurable
import qwiic_scmd
from .motor import Motor


class Robot(SingletonConfigurable):

    left_motor = traitlets.Instance(Motor)
    right_motor = traitlets.Instance(Motor)
    
    
    # config
    #i2c_bus = traitlets.Integer(default_value=1).tag(config=True)
    left_motor_channel = traitlets.Integer(default_value=1).tag(config=True)
    left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    right_motor_channel = traitlets.Integer(default_value=2).tag(config=True)
    right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
        
    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        
        self.motor_driver = qwiic_scmd.QwiicScmd()
        self.left_motor = Motor(self.motor_driver, channel=self.left_motor_channel, alpha=self.left_motor_alpha)
        self.right_motor = Motor(self.motor_driver, channel=self.right_motor_channel, alpha=self.right_motor_alpha)
        self.motor_driver.enable()
        
    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed
        self.right_motor.value = right_speed
        self.motor_driver.enable()
 
    # Set Motor Controls: .set_drive( motor number, direction, speed)
    # Motor Number: A = 0, B = 1
    # Direction: FWD = 0, BACK = 1
    # Speed: (-255) - 255 (neg. values reverse direction of motor)
       
    def forward(self, speed=1.0, duration=None):
        speed = int(speed*255)
        self.motor_driver.set_drive(0, 0, speed)
        self.motor_driver.set_drive(1, 0, speed)
        self.motor_driver.enable()

    def backward(self, speed=1.0):
        speed = int(speed*255)
        self.motor_driver.set_drive(0, 1, speed)
        self.motor_driver.set_drive(1, 1, speed)
        self.motor_driver.enable()

    def left(self, speed=1.0):
        speed = int(speed*255)
        self.motor_driver.set_drive(0, 1, speed)
        self.motor_driver.set_drive(1, 0, speed)
        self.motor_driver.enable()

    def right(self, speed=1.0):
        speed = int(speed*255)
        self.motor_driver.set_drive(0, 0, speed)
        self.motor_driver.set_drive(1, 1, speed)
        self.motor_driver.enable()

    def stop(self):
        self.motor_driver.disable()
