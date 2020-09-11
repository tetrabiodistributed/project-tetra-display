import smbus
import errno
import time


bus_number = 1  # 1 indicates /dev/i2c-1
bus = smbus.SMBus(bus_number)
device_count = 0

#Registers
PRS_B2 = 0x00 # first 6 bytes are Pressure/sensor data

PRS_CFG_reg =  0x06 #Pressure Configuration
TMP_CFG_reg =  0x07 #Temperature Configuration
MEA_CFG_reg = 0x08 #operating mode and status
CFG_reg = 0x09 #interrupts and FIFO
product_id = 0x0d
 
#calibration coefficient registers (read-only)
c0_reg = 0x10 #just read 18 bytes

bus.write_byte(0x70, 1 << 0) # 1st pressure sensor
#bus.write_byte(0x70, 1 << 1) # sensor #2
#bus.write_byte(0x70, 1 << 2) # sensor #3
#bus.write_byte(0x70, 1 << 3) # sensor #4
#bus.write_byte(0x70, 1 << 4) # sensor #5



# compensation scale factors
#
# oversampling rate  : single | 2       | 4       | 8       | 16     | 32     | 64      | 128
# scale factor(KP/KT): 524288 | 1572864 | 3670016 | 7864320 | 253952 | 516096 | 1040384 | 2088960
scale_factor =  524288 # 1x
#scale_factor = 253952 # 16x
#scale_factor =  1040384 #64x


# configuration of pressure measurement rate (PM_RATE) and resolution (PM_PRC)
#
# bit[7]: reserved
#
# PM_RATE[6:4]    : 0 | 1 | 2 | 3 | 4  | 5  | 6  | 7
# measurement rate: 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128
# note: applicable for measurements in background mode only
#
# PM_PRC[3:0]         : 0      | 1   | 2   | 3    | 4    | 5    | 6     | 7
# oversampling (times): single | 2   | 4   | 8    | 16   | 32   | 64    | 128
# measurement time(ms): 3.6    | 5.2 | 8.4 | 14.8 | 27.6 | 53.2 | 104.4 | 206.8
# precision(PaRMS)    : 5.0    |     | 2.5 |      | 1.2  | 0.9  | 0.5   |
# note: use in combination with a bit shift when the oversampling rate is > 8 times. see CFG_REG(0x19) register

# PRS-CFG_reg 0x06
pressure_percision = 1 << 7 | 4 << 4 | 0 # 0b11000000 16hz, 1x oversampling
bus.write_i2c_block_data(0x77, PRS_CFG_reg, [pressure_percision])



# configuration of temperature measurment rate (TMP_RATE) and resolution (TMP_PRC)
#
# temperature measurement: internal sensor (in ASIC) | external sensor (in pressure sensor MEMS element)
# TMP_EXT[7]             : 0                         | 1
# note: it is highly recommended to use the same temperature sensor as the source of the calibration coefficients wihch can be read from reg 0x28
#
# TMP_RATE[6:4]   : 0 | 1 | 2 | 3 | 4  | 5  | 6  | 7
# measurement rate: 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128
# note: applicable for measurements in background mode only
#
# bit[3]: reserved
#
# TMP_PRC[2:0]        : 0      | 1 | 2 | 3 | 4  | 5  | 6  | 7
# oversampling (times): single | 2 | 4 | 8 | 16 | 32 | 64 | 128
# note: single(default) measurement time 3.6ms, other settings are optional, and may not be relevant
# note: use in combination with a bit shift when the oversampling rate is > 8 times. see CFG_REG(0x19) register

# TMP_CFG_reg 0x07
temp_percision = 1 << 7 | 4 << 4 | 0 # 0b11000000 16hz, 1x oversampling
#temp_percision = 1 << 7  | 4 # 0b11000000 16hz, 16x oversampling
bus.write_i2c_block_data(0x77, TMP_CFG_reg, [temp_percision])



# diasble all interrupts and FIFO
#
# bit7: interrupt(on SDO pin) active level
#       0-active low  1-active hight
#
# bit6: set to '1' for FIFO full interrupt
# bit5: set to '1' for pressure measurement ready interrupt
# bit4: set to '1' for temperature measurement ready interrupt
#
# note: bit3 must be set to '1' when the temperature oversampling rate is > 8 times
# note: bit2 must be set to '1' when the pressure oversampling rate is > 8 times
#
# bit1: set to '1' for FIFO enable
#
# bit0: set to '0' for 4-wire interface
#       set to '1' for 3-wire interface

cfg = 1 << 2  #  0b00000100 16hz, 1x oversampling
#cfg = 0b01001110 # 16x oversampling (temperature works... pressure too high)
bus.write_i2c_block_data(0x77, CFG_reg, [cfg])



# sensor operating mode and status
#
# COEF_RDY[7]: 0-coefficients are not available yet;  1-coefficients are available
#
# SENSOR_RDY[6]: 0-sensor initialization not complete;  1-sensor initialization complete
#                it is recommend not to start measurements until the sensor has complete the self initialization
#
# TMP_RDY[5]: 1-new temperature measurement is ready. cleared when temperature measurement is read
# PRS_RDY[4]: 1-new pressure measurement is ready. cleared when procurement measurement is read.
#
# measurement mode: stop meas |  command mode(single) |    na |            background mode(continuous) |
# measurement type:      idle | pres meas | temp meas |    na | pres meas | temp meas | pres&temp meas |
# MEAS_CTRL[2:0]  :         0 |         1 |         2 | 3 | 4 |         5 |         6 |              7 |
operating_mode = 7 #  0b00000111
bus.write_i2c_block_data(0x77, MEA_CFG_reg, [operating_mode])

time.sleep(0.1)

#read coeficients
c = bus.read_i2c_block_data(0x77, c0_reg, 18)
print ('c = ', c)

#temperature coeficients
c0 = c[0] << 4 | c[1] >> 4; #working... returns 200
print('c0= ',c0)
#c0 = (0xf000 | c0) if (c0 & 1 << 11) else c0

#//bitwise from https://github.com/DimianZhan/spl06/blob/master/spl06.c

c1 = (c[1] & 0x0f) << 8 | c[2]
c1 = (-4096 | c1) if c1 & 1 << 11 else c1
print('c1=',c1)

#_spl.coe.c00 = (uint32_t)buf[3] << 12 | (uint32_t)buf[4] << 4 | (uint16_t)buf[5] >> 4;
#_spl.coe.c00 = (_spl.coe.c00 & 1 << 19) ? (0xfff00000 | _spl.coe.c00) : _spl.coe.c00;
c00 = c[3] << 12 | c[4] << 4 | c[5] >> 4;
#c00 = (0xfff00000 | c00) if (c00 & 1 << 19) else c00;
print('c00= ',c00)

c10 = ((c[5] & 0x0F) << 16) | (c[6] << 8) | c[7];
c10_temp = -1048576 if(c[5] & 0x8) else 0
c10 = c10 | c10_temp
print('c10=', c10)

c01 = c[8] << 8 | c[9];
c11 = c[10] << 8 | c[11];
c20 = c[12] << 8 | c[13];
c21 = c[14] << 8 | c[15];
c30 = c[16] << 8 | c[17];
print('c01=',c01)
print('c11=', c11)
print('c20=', c20)
print('c21=', c21)
print('c30=', c30)


id = bus.read_i2c_block_data(0x77, product_id, 1)
print ('id = ', id)
meas_cfg = bus.read_i2c_block_data(0x77, MEA_CFG_reg, 1)
print ('meas_cfg = ', meas_cfg)

   
    
    
def getSensorData():
    #print("Doing stuff...")
    sensor_read = bus.read_i2c_block_data(0x77,0x00,6)
    print(sensor_read)

    temp_raw = (sensor_read[3] << 16) | (sensor_read[4] << 8) | sensor_read[5]
    #temp_raw = (0xff000000 | temp_raw) if (temp_raw & 1 << 23) else temp_raw;
    #print('temp_raw',temp_raw)

    press_raw = sensor_read[0] << 16 | sensor_read[1] << 8 | sensor_read[2];
    #press_raw = (0xff000000 | press_raw) if (press_raw & 1 << 23) else press_raw;
    #print('press_raw = ', press_raw)

    #press_raw1 = (((sensor_read[0] & 0x80 ? 0xFF000000 : 0) | (sensor_read[0] << 16) | (sensor_read[1] << 8) | sensor_read[2]));
    press_raw0 = (sensor_read[0] << 16) | (sensor_read[1] << 8) | sensor_read[2]; 
    #print('raw0 = ', press_raw0)
    #press_raw1 = sensor_read[0] & 0x80 ? 0xFF000000 : 0
    press_raw1 = -16777216 if(sensor_read[0] & 0x80) else 0
    #print('raw1 = ', press_raw1)
    press_raw = press_raw0 | press_raw1
    #print('press_raw = ', press_raw)

    ftsc = float(temp_raw / scale_factor)
    #print('ftsc',ftsc)


    t_comp = (c0*0.5) + (c1*ftsc)
    #print('t_comp = ',t_comp)
    print('t_comp (F)= ', 32 + (t_comp *9/5))

    fpsc = press_raw / scale_factor
    #print('fpsc = ',fpsc)
    qua2 = c10 + (fpsc * (c20 + fpsc * c30))
    #print('qua2 = ',qua2)
    qua3 = ftsc * fpsc * (c11 + fpsc * c21)
    #print('qua3 = ',qua3)

    fp = c00 + fpsc * qua2 + ftsc * c01 + qua3;
    print('pressure_compensated = ', fp)

    msl_pressure = 101325   #// in Pa
    pK = fp / msl_pressure;
    print("pk: ", pK);
    time.sleep(1)
    

while True:
    getSensorData()

        
        #bus.write_byte(0x77, 0)
        #print("Found {0} pressure sensor...")
        #device_count = device_count + 1
    #except IOError as e:
        #if e.errno != errno.EREMOTEIO:
            #print("Error: {0} on address {1}".format(e, hex(address)))
    #except Exception as e: # exception if read_byte fails
        #print("Error unk: {0} on address {1}".format(e, hex(address)))

    #bus.close()
    #bus = None
    #print("Found {0} device(s)".format(device_count))
    
