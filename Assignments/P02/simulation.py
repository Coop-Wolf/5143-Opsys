import pygame
import pandas as pd
import ast

# -----------------------------
# Load timeline data
# -----------------------------
df = pd.read_csv("./timelines/timeline0008.csv")

def parse_list(s):
    try:
        return ast.literal_eval(s) if isinstance(s, str) else s
    except:
        return []

for col in ["ready_queue", "wait_queue", "cpus", "ios"]:
    df[col] = df[col].apply(parse_list)

# -----------------------------
# Pygame setup
# -----------------------------
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OS Scheduling Simulation")
clock = pygame.time.Clock()

# Colors
BG = (30, 30, 30)
BOX_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

# Define positions for boxes
boxes = {
    "ready": (50, 50, 250, 60),
    "wait": (600, 50, 250, 60),
    "CPU0": (250, 150, 100, 100),
    "CPU1": (400, 150, 100, 100),
    "IO0": (250, 300, 100, 100),
    "IO1": (400, 300, 100, 100),
}

# Assign colors for processes
all_procs = sorted(set(df["process"].dropna()))
PROCESS_COLORS = {p: pygame.Color("hsl(%d,100%%,50%%)" % (i*60 % 360)) for i, p in enumerate(all_procs)}

# Process positions dictionary
positions = {}  # proc_id -> current (x, y)
target_positions = {}  # proc_id -> target (x, y)
speed = 5  # pixels per frame

# -----------------------------
# Helper functions
# -----------------------------
def get_queue_positions(name, items):
    """Return positions for all items in a queue (row layout)."""
    x0, y0, w, h = boxes[name]
    positions = []
    for i, proc in enumerate(items):
        positions.append((x0 + 30 + i*30, y0 + h//2))
    return positions

def get_box_center(name):
    """Return center coordinates for CPU/IO box."""
    x, y, w, h = boxes[name]
    return (x + w//2, y + h//2)

def draw_box(name):
    x, y, w, h = boxes[name]
    pygame.draw.rect(screen, BOX_COLOR, (x, y, w, h))
    font = pygame.font.SysFont(None, 24)
    label = font.render(name, True, TEXT_COLOR)
    screen.blit(label, (x + 5, y + 5))

def update_targets(row):
    """Set target positions for all processes based on current row."""
    # Ready Queue
    rq_positions = get_queue_positions("ready", row["ready_queue"])
    for proc, pos in zip(row["ready_queue"], rq_positions):
        if proc is not None:
            target_positions[proc] = pos
            positions.setdefault(proc, pos)

    # Wait Queue
    wq_positions = get_queue_positions("wait", row["wait_queue"])
    for proc, pos in zip(row["wait_queue"], wq_positions):
        if proc is not None:
            target_positions[proc] = pos
            positions.setdefault(proc, pos)

    # CPUs
    for i, proc in enumerate(row["cpus"]):
        if proc is not None:
            target_positions[proc] = get_box_center(f"CPU{i}")
            positions.setdefault(proc, target_positions[proc])

    # IOs
    for i, proc in enumerate(row["ios"]):
        if proc is not None:
            target_positions[proc] = get_box_center(f"IO{i}")
            positions.setdefault(proc, target_positions[proc])

def move_processes():
    """Move processes toward their target positions smoothly."""
    for proc, (tx, ty) in target_positions.items():
        x, y = positions[proc]
        dx, dy = tx - x, ty - y
        dist = (dx**2 + dy**2)**0.5
        if dist < speed or dist == 0:
            positions[proc] = (tx, ty)
        else:
            positions[proc] = (x + dx/dist*speed, y + dy/dist*speed)

def draw_processes():
    """Draw all processes at current positions with labels."""
    font = pygame.font.SysFont(None, 20)
    for proc, (x, y) in positions.items():
        pygame.draw.circle(screen, PROCESS_COLORS[proc], (int(x), int(y)), 12)
        label = font.render(str(proc), True, TEXT_COLOR)
        screen.blit(label, (int(x)-6, int(y)-6))

# -----------------------------
# Main loop
# -----------------------------
frame = 0
running = True
frames_per_step = 15  # number of frames to move between time steps
step_counter = 0

while running:
    clock.tick(30)  # FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG)

    if frame < len(df):
        if step_counter == 0:
            row = df.iloc[frame]
            update_targets(row)
        step_counter += 1
        if step_counter >= frames_per_step:
            step_counter = 0
            frame += 1

    # Draw boxes
    for name in boxes:
        draw_box(name)

    # Move and draw processes
    move_processes()
    draw_processes()

    # Draw current time
    if frame < len(df):
        t = df.iloc[frame]["time"]
        font = pygame.font.SysFont(None, 36)
        time_label = font.render(f"Time: {t}", True, TEXT_COLOR)
        screen.blit(time_label, (WIDTH//2 - 50, 10))

    pygame.display.flip()

pygame.quit()
