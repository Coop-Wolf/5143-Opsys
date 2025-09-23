class PCB:
    
    def __init__(self, start, bursts, pid):
        self.start = start
        self.bursts = bursts
        self.pid = id
        self.waitq_count = 0
        self.readyq_count = 0
        self.running = 0
        self.io = 0
        
        
    def __repr__(self):
        return f"PID: {self.pid}, Start: {self.start}, Burst: {self.bursts}"
        
        
if __name__ == "__main__":
    
    # Will actually be reading from file
    jobs = [PCB(0, [3,2,3], 1), PCB(1, [2,2,3], 2), PCB(1, [2,2,3], 3)]
    
    
    #p1 = PCB(0, [3,2,3], 1)
    #p2 = PCB(1, [2,2,3], 2)
    #p3 = PCB(1, [2,2,3], 3)
    
    runningQ = []
    cpuQ = []
    waitQ = []
    readyQ = []
    ioQ = []
    exitQ = []
    
    clock = 0
    
    print(jobs)
    
    # Loop and add job to ready queue when start time is reached
    for i in range (len(jobs)):
        for i in range (len(jobs) -1):
            if jobs[i].start == clock:
                readyQ.append(jobs[i])
                
        clock += 1
        
        for job in readyQ:
            job.readyq_count += 1
            
        print(readyQ)
            
        
        readyTotal = 0
        
        
        for job in readyQ:
            readyTotal += job.readyq_count
    
        print(readyTotal)