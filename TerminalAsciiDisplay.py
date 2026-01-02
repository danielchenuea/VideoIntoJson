import numpy as np
import time
import os

DISPLAY_0 = '░'
DISPLAY_1 = '█'
NPY_RAWVIDEO_PATH = "videoContent.npz"  # Path to the numpy file
JSON_CONFIG_PATH = "videoConfig.json"  # Path to the JSON config file

def display_matrix_ascii(matrix):
    # Convert 0 to '_' and 1 to '#', print only every second row to reduce height
    lines = [''.join([DISPLAY_1 if val == 1 else DISPLAY_0 for val in row]) for i, row in enumerate(matrix) if i % 2 == 0]
    return '\n'.join(lines)


def play_video_from_numpy(npy_path, json_config):
    frames = np.load(npy_path)['arr_0']
    import json
    with open(json_config, 'r') as f:
        config = json.load(f)

    name = config.get('name')
    total_frames = config.get('total_frames')
    width = config.get('frame_width')
    height = config.get('frame_height')
    grid_rows = config.get('grid_rows')
    grid_cols = config.get('grid_cols')
    fps = config.get('fps')

    # Validation to prevent division by zero
    if not isinstance(fps, (int, float)) or fps <= 0:
        print("Warning: FPS value is invalid or zero. Setting FPS to 1.")
        fps = 1
    if not isinstance(grid_rows, int) or grid_rows <= 0:
        print("Warning: grid_rows is invalid or zero. Setting to 1.")
        grid_rows = 1
    if not isinstance(grid_cols, int) or grid_cols <= 0:
        print("Warning: grid_cols is invalid or zero. Setting to 1.")
        grid_cols = 1

    print(f"Loaded {total_frames} frames from {npy_path}")

    frame_idx = 0
    playing = True

    # prev_frame_time = time.time()
    while True:
        frame_data = frames[frame_idx]
        # frame_data shape: (grid_rows, grid_cols, 3)
        # Reconstruct a frame from the grid matrix

        # cell_w = width // grid_cols
        # cell_h = height // grid_rows
        # frame = np.zeros((height, width, 3), dtype=np.uint8)
        # for r in range(grid_rows):
        #     for c in range(grid_cols):
        #         color = frame_data[r, c]
        #         x0 = c * cell_w
        #         y0 = r * cell_h
        #         x1 = x0 + cell_w
        #         y1 = y0 + cell_h
        #         color = (255, 255, 255) if color == 1 else (0, 0, 0)
        #         frame[y0:y1, x0:x1] = color[::-1]  # Convert RGB to BGR for OpenCV
        key_delay = int(1000 / fps) if fps > 0 else 1000
        
        print("\033[H", end="\r")  # Move cursor to top-left
        print(display_matrix_ascii(frame_data), end="\r")

        time.sleep((key_delay / 1000.0))
        if playing:
            frame_idx = (frame_idx + 1) % total_frames

if __name__ == "__main__":
    # Example: random 0/1 matrix, replace with your own data source
    width, height = 80, 60
    fps = 30
    frame_delay = 1.0 / fps

    play_video_from_numpy(NPY_RAWVIDEO_PATH, JSON_CONFIG_PATH)

    # # Simulate a video: here, just random frames for demonstration
    # for _ in range(300):  # Show 300 frames (~10 seconds)
    #     matrix = np.random.randint(0, 2, (height, width), dtype=int)
    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     print(display_matrix_ascii(matrix))
    #     time.sleep(frame_delay)
