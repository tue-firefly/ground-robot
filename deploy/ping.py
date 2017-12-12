import multiprocessing
import subprocess
import os

def pinger( job_q, results_q ):
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping','-c1',ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def ping_sweep(prefix):
    """
    Returns a list of hosts that respond to a ping request.
    prefix should be the first three octets of an IP address, (e.g. 192.168.1.). In this case the subnet 192.168.1.0/24 is scanned
    """
    pool_size = 255

    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
             for i in range(pool_size) ]

    for p in pool:
        p.start()

    for i in range(1,255):
        jobs.put(prefix + str(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    res = []
    while not results.empty():
        res.append(results.get())
    return res
