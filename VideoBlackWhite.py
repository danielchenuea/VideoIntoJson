

import cv2
import numpy as np
import json

def select_cell_color(frame, x, y):
	"""
	Selects the color for a given cell at (x, y) in the frame.
	By default, returns the RGB value at the center pixel.
	This function can be replaced or modified for different color selection strategies.
	"""
	rgb = frame[y, x, :3]
	rgb = rgb[::-1]  # Convert BGR to RGB
	return rgb

def apply_filter_on_color(rgb):
	"""
	Returns 1 for white and 0 for black, based on luminance.
	"""
	luminance = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
	return 1 if luminance > 127.5 else 0

def extract_frames(video_path):
	cap = cv2.VideoCapture(video_path)
	if not cap.isOpened():
		print(f"Error opening video file: {video_path}")
		return
	# Customizable grid size
	grid_rows = 60  # Change as needed
	grid_cols = 80  # Change as needed
    
	frame_count = 0
	all_frames = []
	fps = cap.get(cv2.CAP_PROP_FPS)
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	# print(f"Video FPS: {fps}")
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		height, width, _ = frame.shape

		# Calculate cell size
		cell_width = width / grid_cols
		cell_height = height / grid_rows

		# Calculate center coordinates for each grid cell
		centers = []
		for row in range(grid_rows):
			row_centers = []
			for col in range(grid_cols):
				x = int((col + 0.5) * cell_width)
				y = int((row + 0.5) * cell_height)
				x = min(x, width - 1)
				y = min(y, height - 1)
				row_centers.append((x, y))
			centers.append(row_centers)

		# Extract black/white values at each center using modular function
		frame_grid = np.zeros((grid_rows, grid_cols), dtype=np.uint8)
		for i, row in enumerate(centers):
			for j, (x, y) in enumerate(row):
				rgb = select_cell_color(frame, x, y)
				frame_grid[i, j] = apply_filter_on_color(rgb)
		all_frames.append(frame_grid.astype(np.uint8))
		frame_count += 1

		# Show progress percentage
		if total_frames > 0:
			percent = (frame_count / total_frames) * 100
			print(f"Progress: {percent:.2f}% ({frame_count}/{total_frames})", end='\r')

	cap.release()

	print()  # Move to next line after progress
	configJson = {
		'name': video_path,
		'grid_rows': grid_rows,
		'grid_cols': grid_cols,
		'frame_width': width,
		'frame_height': height,
		'total_frames': frame_count,
		'fps': fps
	}

	# Save all matrices to JSON file
	output_content = "videoContent.npz"
	output_config = "videoConfig.json"
	with open(output_config, "w") as f:
		json.dump(configJson, f, indent=2)

	# Save all frames as a numpy array
	all_frames_np = np.stack(all_frames)
	np.savez_compressed(output_content, all_frames_np)
	print(f"Saved grid matrices for {frame_count} frames to {output_content} and configuration to {output_config}.")
	print("Done extracting frames.")

if __name__ == "__main__":
	video_path = "earth.mp4"  # Change to your video file path
	extract_frames(video_path)
