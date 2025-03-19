from machine import Pin, ADC


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
    
    def toggle_led(self):
        self.led.toggle()
