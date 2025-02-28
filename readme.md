# Guide Overview
## 1. System Architecture

- CCTV footage (pre-recorded or real-time)
- Read video from a directory and simulate live streaming.
- Extract frames at specific intervals (e.g., every X seconds) for analysis.
- OpenCV for frame extraction & FFmpeg for video processing (if needed).

## 2. Detection & Classification

### Object Detection & Tracking

- Detect people and objects in the scene.
- YOLOv8 (real-time object detection), Vision Transformer (For advanced image understanding).

### Activity Recognition & Anomaly Detection

- **Loitering Detection**: Track a person’s movement over time near high-value items
- **Unauthorized Access Detection**: Define zones (e.g., restricted areas) and flag unauthorized entries.
- **Queue Length Monitoring:** Count people in queues and classify congestion levels.

## 3. AI Agent

### **Event Classification**:

- Uses LangGraph to analyze detections and decide event severity (normal vs. suspicious).
- Determines if an alert should be triggered or just logged.

### **Temporal Analysis**:

- Tracks trends over time (e.g., queue congestion spikes).
- Differentiates between short-term anomalies and long-term trends.

### Automated Report

- Number of unauthorized access events.Queue congestion trends.Suspicious behavior occurrences.
- Formats reports in JSON, CSV, or PDF for store managers.

# Workflow Overview

### Step 1: Video Ingestion
- Read video files from a directory.
- Extract frames at regular intervals.

### Step 2: Object Detection & Activity Recognition
- YOLO detects people, queues, and restricted areas.
DeepSORT tracks movement.
- OpenPose / Action Recognition model classifies activities.

### Step 3: Event Classification (LangGraph AI)
- AI agent determines event type (normal, suspicious, alert-worthy).
- Stores structured event data in a database.

### Step 4: Report Generation & Alerts
- Summarizes daily store activity in a structured format.
- Sends real-time alerts if critical events occur.



ai-cctv-monitoring/
│── data                               # Stores all video data, processed frames, logs, and reports  
│   ├── detected_frames                # Contains frames where objects/activities were detected  
│   ├── logs                           # Stores system and processing logs  
│   ├── processed_frames               # Stores frames after preprocessing (e.g., filtered, enhanced)  
│   ├── raw_videos                     # Original unprocessed video files  
│   │   ├── CAM1.mp4                   # Video from Camera 1  
│   │   ├── CAM2.mp4                   # Video from Camera 2  
│   ├── reports                        # Stores generated reports (e.g., activity summaries, security logs)  
│── models                             # Contains AI/ML models for detection and recognition  
│   ├── activity_recognition           # Models for recognizing human activities  
│   ├── object_detection               # Models for detecting objects in videos  
│   │   ├── yolo_detector.py           # YOLO-based object detection implementation  
│── src                                # Source code for different components of the system  
│   ├── activity_recognition           # Code related to recognizing activities in video  
│   │   ├── activity_classifier.py     # Classifies different human activities  
│   │   ├── activity_detection.py      # Detects human activities in video  
│   │   ├── pose_estimation.py         # Estimates human poses from video frames  
│   ├── ai_agent                       # AI-driven decision-making logic  
│   │   ├── ai-agent.py                # Main AI agent for decision-making  
│   │   ├── decision_agent.py          # Implements decision logic based on events  
│   │   ├── event_classifier.py        # Classifies events based on detected activities  
│   ├── object_detection               # Code related to object tracking  
│   │   ├── multi_object_tracker.py    # Tracks multiple objects in real time  
│   ├── video_processing               # Handles video-related operations  
│   │   ├── video_reader.py            # Reads and processes video files  
│   ├── report_generator.py            # Generates reports from detected events and activities  
│   ├── main.py                        # Entry point of the application  
│── readme.md                          # Documentation and project details  
│── requirements.txt                    # List of dependencies for the project  

