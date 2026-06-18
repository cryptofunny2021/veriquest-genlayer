# VeriQuest Architecture

VeriQuest is an AI-powered reputation and campaign evaluation system built on GenLayer.

## Core Flow

1. Campaign creator creates a quest
2. Participants submit content
3. Intelligent Contract evaluates content
4. AI returns a score and reasoning
5. Reputation is updated
6. Best submission is selected
7. Campaign status is determined

## Components

### Quest Engine

Stores:

* Title
* Description
* Category

### Evaluation Engine

Uses GenLayer AI evaluation to score content.

### Reputation Engine

Tracks:

* Successful submissions
* Failed submissions
* Gold rewards
* Silver rewards
* Reputation score

### Campaign Decision Engine

Determines:

* Approved
* Review
* Rejected

based on the highest quality submission.

## Future Expansion

* Escrow rewards
* Multi-user storage
* DAO integration
* Governance
