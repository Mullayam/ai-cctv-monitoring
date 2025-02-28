import argparse
from src.frame_extractor import extract_frames
from pathlib import Path
from src.ai_integration import send_to_ai

VIDEO_DIR = "data/raw_videos"
OUTPUT_DIR = "data/detected_frames"

def main():
    
    # Create Path objects
    input_dir = Path(VIDEO_DIR)
    output_dir = Path(OUTPUT_DIR)
    
    # Ensure input directory exists
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist!")
        return
    
    # Process all videos
    video_count = 0
    for video_file in input_dir.glob("*"):
        if video_file.suffix.lower() in ['.mp4', '.avi', '.mov']:
            print(f"Processing video: {video_file.name}")
            extract_frames(str(video_file), str(output_dir / video_file.stem),  extract_fps=False)
            video_count += 1
    
    print(f"\nProcessing complete!")
    print(f"Processed {video_count} videos")
    print(f"Extracted frames are saved in: {output_dir}")
     
    # Use extracted frames and send them to GPT or Grok AI/Gemini

    for frame_dir in output_dir.glob("*"):
        if frame_dir.is_dir():
            print(f"Sending frames from {frame_dir.name} to AI service")
            send_to_ai(str(frame_dir))

if __name__ == "__main__":
    main()
