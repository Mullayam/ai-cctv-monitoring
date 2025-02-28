import cv2
import os
from pathlib import Path

def extract_frames(video_path, output_dir, extract_fps=False):
    """
    Extract frames from video either at 1 FPS or every 30th frame
    Args:
        video_path: Path to the video file
        output_dir: Directory to save extracted frames
        extract_fps: If True, extract 1 frame per second; if False, extract every 30th frame
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while True:
        success, frame = video.read()
        if not success:
            break
            
        # Determine if we should save this frame
        should_save = False
        if extract_fps:
            # Save one frame per second
            if frame_count % int(fps) == 0:
                should_save = True
        else:
            # Save every 30th frame
            if frame_count % 30 == 0:
                should_save = True
                
        if should_save:
            # Generate output filename
            output_filename = f"frame_{frame_count}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the frame
            cv2.imwrite(output_path, frame)
            
        frame_count += 1
    
    # Release the video capture object
    video.release()


def main():
    # Define input and output directories
    input_dir = Path("data/raw_videos")
    output_dir = Path("data/detected_frames")
    
    # Process all videos in the input directory
    for video_file in input_dir.glob("*"):
        if video_file.suffix.lower() in ['.mp4', '.avi', '.mov']:
            print(f"Processing {video_file}")
            extract_frames(
                str(video_file),
                str(output_dir / video_file.stem),
                extract_fps=True  # Set to True for 1 FPS, False for every 30th frame
            )

if __name__ == "__main__":
    main()
