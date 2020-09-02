#!/usr/bin/env python3

# make sure raspberry PI is set to use python 3 as math operations change between 2 and 3. specifically floats

import smbus
import errno
import time

if __name__ == "__main__":
    bus_number = 1  # 1 indicates /dev/i2c-1
    bus = smbus.SMBus(bus_number)
    device_count = 0
    
    #Pressure and Sensor readings... Registers
    PRS_B2 = 0x00 # just read 6 bytes
    #PRS_B1 = 0x01
    #PRS_B0 = 0x02
    #TMP_B2 = 0x03
    #TMP_B1 = 0x04
    #TMP_B0 = 0x05    
    
    
    reg_pressure = 0xEF
    
    PRS_CFG_reg =  0x06 #Pressure Configuration
    TMP_CFG_reg =  0x07 #Temperature Configuration
    
    MEA_CFG_reg = 0x08 #operating mode and status
    
    CFG_reg = 0x09 #interrupts and FIFO
    

    
    product_id = 0x0d
    #product and revision ID reg = 0x10
    
    #calibration coefficient registers (read-only)
    c0_reg = 0x10 #just read 18 bytes
    #c0_c1_reg = 0x11
    #c1_reg = 0x12
    #c00_reg1 = 0x13
    #c00_reg2 = 0x14
    #c01_reg1 = 0x18
    #c01_reg2 = 0x19
    #c10_reg1 = 0x16
    #c10_reg2 = 0x17
    #c11_reg1 = 0x1A
    #c11_reg2 = 0x1B
    #c20_reg1 = 0x1c
    #c20_reg2 = 0x1d
    #c21_reg1 = 0x1E
    #c21_reg2 = 0x1F
    #c30_reg1 = 0x20
    #c30_reg2 = 0x21


    
    time.sleep(0.1)
    
    bus.write_byte(0x70, 1 << 0) #set the tca9548a to just get 1st sensor
    
    #set pressure precision
    pressure_percision = 0b00000110 # once per second... and 64 times oversampling
    #scale_factor = 1040384 #based on 64 times precision from Table 4 in cutsheet
    scale_factor = 524288
    
    pressure_percision = 4 << 4 | 4
    bus.write_i2c_block_data(0x77, PRS_CFG_reg, [pressure_percision])
    
    temp_percision = 1 << 7 | 4 << 4 | 0
    bus.write_i2c_block_data(0x77, TMP_CFG_reg, [temp_percision])
    
    cfg = 1 << 2
    bus.write_i2c_block_data(0x77, CFG_reg, [cfg])
    
    operating_mode = 7
    bus.write_i2c_block_data(0x77, MEA_CFG_reg, [operating_mode])
    
    time.sleep(1.1)
    
    #read coeficients
    c = bus.read_i2c_block_data(0x77, c0_reg, 18)
    print ('c = ', c)
    print('c = ',' '.join(map(str, c))) 

    
   
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
    
    
    time.sleep(1.1)
    

    
    #val = bus.read_i2c_block_data(0x77, pressure_reg, 4)
    #print(val)
    sensor_read = bus.read_i2c_block_data(0x77,0x00,6)
    print(sensor_read)
    
    
    temp_raw = (sensor_read[3] << 16) | (sensor_read[4] << 8) | sensor_read[5]
    #temp_raw = (0xff000000 | temp_raw) if (temp_raw & 1 << 23) else temp_raw;
    print('temp_raw',temp_raw)
    
    scaled_temperature = float(temp_raw / scale_factor)
    print('scaled_temperature = ',scaled_temperature)
    
    t_comp = (c0*0.5) + (c1*scaled_temperature)
    print('t_comp = ',t_comp)    
    
    
    
    #press_raw1 = (((sensor_read[0] & 0x80 ? 0xFF000000 : 0) | (sensor_read[0] << 16) | (sensor_read[1] << 8) | sensor_read[2]));
    press_raw0 = (sensor_read[0] << 16) | (sensor_read[1] << 8) | sensor_read[2]; 
    print('raw0 = ', press_raw0)
    #press_raw1 = sensor_read[0] & 0x80 ? 0xFF000000 : 0
    press_raw1 = -16777216 if(sensor_read[0] & 0x80) else 0
    print('raw1 = ', press_raw1)
    press_raw = press_raw0 | press_raw1
    print('press_raw = ', press_raw)
    
    
    
    scaled_pressure = press_raw / scale_factor
    print('scaled_pressure = ',scaled_pressure)
    
    compensated_pressure0 = c10 + (scaled_pressure * (c20 + scaled_pressure * c30))
    print('compensated_pressure0 = ',compensated_pressure0)
    compensated_pressure1 = scaled_temperature * scaled_pressure * (c11 + scaled_pressure * c21)
    print('compensated_pressure1 = ',compensated_pressure1)

    fp = c00 + scaled_pressure * compensated_pressure0 + scaled_temperature * c01 + compensated_pressure1;
    print('pressure_compensated = ', fp)
    
    msl_pressure = 101325   #// in Pa
    pK = fp / msl_pressure;
    print("pk: ", pK);
    
    #press_raw_sc = press_raw/scale_factor
    #temp_raw_sc = temp_raw/scale_factor
    #pressure_compensated = c00 + press_raw_sc * (c10 + press_raw_sc * (c20 + press_raw_sc * c30)) + temp_raw_sc * c01 + temp_raw_sc * press_raw_sc * (c11 + press_raw_sc ^ c21)
    #print('pressure_compensated = ', pressure_compensated)
    
    #for device in range(3, 128):
    try:
        #bus.write_byte(0x70, 1 << 0) ##set the tca9548a to read 1st sensor
        #bus.write_byte(0x70, 1 << 1) #set the tca9548a to read 2 sensor
        #bus.write_byte(0x70, 1 << 2) #set the tca9548a to read 3 sensor
        #bus.write_byte(0x70, 1 << 3) #set the tca9548a to read 4 sensor
        #bus.write_byte(0x70, 1 << 4) #set the tca9548a to read 5 sensor
 
        bus.write_byte(0x77, 0)
        print("Found {0} pressure sensor...")
        device_count = device_count + 1
    except IOError as e:
        if e.errno != errno.EREMOTEIO:
            print("Error: {0} on address {1}".format(e, hex(address)))
    except Exception as e: # exception if read_byte fails
        print("Error unk: {0} on address {1}".format(e, hex(address)))

    bus.close()
    bus = None
    print("Found {0} device(s)".format(device_count))