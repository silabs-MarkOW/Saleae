# Saleae
Scripts for processing data acquired using Saleae Logic

## TDK IMU SPI Decoder

<pre>
~/src/Saleae$ python3 decode-spi-tdk-imu.py --model 20648 --spi tdk/spi-tdk-icm-20648.csv
WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
WRITE bank0[0x06]           PWR_MGMT_1 : 0x80
WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
WRITE bank0[0x03]            USER_CTRL : 0x10
WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
 READ bank0[0x00]             WHO_AM_I : 0xe0
WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
WRITE bank0[0x06]           PWR_MGMT_1 : 0x01
WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
WRITE bank0[0x0f]          INT_PIN_CFG : 0xc0
...
WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
 READ bank0[0x1a]         INT_STATUS_1 : 0x01
WRITE bank0[0x7f]         REG_BANK_SEL : 0x20
 READ bank2[0x14]         ACCEL_CONFIG : 0x00
WRITE bank2[0x7f]         REG_BANK_SEL : 0x00
 READ bank0[0x2d]         ACCEL_XOUT_H : 0xfb,0x90,0xf1,0x88,0x3d,0x10
WRITE bank0[0x7f]         REG_BANK_SEL : 0x20
 READ bank2[0x01]        GYRO_CONFIG_1 : 0x19
WRITE bank2[0x7f]         REG_BANK_SEL : 0x00
 READ bank0[0x33]          GYRO_XOUT_H : 0xff,0xfc,0x00,0x48,0xff,0xf5
WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
 READ bank0[0x1a]         INT_STATUS_1 : 0x00
</pre>

Can display timestamp and restrict display by time
<pre>
~/src/Saleae$ python3 decode-spi-tdk-imu.py --model 20648 --spi tdk/spi-tdk-icm-20648.csv --timestamp=6 --before 24.07
23.941074: WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
23.941081: WRITE bank0[0x06]           PWR_MGMT_1 : 0x80
24.041118: WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
24.041125: WRITE bank0[0x03]            USER_CTRL : 0x10
24.041132: WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
24.041140:  READ bank0[0x00]             WHO_AM_I : 0xe0
24.041148: WRITE bank0[0x7f]         REG_BANK_SEL : 0x00
24.041155: WRITE bank0[0x06]           PWR_MGMT_1 : 0x01
</pre>
