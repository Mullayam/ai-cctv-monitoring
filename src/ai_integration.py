import os
import json
import shutil
import re
from pathlib import Path
from google import genai
from google.generativeai import types
from datetime import datetime
import PIL
LOGS_DIR = Path("data/reports")
PROCESSED_DIR = Path("data/processed_frames")

def process_frame_batches(frame_dir):
    """Process frames in batches of 5 and generate analysis"""
    frame_dir = Path(frame_dir)
    all_responses = []
    batch_number = 1

    # Create directories if they don't exist
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize AI client
    client = genai.Client(api_key="AIzaSyBMIdAYMhyGrzKKSS2mL8_lc-OVOFgTWMw")

    # Get all frame files
    frame_files = sorted(list(frame_dir.glob("*.jpg")))
    
    # Process frames in batches of 5
    for i in range(0, len(frame_files), 5):
        batch_frames = frame_files[i:i+5]
        if not batch_frames:
            break

        print(f"\nProcessing batch {batch_number}...")
        
        # Create batch directory in processed frames
        batch_dir = PROCESSED_DIR / f"batch_{batch_number}"
        batch_dir.mkdir(exist_ok=True)

        # Copy frames to batch directory
        files = []
        for frame in batch_frames:
            # Copy frame to batch directory
            shutil.copy2(frame, batch_dir / frame.name)
            # Create genai.Image object        
            files.append(PIL.Image.open(batch_dir / frame.name))
      

        try:
            # Send to AI
             
            prompt = get_ai_prompt()
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[files, prompt],
            )
            
            # Parse the response text into JSON
            try:
                # Get the text content from response
                response_text = response.text              
            
                # Clean the response text to ensure it's valid JSON
                response_text = response_text.replace("```json", "").replace("```", "").strip()
                
                # Parse the cleaned text into JSON
                result = json.loads(response_text)
                
                # print("Parsed JSON response:", json.dumps(result, indent=2))
                
                # Add batch information
                result['batch_info'] = {
                    'batch_number': batch_number,
                    'frames_processed': [f.name for f in batch_frames],
                    'timestamp': datetime.now().isoformat()
                }
                # result['what_is_in_frame'] =  
                #  
                # Save batch result
                batch_result_file = batch_dir / "analysis.json"
                with open(batch_result_file, 'w') as f:
                    json.dump(result, f, indent=4)
                
                all_responses.append(result)
                print(f"Batch {batch_number} processed and saved successfully!")
                
            except json.JSONDecodeError as je:
                print(f"Failed to parse JSON response: {je}")
                print("Raw response:", response_text)
                
        except Exception as e:
            print(f"Error processing batch {batch_number}: {e}")
        
     
        
        batch_number += 1

    # Generate final report
    generate_summary_report(all_responses, frame_dir.name)

def generate_summary_report(responses, video_name):
    """Generate a summary report from all batch responses"""
    summary = {
        'video_name': video_name,
        'total_batches': len(responses),
        'timestamp': datetime.now().isoformat(),
        'description': "This is a summary report for the video.",
        'overall_analysis': {
            'motion_detected_count': 0,
            'scene_classifications': set(),
            'detected_objects': set(),
            'suspicious_behavior_incidents': 0
        },
        'batch_summaries': []
    }

    # Analyze all responses
    for resp in responses:
        analysis = resp.get('analysis', {})
        original_data = resp.get('original_data', {})
        summary['description'] += resp["what_is_in_frame"]
        # Count motion detections
        if analysis.get('motion_detected'):
            summary['overall_analysis']['motion_detected_count'] += 1
        
        # Collect unique scene classifications
        summary['overall_analysis']['scene_classifications'].update(
            original_data.get('scene_classification', [])
        )
        
        # Collect unique detected objects
        summary['overall_analysis']['detected_objects'].update(
            original_data.get('detected_objects', [])
        )
        
        # Count suspicious behavior incidents
        suspicious = original_data.get('suspicious_behavior', {})
        if suspicious.get('loitering_detected') or suspicious.get('sudden_movement_detected'):
            summary['overall_analysis']['suspicious_behavior_incidents'] += 1
        
        # Add batch summary
        summary['batch_summaries'].append({
            'batch_number': resp['batch_info']['batch_number'],
            'frames_processed': resp['batch_info']['frames_processed'],
            'key_findings': analysis
        })

    # Convert sets to lists for JSON serialization
    summary['overall_analysis']['scene_classifications'] = list(summary['overall_analysis']['scene_classifications'])
    summary['overall_analysis']['detected_objects'] = list(summary['overall_analysis']['detected_objects'])

    # Save summary report
    report_file = LOGS_DIR / f"summary_report_{video_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(summary, f, indent=4)
    
    print(f"\nSummary report generated: {report_file}")

def get_ai_prompt():
    """Return the AI analysis prompt"""
    return """You are an advanced AI surveillance system. Analyze the given video frames to detect motion, object presence, and scene classification. 
    Also Describe what is in the frame.
    You must return only a valid JSON output without any explanation, markdown formatting, or additional text. 
Do not include triple backticks or any extra words. Here is the expected JSON structure with the following details:

    {
        "analysis": {
            "motion_detected": true, 
            "scene_dynamic": true,
            "queue_detected": true,
            "unauthorized_access_possible": false    
        },
        "what_is_in_frame": "", // A whole description of what is in the frame
        "original_data": {    
            "scene_classification": [], // List of scene classifications
            "detected_objects": [],
            "suspicious_behavior": {
                "loitering_detected": false,
                "sudden_movement_detected": true
            }
        }
    }
    """

if __name__ == "__main__":
    process_frame_batches("data/detected_frames")