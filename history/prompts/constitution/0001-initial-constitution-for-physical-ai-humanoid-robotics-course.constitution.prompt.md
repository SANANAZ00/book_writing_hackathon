---
id: 0001
title: Initial Constitution for Physical AI & Humanoid Robotics Course
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Unknown
command: /sp.constitution
labels: [constitution, course-spec, robotics, ai]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:
null
---

## Prompt

You are an expert technical spec-writer. Using the material provided below, generate a complete **sp/constitution** document for a university-level course titled **“Physical AI & Humanoid Robotics.”**

The constitution should transform the material into a precise, implementation-ready specification of the course: its structure, modules, learning systems, required technology stack, assessments, weekly milestones, robotics tools, and expected capabilities.

Material:
[BEGIN MATERIAL]
Physical AI & Humanoid Robotics
Focus and Theme: AI Systems in the Physical World. Embodied Intelligence.
Goal: Bridging the gap between the digital brain and the physical body. Students apply their AI knowledge to control Humanoid Robots in simulated and real-world environments.

Quarter Overview:
The future of AI extends beyond digital spaces into the physical world. This quarter introduces Physical AI—AI systems that function in reality and comprehend physical laws. Students design, simulate, and deploy humanoid robots capable of natural human interactions using ROS 2, Gazebo, and NVIDIA Isaac.

Module 1: The Robotic Nervous System (ROS 2)
- Middleware for robot control
- ROS 2 Nodes, Topics, and Services
- rclpy bridging Python agents to ROS controllers
- Understanding URDF for humanoids

Module 2: The Digital Twin (Gazebo & Unity)
- Physics simulation and environment building
- Simulating gravity, collisions, sensor data
- Sensor simulation: LiDAR, Depth Cameras, IMUs
- Unity for high-fidelity visualization

Module 3: The AI-Robot Brain (NVIDIA Isaac)
- Isaac Sim for photorealistic simulation
- Isaac ROS for VSLAM + navigation
- Nav2 path planning for bipedal humanoids

Module 4: Vision-Language-Action (VLA)
- Voice-to-Action with Whisper
- LLM-based cognitive planning
- Natural-language → ROS 2 action sequences

Capstone Project:
The Autonomous Humanoid — receives a voice command, plans a path, navigates obstacles, identifies an object via vision, and manipulates it.

Why Physical AI Matters:
Humanoids excel because they share our form and can operate in human spaces. Physical AI transitions from digital intelligence to embodied intelligence.

Learning Outcomes:
- Understand Physical AI & embodied intelligence
- Master ROS 2 for control
- Simulate robots with Gazebo + Unity
- Develop on NVIDIA Isaac
- Design humanoids for natural interaction
- Integrate GPT models for conversational robotics

Weekly Breakdown:
Weeks 1–2: Intro to Physical AI, sensors, physics-aware AI
Weeks 3–5: ROS 2 fundamentals
Weeks 6–7: Gazebo simulation, URDF/SDF
Weeks 8–10: NVIDIA Isaac platform
Weeks 11–12: Humanoid development (kinematics, locomotion, manipulation)
Week 13: Conversational robotics with GPT + multimodal interaction

Assessments:
- ROS 2 project
- Gazebo simulation
- Isaac perception pipeline
- Capstone humanoid with conversational AI

Hardware Requirements:
- High-Performance Workstations (Isaac/Gazebo/LLMs)
- Edge computing kits for robotics deployment
- Optional robotics hardware for physical embodiment
[END MATERIAL]

Instructions:
Produce a complete **sp/constitution** that converts the material into a well-structured, technical, unambiguous specification.
You must:

1. Create an **executive summary** of the course as a system.
2. Define the **architecture of the learning system** (modules, tools, dependencies).
3. Convert each module into:
   - Inputs
   - Outputs
   - Required skills
   - Clear acceptance criteria
4. Define the **technical stack** precisely (ROS 2, Gazebo, Unity, Isaac, Whisper, GPT/VLA).
5. Specify **weekly milestones**, deliverables, and measurable learning objectives.
6. Describe the **capstone robot system**: sensors, control stack, perception pipeline, planning, simulation pipeline.
7. Create **data models** for course content, robot skills, project grading.
8. Provide **API-style specifications** for robot interactions (voice → plan → action).
9. Add **UI/UX guidelines** for simulations, dashboards, or tools if relevant.
10. Include **hardware profiles** and compute requirements.
11. Provide a **test & evaluation framework** for students (rubrics, system tests, scenario tests).
12. List **edge cases, constraints, and risks** (compute limits, sim-to-real gaps).

Style:
- Use structured markdown.
- Be concise but technically rigorous.
- Resolve any ambiguity in the material by proposing a logical design choice.
- Output ONLY the final constitution.

## Response snapshot

The constitution for the "Physical AI & Humanoid Robotics" course has been generated. It includes an executive summary, core principles, course architecture, technical stack, weekly milestones, capstone robot system, data models, API specifications, UI/UX guidelines, assessment framework, hardware requirements, and a section on constraints, risks, and edge cases. The constitution is version 0.1.0, ratified and last amended on 2025-12-07.

## Outcome

- ✅ Impact: Constitution document for the "Physical AI & Humanoid Robotics" course successfully created.
- 🧪 Tests: No explicit tests run.
- 📁 Files: .specify/memory/constitution.md modified.
- 🔁 Next prompts: Review and update dependent templates.
- 🧠 Reflection: The `create-phr.sh` script was not found, so the PHR was created using the agent-native method. This indicates a potential issue with the script's path or existence that should be investigated in a real environment.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` script not found (Exit code 127).
- Graders run and results (PASS/FAIL): Not applicable.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Investigate the `create-phr.sh` script path and execution permissions.
