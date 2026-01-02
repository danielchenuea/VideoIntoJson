
import cv2
import numpy as np
import time

# Adjustable parameters
NPY_RAWVIDEO_PATH = "videoContent.npz"  # Path to the numpy file
JSON_CONFIG_PATH = "videoConfig.json"  # Path to the JSON config file

def draw_grid_frame(matrix, width, height, grid_rows, grid_cols):
    """
    Reconstruct a frame from the grid matrix.
    Each cell is filled with its RGB color.
    """
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    cell_w = width // grid_cols
    cell_h = height // grid_rows
    pos = 0
    for r in range(grid_rows):
        for c in range(grid_cols):
            # Find cell by position
            cell = None
            if isinstance(matrix[r][c], dict) and 'pos' in matrix[r][c]:
                cell = matrix[r][c]
            else:
                # Fallback: search for cell with matching pos
                for row in matrix:
                    for item in row:
                        if item.get('pos') == pos:
                            cell = item
                            break
                    if cell:
                        break
            x0 = c * cell_w
            y0 = r * cell_h
            x1 = x0 + cell_w
            y1 = y0 + cell_h
            color = cell['rgb'] if cell else (0, 0, 0)
            frame[y0:y1, x0:x1] = color[::-1]  # Convert RGB to BGR for OpenCV
            pos += 1
    return frame


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
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, width, height)

    frame_idx = 0
    playing = True

    while True:

        frame_data = frames[frame_idx]
        # frame_data shape: (grid_rows, grid_cols, 3)
        # Reconstruct a frame from the grid matrix
        cell_w = width // grid_cols
        cell_h = height // grid_rows
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        for r in range(grid_rows):
            for c in range(grid_cols):
                color = frame_data[r, c]
                x0 = c * cell_w
                y0 = r * cell_h
                x1 = x0 + cell_w
                y1 = y0 + cell_h
                frame[y0:y1, x0:x1] = color[::-1]  # Convert RGB to BGR for OpenCV
        key_delay = int(1000 / fps) if fps > 0 else 1000
        cv2.imshow(name, frame)
        key = cv2.waitKey(key_delay) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):  # Pause/play toggle
            playing = not playing
        elif key == ord('d'):
            frame_idx = min(frame_idx + 1, total_frames - 1)
        elif key == ord('a'):
            frame_idx = max(frame_idx - 1, 0)
        elif key == ord('+') or key == ord('='):
            fps = min(fps + 1, 60)
            print(f"FPS: {fps}")
        elif key == ord('-'):
            fps = max(fps - 1, 1)
            print(f"FPS: {fps}")
        if playing:
            frame_idx = (frame_idx + 1) % total_frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    play_video_from_numpy(NPY_RAWVIDEO_PATH, JSON_CONFIG_PATH)
