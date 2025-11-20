import json
import sys
from cmd_pkg import *
from gen_jobs import generate_jobs

# ---------------------------------------
# Load JSON into Process objects
# ---------------------------------------
def load_processes_from_json(filename="generated_processes.json", limit=None):
    """Load processes from a JSON file into Process instances
    Args:
        filename: path to the JSON file
        limit: if set, only load this many processes
    Returns:
        list of Process instances
    Raises:
        FileNotFoundError if the file does not exist
    """

    # If limit is set, only load that many processes
    with open(filename) as f:
        data = json.load(f)

    processes = []

    # If limit is None or greater than available, use all
    if limit is None or limit > len(data):
        limit = len(data)

    # :limit slices the list of processes loaded from the JSON file to only include
    # the first 'limit' number of processes.
    # This is useful for testing or running simulations with a smaller subset of processes.
    for p in data[:limit]:

        # Create a list of bursts in the expected format for Process
        # [{"cpu": X}, {"io": {"type": T, "duration": D}}, ...]
        bursts = []

        # Iterate over each burst in the process's burst list
        # and append to bursts list in the correct format
        for b in p["bursts"]:
            if "cpu" in b:
                # format {"cpu": X}
                bursts.append({"cpu": b["cpu"]})

            elif "io" in b:
                # format {"io": {"type": T, "duration": D}}
                bursts.append(
                    {"io": {"type": b["io"]["type"], "duration": b["io"]["duration"]}}
                )

        proc = Process(pid=p["pid"], bursts=bursts, priority=p["priority"], arrival_time=p["arrival_time"])
        processes.append(proc)

    return processes


def parse_value(value):
    """
    Try to convert string to appropriate type since everything read in from command line is a string
    Args:
        value: string value to parse
    Returns:
        value converted to bool, int, float, or original string
    """
    # Try boolean
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    # Try int
    try:
        return int(value)
    except ValueError:
        pass
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    # Give up, return string
    return value


def argParse():
    """Parse command line arguments into a dictionary
    Returns:
        dict of argument names to values
    """
    kwargs = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            kwargs[key] = parse_value(value)
    return kwargs


def increment_timeline_count():
    '''
    Gets the number of timelines from tid.txt,
    and increments its value by one and returns
    '''
    
    with open("timelines/tid", "r") as f:
        tid = int(f.read().strip())
    new_tid = tid + 1
    with open("timelines/tid", "w") as f:
        f.write(str(new_tid))
    return new_tid

def get_gen_jobs_count():
    '''
    Gets the numbers of generated jobs from
    fid and returns value
    '''
    with open("gen_jobs/fid", "r") as f:
        fid = int(f.read().strip())
    return fid


# ---------------------------------------
# Example usage
# ---------------------------------------
if __name__ == "__main__":
    # Parse command line arguments
    args = argParse()

    # Get parameters if they exist, else use defaults
    # file_num is used to load different process files and save different timeline files
    # If user doesn't give a file_num, it will be set to None and process file will be generated
    file_num = args.get("file_num", None)

    # Limit is used to restrict the number of processes loaded
    limit = args.get("limit", None)

    # Number of CPUs and IO devices
    cpus = args.get("cpus", 1)
    ios = args.get("ios", 1)
    
    # Scheduler
    scheduler = args.get("sched", "fcfs")
    
    # quantum size (default 4)
    quantum = args.get("quantum", 4)

    # Get parameters used for generating process file, if user wants
    # To generate file and simulate on it at the same time.
    num_processes = args.get("num_processes", 10)
    arrival_time = args.get("arrival_time", "zero")
    device_load = args.get("device_load", "default")
    

    # If user gave a file_num to run simluation on, use it
    if file_num:
        
        # Load processes from JSON file
        processes = load_processes_from_json(
            f"./job_jsons/process_file_{str(file_num).zfill(4)}.json", limit=limit)
        
    # User wants a process file to be generated for them
    else:
        
        # Calling generate jobs file function from generate_jobs.py
        file_path = generate_jobs.generate_jobs_file(num_processes, arrival_time, device_load)
        processes = load_processes_from_json(file_path, limit=limit)
        
    # Run the simulation
    clock = Clock()
    print(f"\n=== Simulation with {cpus} CPU(s) and {ios} IO device(s) ===")

    # Initialize scheduler
    if scheduler.lower() == "rr":
        print(f"Using Round Robin with quantum={quantum}")
        sched = RoundRobinScheduler(
            num_cpus=cpus,
            num_ios=ios,
            verbose=False,
            processes=processes,
            quantum=quantum
        )
        
    elif scheduler.lower() == "sjf":
        print("Using Shortest Job First")
        sched = ShortestJobFirst(
            num_cpus=cpus,
            num_ios=ios,
            verbose=False,
            processes=processes
        )
        
    elif scheduler.lower() == "srtf":
        print("Using Shortest Remaining Time First")
        sched = ShortestRemainingTimeFirst(
            num_cpus=cpus,
            num_ios=ios,
            verbose=False,
            processes=processes
        )

    elif scheduler.lower() == "priority":
        aging = args.get("aging", False)
        aging_interval = args.get("aging_interval", 5)
        aging_delta = args.get("aging_delta", 1)
        print(
            f"Using Priority scheduler "
            f"(aging={aging}, interval={aging_interval}, delta={aging_delta})"
        )
        sched = PriorityScheduler(
            num_cpus=cpus,
            num_ios=ios,
            verbose=False,
            processes=processes,
            aging=aging,
            aging_interval=aging_interval,
            aging_delta=aging_delta,
        )    
        
    else:
        print("Using First come First Serve")
        sched = Scheduler(
            num_cpus=cpus,
            num_ios=ios,
            verbose=False,
            processes=processes
        )

    # Run the scheduler
    sched.run()

    # Print final log and stats
    print("\n--- Final Log ---")
    print(sched.timeline())
    print(f"\nTime elapsed: {sched.clock.now() - 1}")
    print(f"Finished: {[p.pid for p in sched.finished]}")

    # Increment count of timelines
    timeline_count = increment_timeline_count()
    
    # Get count of generated jobs
    jobs_count = get_gen_jobs_count()
    
    # Print scheduler stats
    sched.print_scheduler_stats()

    # Export structured logs
    if file_num:
        sched.export_json(f"./timelines/timeline{str(timeline_count).zfill(4)}_{scheduler}_{file_num}.json")
        sched.export_csv(f"./timelines/timeline{str(timeline_count).zfill(4)}_{scheduler}_{file_num}.csv")
    else:
        sched.export_json(f"./timelines/timeline{str(timeline_count).zfill(4)}_{scheduler}_{jobs_count}.json")
        sched.export_csv(f"./timelines/timeline{str(timeline_count).zfill(4)}_{scheduler}_{jobs_count}.csv")
    clock.reset()