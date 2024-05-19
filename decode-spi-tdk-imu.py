from tdk import icm20648
from tdk import icm20688
import sys
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--debug',action='store_true',help='show generally uninteresting info')
parser.add_argument('--summary',action='store_true',help='summarize time of activity')
parser.add_argument('--timestamp',type=int,default=0,help='decimal places for timestamp.  Default, 0, suppress')
parser.add_argument('--after',type=float,help='include only output before seconds')
parser.add_argument('--before',type=float,help='include only output after seconds')
parser.add_argument('--spi',required=True,help='Saleae SPI analyzer table export')
parser.add_argument('--model',required=True,help='IMU model (20648/20688')
args = parser.parse_args()

if '20648' == args.model :
    BANK_SEL_SHIFT = 4
    BANK_SEL_MASK = 3 << BANK_SEL_SHIFT
    BANK_SEL_ADDR = 0x7f
    register_banks = icm20648.register_banks
elif '20688' == args.model :
    BANK_SEL_SHIFT = 0
    BANK_SEL_MASK = 7
    BANK_SEL_ADDR = 0x76
    register_banks = icm20688.register_banks
else :
    raise RuntimeError('Model must be one of 20648, 20688')
if args.debug :
    print('BANK_SEL_SHIFT: %d'%(BANK_SEL_SHIFT))
    print('BANK_SEL_MASK: 0x%x'%(BANK_SEL_MASK))

if None != args.before and None != args.after and args.before > args.after :
    raise RuntimeError('before > after')

lines = [x for x in csv.DictReader(open(args.spi,'r')).reader]

class IMU :
    def __init__(self,banks, timestamp) :
        self.miso = []
        self.mosi = []
        self.bank = 0
        self.banks = banks
        self.timestamp = timestamp
        if timestamp :
            self.tsfmt = '%%0.%df:'%(timestamp)
        self.before = None
        self.after = None
        self.normalize()
    def normalize(self) :
        max = 1
        for bank in self.banks :
            for index in bank :
                length = len(bank[index])
                if length > max :
                    max = length
        fmt = '%%0%ds'%(max)
        if args.debug : print('format string: "%s"'%fmt)
        for bank in self.banks :
            for index in bank :
                bank[index] = fmt%(bank[index])
    def push(self,mosi,miso) :
        self.mosi.append(mosi)
        self.miso.append(miso)
    def start(self,seconds) :
        self.seconds = seconds
    def suppress_after(self,seconds) :
        self.before = seconds
    def suppress_before(self,seconds) :
        self.after = seconds
    def visible(self,seconds) :
        if None != self.after and self.seconds < self.after : return False
        if None != self.before and self.seconds > self.before : return False
        return True
    def process(self,seconds) :
        read = self.mosi[0] >> 7
        addr = self.mosi[0] & 0x7f
        name = self.banks[self.bank][addr]
        if self.visible(seconds) :
            if self.timestamp :
                print(self.tsfmt%(self.seconds),end=' ')
            if read :
                data = ','.join(['0x%02x'%(x) for x in self.miso[1:]])
                print(' READ bank%d[0x%02x] %s : %s'%(self.bank,addr,name,data))
            else :
                data = ','.join(['0x%02x'%(x) for x in self.mosi[1:]])
                print('WRITE bank%d[0x%02x] %s : %s'%(self.bank,addr,name,data))
        if addr == BANK_SEL_ADDR :
            bank = (self.mosi[1] & BANK_SEL_MASK) >> BANK_SEL_SHIFT
            if self.bank != bank :
                if args.debug : print('Bank change: %d -> %d'%(self.bank,bank))
                self.bank = bank
        self.miso = []
        self.mosi = []

imu = IMU(register_banks,args.timestamp)
if None != args.after :
    imu.suppress_before(args.after)
if None != args.before :
    imu.suppress_after(args.before)
if args.summary :
    first = None
enable = False
titles = lines[0]
for line in lines[1:] :
    if 'SPI' != line[0] :
        raise RuntimeError(line)
    seconds = float(line[2])
    duration = float(line[3])
    if args.summary :
        if None == first :
            first = seconds
        continue
    if enable :
        if 'disable' == line[1] :
            enable = False
            imu.process(seconds+duration)
        elif 'result' == line[1] :
            imu.push(int(line[4][2:],16),int(line[5][2:],16))
        else :
            raise RuntimeError(line)
    else :
        if 'enable' == line[1] :
            enable = True
            imu.start(seconds)
        else :
            raise RuntimeError(line)
    #print(line)
if args.summary :
    print('SPI activity in range %.9f to %.9f seconds'%(first,seconds+duration))
