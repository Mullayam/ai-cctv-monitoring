# Guide Overview
## 1. System Architecture

- CCTV footage (pre-recorded or real-time)
- Read video from a directory and simulate live streaming.
- Extract frames at specific intervals (e.g., every X seconds) for analysis.
- OpenCV for frame extraction & FFmpeg for video processing (if needed).

## 2. Detection & Classification

### Object Detection & Tracking

- Detect people and objects in the scene.
- Send All Image to AI and detect.
- (Also if needed) YOLOv8 (real-time object detection), Vision Transformer (For advanced image understanding).

### Activity Recognition & Anomaly Detection

- **Loitering Detection**: Track a person’s movement over time near high-value items
- **Unauthorized Access Detection**: Define zones (e.g., restricted areas) and flag unauthorized entries.
- **Queue Length Monitoring:** Count people in queues and classify congestion levels.

## 3. AI Agent

### **Event Classification**:

- Uses LangGraph to analyze detections and decide event severity (normal vs. suspicious).
- Determines if an alert should be triggered or just logged.

 

### Automated Report
- Number of unauthorized access events.Queue congestion trends.Suspicious behavior occurrences.
- Formats reports in JSON

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

 
