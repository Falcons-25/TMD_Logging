import time, random

count = 0
thr_count = 0
thr_reach_100 = False
try:
    with open("TM_log.csv", 'a') as file:
        print(f"{time.strftime("%Y-%m-%d %H:%M:%S")},APC 6x4EP,EMAX EcoII 2207 (1900KV),CC Phoenix Edge 75,DOGCOM 3000mAh 80C \"DI\"", file=file)
        while True:
            thr = int(thr_count)
            if thr==100: thr_reach_100 = True
            elif thr==-1:
                print("Completed.")
                break
            t = random.randint(0, 1310)
            c = 1 + random.random()*29
            c2 = 1 + random.random()*29
            v = 14 + random.random()*2.8
            v2 = 14 + random.random()*2.8
            rpm = random.randint(0, 21000)
            chg = int(count * 0.4)
            print(f"{time.strftime("%Y-%m-%d %H:%M:%S")},{int(thr)},{t},{c:.3f},{c2:.3f},{v:.2f},{v2:.2f},{int(rpm)},{chg}", file=file)
            count += 1
            if thr_reach_100:
                thr_count -= 0.3
            else:
                thr_count += 0.3
            time.sleep(0.1)
except KeyboardInterrupt:
    with open("TM_log.csv", 'a') as file:
        print(file=file)
    print("Terminated.")