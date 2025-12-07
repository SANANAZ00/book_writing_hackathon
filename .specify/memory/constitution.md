<!--
Sync Impact Report:
Version change: None → 0.1.0
List of modified principles:
  - PRINCIPLE_1_NAME → Embodied Intelligence
  - PRINCIPLE_2_NAME → ROS 2 Control Mastery
  - PRINCIPLE_3_NAME → Digital Twin Simulation Proficiency
  - PRINCIPLE_4_NAME → NVIDIA Isaac Development
  - PRINCIPLE_5_NAME → Humanoid Interaction Design
  - PRINCIPLE_6_NAME → Conversational Robotics Integration
Added sections: Hardware and Compute Requirements, Constraints, Risks, and Edge Cases
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/sp.phr.md ⚠ pending
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Course Constitution

The "Physical AI & Humanoid Robotics" course bridges the gap between digital AI and physical robotics, enabling students to apply AI knowledge to control humanoid robots in simulated and real-world environments.

## Core Principles

### Embodied Intelligence
Every student will understand Physical AI and AI systems that function in reality, comprehending physical laws.

### ROS 2 Control Mastery
Students MUST design and implement middleware for robot control, including ROS 2 Nodes, Topics, Services, and `rclpy` for Python agent integration.

### Digital Twin Simulation Proficiency
Students MUST build and simulate robot environments using Gazebo and Unity, incorporating physics, sensor data (LiDAR, Depth Cameras, IMUs), and URDF/SDF.

### NVIDIA Isaac Development
Students MUST develop on the NVIDIA Isaac platform, utilizing Isaac Sim for photorealistic simulation, Isaac ROS for VSLAM + navigation, and Nav2 for bipedal humanoid path planning.

### Humanoid Interaction Design
Students MUST design humanoids capable of natural human interactions, focusing on kinematics, locomotion, and manipulation.

### Conversational Robotics Integration
Students MUST integrate GPT models and multimodal interaction for voice-to-action capabilities, LLM-based cognitive planning, and natural-language to ROS 2 action sequences.

## Course Architecture and Technical Stack

### Executive Summary
The course focuses on bridging the gap between digital AI and physical robotics, enabling students to apply AI knowledge to control humanoid robots in simulated and real-world environments.

### Modules
#### Module 1: The Robotic Nervous System (ROS 2)
- **Inputs**: AI knowledge, Python programming.
- **Outputs**: ROS 2 nodes, topics, services, URDF models.
- **Required Skills**: Python, Linux command line, basic robotics concepts.
- **Acceptance Criteria**: Successful deployment of ROS 2 communication, accurate URDF representation of a humanoid.

#### Module 2: The Digital Twin (Gazebo & Unity)
- **Inputs**: ROS 2 knowledge, physics concepts.
- **Outputs**: Simulated environments, sensor data streams.
- **Required Skills**: ROS 2, 3D modeling basics, physics principles.
- **Acceptance Criteria**: High-fidelity physics simulation, accurate sensor data generation within Gazebo/Unity.

#### Module 3: The AI-Robot Brain (NVIDIA Isaac)
- **Inputs**: Simulation data, AI algorithms.
- **Outputs**: VSLAM maps, navigation paths, perception pipelines.
- **Required Skills**: NVIDIA Isaac SDK, computer vision, path planning algorithms.
- **Acceptance Criteria**: Robust VSLAM, efficient path planning for bipedal humanoids.

#### Module 4: Vision-Language-Action (VLA)
- **Inputs**: Natural language commands, visual data, robot state.
- **Outputs**: Cognitive plans, ROS 2 action sequences.
- **Required Skills**: LLM integration, speech recognition (Whisper), natural language processing.
- **Acceptance Criteria**: Accurate voice-to-action translation, effective LLM-based planning.

### Technical Stack
ROS 2, Gazebo, Unity, NVIDIA Isaac Sim, NVIDIA Isaac ROS, Nav2, OpenAI Whisper, GPT (or similar LLMs).

### Weekly Milestones
- **Weeks 1-2**: Intro to Physical AI, sensors, physics-aware AI
- **Weeks 3-5**: ROS 2 fundamentals
- **Weeks 6-7**: Gazebo simulation, URDF/SDF
- **Weeks 8-10**: NVIDIA Isaac platform
- **Weeks 11-12**: Humanoid development (kinematics, locomotion, manipulation)
- **Week 13**: Conversational robotics with GPT + multimodal interaction

### Capstone Robot System
- **Sensors**: LiDAR, Depth Cameras, IMUs, Microphones (for voice commands).
- **Control Stack**: ROS 2, `rclpy`.
- **Perception Pipeline**: NVIDIA Isaac ROS (VSLAM), object detection (vision-based).
- **Planning**: Nav2 (path planning), LLM-based cognitive planning.
- **Simulation Pipeline**: Gazebo, Unity, NVIDIA Isaac Sim.

### Data Models
- **Course Content**: Modules (name, description, learning outcomes, required skills, technical stack), Weeks (topics, deliverables).
- **Robot Skills**: Skill (name, description, required inputs, expected outputs, success criteria).
- **Project Grading**: Rubric (criteria, weighting, assessment method), Submission (student ID, project URL, demo video).

### API-Style Specifications for Robot Interactions
- `POST /robot/command`:
    - **Input**: `{ "voice_command": "string" }`
    - **Output**: `{ "plan": ["string"], "status": "success/failure", "message": "string" }`
    - **Errors**: 400 (Invalid Command), 500 (Execution Failure).
- `GET /robot/status`:
    - **Input**: None
    - **Output**: `{ "current_task": "string", "robot_position": { "x": float, "y": float, "z": float }, "battery_level": float }`

### UI/UX Guidelines
Simulation environments MUST provide clear visualization of robot state, sensor data, and planning trajectories. Dashboards for robot control and monitoring MUST be intuitive.

## Assessment and Evaluation Framework

### Assessments
- ROS 2 project
- Gazebo simulation
- Isaac perception pipeline
- Capstone humanoid with conversational AI

### Test & Evaluation Framework
- **Rubrics**: Detailed rubrics for each assessment, evaluating technical implementation, design choices, and problem-solving.
- **System Tests**: Automated tests for ROS 2 node communication, Gazebo physics accuracy, Isaac navigation, and VLA integration.
- **Scenario Tests**: Real-world (or simulated equivalent) scenarios for the Capstone Project, e.g., "Navigate to the red cube, pick it up, and bring it here."

## Hardware and Compute Requirements

### High-Performance Workstations
Required for NVIDIA Isaac, Gazebo, Unity, and local LLM execution. Minimum 32GB RAM, NVIDIA RTX 3080 (or equivalent) GPU, multi-core CPU.

### Edge Computing Kits
Optional, for real-world robotics deployment (e.g., NVIDIA Jetson series).

### Optional Robotics Hardware
Physical humanoid robots for advanced students to deploy their AI systems.

## Constraints, Risks, and Edge Cases

### Compute Limits
Resource constraints on student workstations may limit simulation complexity and LLM model size.

### Sim-to-Real Gaps
Discrepancies between simulated and real-world physics, sensor noise, and environmental factors can impact real-world deployment. Mitigation: Emphasize robust control and perception.

### API Rate Limits
External LLM APIs may have rate limits, requiring careful design of interaction patterns.

### Data Privacy
Handling of voice commands and user interaction data MUST comply with privacy regulations.

## Governance
This Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan. All PRs/reviews MUST verify compliance. Complexity MUST be justified.

**Version**: 0.1.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
