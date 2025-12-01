# Universal Advocate: AI Dispute Resolver 🛡️

![Universal Advocate Banner](https://via.placeholder.com/1200x300?text=Universal+Advocate:+AI+Dispute+Resolver)

**Agents Intensive - Capstone Project Submission**
*Track: Agents for Good / Concierge Agents*

---

## 📋 Executive Summary
**Universal Advocate** is an intelligent multi-agent system designed to automate consumer dispute resolution. Unlike standard chatbots, this system actively researches refund policies, verifies their authenticity, and drafts professional "Golden Rules" legal demand letters. It empowers everyday people to resolve disputes with airlines, retailers, and service providers without the stress of manual negotiation.

## 🧐 Problem Statement
**The Refund Gap**: Billions of dollars in valid refunds go unclaimed every year because the process is intentionally difficult.

*   **Complexity**: Finding the specific refund policy for a specific scenario (e.g., "flight delayed by 4 hours") is tedious.
*   **Bureaucracy**: Writing a formal, legally sound demand letter requires time and expertise most consumers lack.
*   **Power Imbalance**: Large corporations rely on consumer fatigue to avoid paying out.

## 💡 Solution: The "Universal Advocate" Architecture
We solve this by implementing a Multi-Agent System that acts as your personal consumer champion.

### Core Agents
*   **🕵️ Intake Agent**: Analyzes your issue to extract key facts (Amount, Date, Transaction ID).
*   **📚 Researcher Agent**: Scans company policies to find the specific clause that guarantees your refund.
*   **⚖️ Verifier Agent**: Checks the credibility of the policy source to ensure your argument is bulletproof.
*   **📝 Writer Agent**: Auto-generates a "Golden Rules" compliant Legal Demand Letter ready to send.

## 🏗️ Technical Implementation
This project demonstrates advanced agentic patterns:
*   **Multi-Agent Orchestration**: A central Orchestrator manages hand-offs.
*   **Tool Use**: Google Search for real-time statute lookup.
*   **Model**: Powered by **Gemini 2.0 Flash** for high speed and reasoning capability.

## 🚀 Installation & Usage

### Prerequisites
*   Python 3.9+
*   Google Gemini API Key

### Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/devils-advocate.git
    cd devils-advocate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure Environment:
    Rename `.env.example` to `.env` and add your API key:
    ```env
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

### Running the Agent
**Web Interface (Recommended)**:
```bash
streamlit run app.py
```

## 📊 Real-World Scenario: The Security Deposit
**User**: "My landlord won't return my deposit."

1.  **Intake**: Asks for lease dates and move-out photos.
2.  **Research**: Identifies State Law requiring itemized deductions within 21 days.
3.  **Outcome**: User gets a generated Demand Letter citing the specific code.

---
*Project Status: Python AI Model License*
