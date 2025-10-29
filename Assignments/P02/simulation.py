import pygame
import pandas as pd
import ast
import colorsys

WIDTH, HEIGHT = 900, 500


def load_timeline(timesheet_id):
    """Load timeline CSV into DataFrame."""
    try:
        df = pd.read_csv(f"./timelines/timeline{timesheet_id}.csv")
        print("✅ File loaded successfully!")
        
        # Parse list columns
        for col in ["ready_queue", "wait_queue", "cpus", "ios"]:
            df[col] = df[col].apply(parse_list)
            
        # Ensure process column is string
        df["process"] = df["process"].astype(str)
        return df
    except FileNotFoundError:
        print(f"❌ Error: The file 'timeline{timesheet_id}.csv' does not exist in the 'timelines' folder.")
        exit(1)

    
def parse_list(l):
    '''Convert string representation of list into Python list.'''
    try:
        return ast.literal_eval(l) if isinstance(l, str) else l
    except:
        return []
    
    
def detect_rr_quantum(df):
    '''Check if RR scheduler is used and detect quantum values'''
    
    # Determining if RR scheduler was ran
    RR = any("preempt_cpu" in str(x) for x in df["event_type"])
    quantum_value = None
    
    if RR:
        rr_events = df[df["event_type"] == "preempt_cpu"]

        for _, preempt_row in rr_events.iterrows():
            proc_id = preempt_row["process"]
            preempt_time = preempt_row["time"]
        
            # Find the last dispatch for this process before this preemption
            dispatch_rows = df[(df["process"] == proc_id) & 
                             (df["event_type"] == "dispatch_cpu") & 
                             (df["time"] < preempt_time)]
        
            if not dispatch_rows.empty:
                dispatch_time = dispatch_rows["time"].max()
                quantum_value = preempt_time - dispatch_time
                break
            
    return RR, quantum_value
        

def init_pygame():
    '''Initialize Pygame.'''
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("OS Scheduling Simulation")
    clock = pygame.time.Clock()
    return screen, clock


def build_boxes(df):
    '''Build boxes dictionary based on CPUs and IOs in timeline.'''
    
    # Determining number of CPUs and IOs
    cpu_count = len(df["cpus"].iloc[0])
    io_count = len(df["ios"].iloc[0])
    
    # Dynamically build boxes dict
    boxes = {
        "Ready": (50, 50, 250, 75),
        "Wait": (600, 50, 250, 75),
        "Finished": (50, 410, 800, 75),
    }

    # Base positions
    cpu_start_x, cpu_y = 300, 150
    io_start_x, io_y = 300, 300
    box_w, box_h = 100, 100
    gap = 150

    # Add CPU boxes
    for i in range(cpu_count):
        boxes[f"CPU {i}"] = (cpu_start_x + i * gap, cpu_y, box_w, box_h)

    # Add IO boxes
    for i in range(io_count):
        boxes[f"IO {i}"] = (io_start_x + i * gap, io_y, box_w, box_h)
        
    return boxes, cpu_count, io_count


def generate_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        colors.append((int(r*255), int(g*255), int(b*255)))
    return colors


def assign_process_colors(df):
    # Generate colors safely
    all_procs = sorted(set(df["process"].dropna()))
    color_list = generate_colors(len(all_procs))
    return {p: pygame.Color(*color_list[i]) for i, p in enumerate(all_procs)}


def get_queue_positions(boxes, name, items):
    x, y, w, h = boxes[name]
    return [(x + 30 + i*30, y + h//2) for i, proc in enumerate(items)]


def get_box_center(boxes, name):
    x, y, w, h = boxes[name]
    return (x + w//2, y + h//2)


def draw_box(screen, boxes, name):
    BG = (30, 30, 30)
    BOX_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    
    x, y, w, h = boxes[name]
    pygame.draw.rect(screen, BOX_COLOR, (x, y, w, h))
    font = pygame.font.SysFont(None, 24)
    label = font.render(name, True, TEXT_COLOR)
    screen.blit(label, (x + 5, y + 5))


def move_processes(positions, target_positions, speed):
    for proc, (tx, ty) in target_positions.items():
        x, y = positions[proc]
        dx, dy = tx - x, ty - y
        dist = (dx**2 + dy**2)**0.5
        if dist < speed or dist == 0:
            positions[proc] = (tx, ty)
        else:
            positions[proc] = (x + dx/dist*speed, y + dy/dist*speed)


def draw_processes(screen, positions, process_colors):
    TEXT_COLOR = (255, 255, 255)
    font = pygame.font.SysFont(None, 20)
    for proc, (x, y) in positions.items():
        pygame.draw.circle(screen, process_colors[proc], (int(x), int(y)), 12)
        label = font.render(str(proc), True, TEXT_COLOR)
        screen.blit(label, (int(x)-6, int(y)-6))


def update_quantum(cpu_quantum, cpu_process, quantum_value, cpu_count):
    for i in range(cpu_count):
        cpu_name = f"CPU {i}"
        if cpu_process[cpu_name] is not None:
            cpu_quantum[cpu_name] -= 1
            if cpu_quantum[cpu_name] <= 0:
                cpu_process[cpu_name] = None
                cpu_quantum[cpu_name] = quantum_value


def update_targets(row, boxes, positions, target_positions, finished_queue, RR, cpu_process, cpu_quantum, quantum_value, cpu_count, io_count):
    # Ready Queue
    for proc, pos in zip(row["ready_queue"], get_queue_positions(boxes, "Ready", row["ready_queue"])):
        if proc:
            if proc not in positions:
                positions[proc] = pos  # Initialize position for new process
            target_positions[proc] = pos

    # Wait Queue
    for proc, pos in zip(row["wait_queue"], get_queue_positions(boxes, "Wait", row["wait_queue"])):
        if proc:
            if proc not in positions:
                positions[proc] = pos
            target_positions[proc] = pos

    # CPUs
    for i, proc in enumerate(row["cpus"]):
        cpu_name = f"CPU {i}"
        if proc:
            center = get_box_center(boxes, cpu_name)
            if proc not in positions:
                positions[proc] = center
            target_positions[proc] = center
            if RR and cpu_process[cpu_name] != proc:
                cpu_process[cpu_name] = proc
                cpu_quantum[cpu_name] = quantum_value

    # IOs
    for i, proc in enumerate(row["ios"]):
        if proc:
            center = get_box_center(boxes, f"IO {i}")
            if proc not in positions:
                positions[proc] = center
            target_positions[proc] = center

    # Finished queue
    if "finished all bursts" in str(row["event"]):
        proc = str(int(float(row["process"])))
        if proc not in finished_queue:
            finished_queue.append(proc)
    for proc, pos in zip(finished_queue, get_queue_positions(boxes, "Finished", finished_queue)):
        if proc not in positions:
            positions[proc] = pos
        target_positions[proc] = pos


# -----------------------------
# Main execution
# -----------------------------
def main():
    BG = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    
    timesheet = input("Enter timesheet ID (ex. 0001): ")
    df = load_timeline(timesheet)
    RR, quantum_value = detect_rr_quantum(df)
    boxes, cpu_count, io_count = build_boxes(df)
    process_colors = assign_process_colors(df)

    positions = {}
    target_positions = {}
    speed = 30
    finished_queue = []

    cpu_quantum = {}
    cpu_process = {}
    if RR:
        cpu_quantum = {f"CPU {i}": quantum_value for i in range(cpu_count)}
        cpu_process = {f"CPU {i}": None for i in range(cpu_count)}

    screen, clock = init_pygame()

    sim_time = 1
    frame = 0
    frames_per_tick = 20
    tick_counter = 0
    running = True

    while running:
        clock.tick(30)  # FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG)

        tick_counter += 1
        if tick_counter >= frames_per_tick:
            sim_time += 1
            tick_counter = 0
            if RR:
                update_quantum(cpu_quantum, cpu_process, quantum_value, cpu_count)

        # Update target positions for all rows whose time == sim_time
        while frame < len(df) and df.iloc[frame]["time"] <= sim_time:
            update_targets(df.iloc[frame], boxes, positions, target_positions, finished_queue, 
                         RR, cpu_process, cpu_quantum, quantum_value, cpu_count, io_count)
            frame += 1

        # Draw boxes
        for name in boxes: 
            draw_box(screen, boxes, name)

        # Move and draw processes
        move_processes(positions, target_positions, speed)
        draw_processes(screen, positions, process_colors)
        
        # Draw CPU quantum labels
        if RR:
            font = pygame.font.SysFont(None, 20)
            y_offset = 150
            for cpu_name, remaining in cpu_quantum.items():
                label = font.render(f"{cpu_name} Quantum: {remaining}", True, TEXT_COLOR)
                screen.blit(label, (WIDTH - 200, y_offset))
                y_offset += 25

        # Draw current time
        font = pygame.font.SysFont(None, 36)
        time_label = font.render(f"Time: {sim_time}", True, TEXT_COLOR)
        screen.blit(time_label, (WIDTH//2 - 50, 10))

        pygame.display.flip()
        
    pygame.quit()


if __name__ == "__main__":
    main()
