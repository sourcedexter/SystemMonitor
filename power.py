import os
 
rate = 0.0
batteries = os.listdir("/sys/class/power_supply/BAT0")
home = os.getenv("HOME")
path = "/tmp/draw"
if batteries:
    batInfo = open("/sys/class/power_supply/BAT0/%s/state" % (batteries[0],))
    voltage = 0.0
    watts_drawn = 0.0
    amperes_drawn = 0.0
    seconds = 0.0
    available = True
    for line in batInfo:
        if "charging state" in line:
            if not "discharging" in line:
                available = False
        if "present voltage" in line:
            voltage = float(line.split()[2]) / 1000.0
        if "present rate" in line and "mW" in line:
            watts_drawn = float(line.split()[2]) / 1000.0
        if "present rate" in line and "mA" in line:
            amperes_drawn = float(line.split()[2]) / 1000.0
        if "remaining capacity" in line:
            capacity = float(line.split()[2])
    if watts_drawn == 0.0 and amperes_drawn == 0.0:
        if os.path.exists(path):
            draw_file = open(path)
            draw = draw_file.readline()
            if draw:
                draw = float(draw)
                seconds = float(draw_file.readline())
                if draw == capacity:
                    seconds = seconds + 1
                    amperes_drawn = float(draw_file.readline())
                else:
                    draw = draw - capacity
                    amperes_drawn = draw / seconds * 3600.0 / 1000.0
                    seconds = 0.0
        draw = open(path,"w")
        draw.write(str(capacity) + "\n" + str(seconds) + "\n" + str(amperes_drawn))
    rate = watts_drawn + voltage * amperes_drawn
    if available:
        if rate < 1.0:
            print "Gathering Data"
        else:
            print '%.2f'%(rate)
    else:
        print "No Data"
        if os.path.exists(path):
            os.remove(path)
else:
    print "No Data"
    if os.path.exists(path):
        os.remove(path) 
