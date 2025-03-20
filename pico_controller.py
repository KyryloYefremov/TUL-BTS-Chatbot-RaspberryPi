import machine
from machine import Pin, ADC
import utime


class PicoController:
    
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        # internal temperature sensor is connected to ADC channel 4
        self.temp_sensor = ADC(4)
    
    def read_internal_temperature(self) -> float:
        # Read the raw ADC value
        adc_value = self.temp_sensor.read_u16()

        # Convert ADC value to voltage
        voltage = adc_value * (3.3 / 65535.0)

        # Temperature calculation based on sensor characteristics
        temperature_celsius = 27 - (voltage - 0.706) / 0.001721

        return temperature_celsius
    
    def init_blink(self, times=3, freq=1):
        for _ in range(times):
            self.led.value(1)  # turn LED ON
            utime.sleep(freq/2)
            self.led.value(0)  # turn LED OFF
            utime.sleep(freq/2)
    
    def toggle_led(self):
        self.led.toggle()
    
