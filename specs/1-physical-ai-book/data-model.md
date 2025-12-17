# Data Model: Physical AI & Humanoid Robotics Book

## Entity: Book
**Description**: The complete Physical AI & Humanoid Robotics educational resource
**Fields**:
- id: string (unique identifier for the book)
- title: string (Physical AI & Humanoid Robotics)
- version: string (semantic versioning)
- author: string (author or institution)
- created_date: date (creation timestamp)
- last_updated: date (last modification timestamp)
- modules: [Module] (collection of modules)

## Entity: Module
**Description**: A major section of the book covering a specific topic area
**Fields**:
- id: string (unique identifier for the module)
- title: string (descriptive title of the module)
- description: string (brief overview of the module content)
- position: integer (order in the book sequence)
- learning_outcomes: [string] (measurable outcomes for the module)
- prerequisites: [string] (required knowledge/skills)
- chapters: [Chapter] (collection of chapters within the module)
- duration: string (estimated time to complete)
- technology_stack: [string] (technologies covered in the module)

**Validation Rules**:
- position must be unique within the book
- title must be 5-100 characters
- learning_outcomes must contain at least 2 outcomes
- technology_stack must contain valid technology names

## Entity: Chapter
**Description**: A document file representing a section of a module
**Fields**:
- id: string (unique identifier for the chapter)
- module_id: string (reference to parent module)
- title: string (chapter title)
- filename: string (MDX filename without extension)
- sidebar_position: integer (position in sidebar navigation)
- content: string (the actual MDX content)
- learning_objectives: [string] (specific objectives for this chapter)
- exercises: [Exercise] (practice activities)
- code_examples: [CodeExample] (embedded code examples)
- tags: [string] (metadata tags for search and organization)

**Validation Rules**:
- sidebar_position must be unique within the module
- filename must follow kebab-case format
- content must be valid MDX format
- title must be 5-80 characters

## Entity: CodeExample
**Description**: A code snippet with explanation and context
**Fields**:
- id: string (unique identifier for the example)
- chapter_id: string (reference to parent chapter)
- title: string (brief description of the example)
- language: string (programming language or format)
- code: string (the actual code content)
- explanation: string (detailed explanation of the code)
- expected_output: string (what the code should produce)
- prerequisites: [string] (requirements to run the example)

**Validation Rules**:
- language must be a supported syntax highlighting language
- code must be syntactically valid for the specified language
- explanation must be 20-500 characters

## Entity: Exercise
**Description**: A practical task for students to practice concepts
**Fields**:
- id: string (unique identifier for the exercise)
- chapter_id: string (reference to parent chapter)
- title: string (brief title of the exercise)
- description: string (detailed description of the task)
- difficulty: string (beginner, intermediate, advanced)
- estimated_time: string (time needed to complete)
- requirements: [string] (software/hardware needed)
- expected_outcome: string (what should be achieved)
- hints: [string] (optional guidance for students)
- solution: string (reference solution, optional)

**Validation Rules**:
- difficulty must be one of: beginner, intermediate, advanced
- estimated_time must follow format: "X hours" or "X minutes"
- description must be 50-500 characters

## Entity: LearningObjective
**Description**: A measurable outcome that students should achieve
**Fields**:
- id: string (unique identifier for the objective)
- parent_id: string (reference to module or chapter)
- parent_type: string (module or chapter)
- text: string (the objective statement)
- measurable: boolean (can the outcome be measured)
- type: string (knowledge, skill, application)

**Validation Rules**:
- text must follow SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound)
- measurable must be true for all objectives
- type must be one of: knowledge, skill, application

## Entity: Assessment
**Description**: Evaluation method for measuring student progress
**Fields**:
- id: string (unique identifier for the assessment)
- module_id: string (reference to the module being assessed)
- title: string (title of the assessment)
- type: string (quiz, project, practical, peer-review)
- weight: number (percentage of total grade, 0-100)
- criteria: [string] (grading criteria)
- duration: string (time allowed for completion)
- pass_threshold: number (minimum score required, 0-100)

**Validation Rules**:
- type must be one of: quiz, project, practical, peer-review
- weight must be between 0 and 100
- pass_threshold must be between 0 and 100

## Entity: Technology
**Description**: A technology or tool covered in the book
**Fields**:
- id: string (unique identifier for the technology)
- name: string (full name of the technology)
- version: string (recommended version)
- purpose: string (primary use case in robotics)
- platform: string (operating system requirements)
- installation_guide: string (reference to setup instructions)
- modules: [string] (list of module IDs that use this technology)

**Validation Rules**:
- name must be unique
- version must follow semantic versioning or be "latest stable"
- platform must be a valid OS identifier

## Relationships

### Book to Module
- Book (1) → Module (Many)
- Book contains multiple modules in a specific sequence

### Module to Chapter
- Module (1) → Chapter (Many)
- Module contains multiple chapters that build on each other

### Chapter to CodeExample
- Chapter (1) → CodeExample (Many)
- Chapter may contain multiple code examples

### Chapter to Exercise
- Chapter (1) → Exercise (Many)
- Chapter may contain multiple exercises

### Module to LearningObjective
- Module (1) → LearningObjective (Many)
- Module has multiple learning objectives

### Module to Assessment
- Module (1) → Assessment (Many)
- Module may have multiple assessments

## State Transitions

### Chapter States
- draft → review → approved → published
- draft: Initial content creation
- review: Content under review for quality and accuracy
- approved: Content reviewed and approved for publication
- published: Content published and available to students

### Module States
- planned → in-progress → review → complete
- planned: Module structure defined
- in-progress: Content being developed
- review: Module under comprehensive review
- complete: Module finished and ready for publication

## Validation Rules Summary

1. **Uniqueness**: All ID fields must be unique across their entity type
2. **Content Quality**: All content must adhere to the book's quality standards
3. **Technical Accuracy**: Code examples and technical content must be validated
4. **Progressive Complexity**: Content must build appropriately from basic to advanced
5. **Cross-Module Consistency**: Terminology and concepts must be consistent across modules
6. **Accessibility**: Content must be suitable for the target audience level