import os
import json
from pathlib import Path
from google import  genai
 
 

LOGS_DIR = "data/reports"         
def send_to_ai(frame_dir):
    # List all frame files in the directory
    frame_files = sorted(Path(frame_dir).glob("*.jpg"))[:5]  # Assuming frames are saved as .jpg files
    
    if not frame_files:
        print(f"No frames found in {frame_dir}")
        return
    
    # Initialize the Gemini client  
    client = genai.Client(api_key="AIzaSyBMIdAYMhyGrzKKSS2mL8_lc-OVOFgTWMw")
    # Prepare the data to send to the AI service
    files = [genai.types.Image.from_file(open(frame, "rb")) for frame in frame_files]
           

    prompt = """You are an advanced AI surveillance system. Analyze the given video frames to detect motion, object presence, and scene classification. Provide a structured JSON output with the following details:

   Output be like this: {
  "analysis": {
    "motion_detected": true, 
    "scene_dynamic": true,
    "queue_detected": true,
    "unauthorized_access_possible": false,    
  },
  "original_data": {    
    "scene_classification": [], // Identify the environment depicted in the frames. Possible classifications include eg. mall,subway,metro,station,roads, etc
    "detected_objects": [] //Identify objects present in the frames e.g People,vehicles,items,objects,security-zone etc
    "suspicious_behavior": {
      "loitering_detected": false,
      "sudden_movement_detected": true
    }
  }
}

    """
    
    response = client.models.generate_content(
    model="gemini-2.0-flash",
     contents=[
         {"role": "system", "parts": [{"text": prompt}]},
        {"role": "user", "parts":  [{"image": files}]}
    ]
)
    
    
    # Send the request to the AI service
    try:
        print("Sending request to AI service...")
        result = response.json()
        print(f"Received result from AI service: {result}")
        
        # Save the result to a JSON file
        result_file = os.path.join(frame_dir, "analysis_result.json")
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Analysis result saved to {result_file}")
    except Exception as e:
        print(f"Failed to get response from AI service. Error: {e}")
    finally:
        # Close all file handles
        for file in files:
            file.close()

if __name__ == "__main__":
    send_to_ai("data/detected_frames")