import numpy as np
import json
import os
import sys

def npz_to_json(npz_file, json_file, config_file='videoConfig.json'):
    # Load videoConfig.json for metadata
    try:
        with open(config_file, 'r') as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    try:
        data = np.load(npz_file)['arr_0']
    except Exception as e:
        print(f"Error loading npz: {e}")
        sys.exit(1)
        
    total_frames = metadata.get('total_frames', data.shape[0])
    frames = []

    for frameId in range(0, total_frames):
        frame_data = data[frameId].tolist()
        frames.append(frame_data)
        
        if total_frames > 0:
            percent = (frameId / total_frames) * 100
            print(f"Progress: {percent:.2f}% ({frameId}/{total_frames})", end='\r')
    
    print(f"Progress: 100.00% ({total_frames}/{total_frames})", end='\r')
    
    # Write to JSON
    with open(json_file, 'w') as f:
        json.dump(frames, f)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert .npz video frames to JSON with metadata.')
    parser.add_argument('--npz_file', default='videoContent.npz', help='Path to the .npz file')
    parser.add_argument('--output_json', default='output.json', help='Path to output JSON file')
    parser.add_argument('--config', default='videoConfig.json', help='Path to config JSON file')
    args = parser.parse_args()
    npz_to_json(args.npz_file, args.output_json, args.config)
