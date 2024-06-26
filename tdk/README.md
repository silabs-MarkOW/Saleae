# TDK IMU Data
This folder contains modules mapping register address to name and sample data saved from Saleae Logic

Size   | Name                    | Description
-------|-------------------------|------------
   3234|icm20648.py              | module containing [ICM-20648](https://invensense.tdk.com/wp-content/uploads/2021/07/DS-000179-ICM-20648-v1.5.pdf#page=40) IMU register bank data
   2917|icm20688.py              | module containing [ICM-20688-P](https://invensense.tdk.com/wp-content/uploads/2020/04/ds-000347_icm-42688-p-datasheet.pdf) IMU register bank data
  69608|spi-tdk-icm-20648.sal    | Session containing SPI data capture from Thunderboard BG22 BRD4184A
 542690|spi-tdk-icm-20648.csv    | SPI analyer table exported from session above
 
## spi-tdk-icm-20648.sal
First bytes of communication:

![image](https://github.com/silabs-MarkOW/Saleae/assets/41750418/a29ae4a4-b495-49b0-8d69-07beacf0ebbb)

SPI analyzer configured as 

![image](https://github.com/silabs-MarkOW/Saleae/assets/41750418/67b287de-820e-4fce-9ba0-7ecb537008e5)

