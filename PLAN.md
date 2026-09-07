# Issue Tracking & Management System Development Plan

## 1. Project Overview
The issue reporting and feedback system is designed to manage order within an area (e.g., the common areas of Chiang Mai University) by integrating AI to help filter the urgency and categorize problems, thereby reducing the workload of the team. And increase the speed of problem solving.

## 2. Technology Stack Architecture
* **Frontend (Web/Mobile-responsive):** Nuxt coupled with Tailwind CSS or Vuetify for creating incident reporting forms and dashboards displaying statistics.
* **Backend (API & Logic):** Python FastAPI for managing business logic, such as counting duplicate cases in 24 hours and connecting to various APIs.
* **Database & Auth:** Superbase (PostgreSQL) for storing incident reporting data (Issue Logs), managing user systems (Row-Level Security), and storing GPS coordinates for maps.
* **AI Engine:** Gemini API for processing natural language text and extracting data into JSON (Structured Output).
* **Notification:** LINE Messaging API connected to FastAPI to send notifications to the communications team.

## 3. System Components

### 3.1. User Form
* **Issues** (Issue): **Short problem title**
* **Details:** Further problem description
* **Location:**
* **Dropdown:** List of key incident locations (Latitude/Longitude already linked in Supabase)
* **Text Input ("Other"):** Displayed when the user selects "Other" To specify the location yourself:
* **Date & Time:** The system will auto-timestamp when you click Submit.

### 3.2. Processing and Classification (AI Sorting & Backend Logic)
**AI Processing (Gemini API):**
Receives the message from "Details" and classifies it into 2 parts:
1. **Problem Category:** Safety & Persons / Structure & Traffic / Common Areas / Environment
2. **Basic Risk:** Assess whether it is an emergency (Level 3) or a common incident (Level 1).

**Backend Logic (FastAPI):**
* **Level 3 (Red - Emergency Threat):** If Gemini returns Level 3, the FastAPI system will immediately trigger a Notify Report to the team's LINE account.
* **Level 2 (Yellow - Recurring Problem):** If Gemini returns Level 1, but FastAPI checks the query in PostgreSQL and finds that this point or problem has been reported more than 2-3 times on the same day. The system will upgrade the status to Level 2 and add it to the queue for mention in the Daily Report.
* **Level 1 (Green - Common Problems/Compliments):** Silently recorded in the statistics table.

### 3.3. Dashboard and Map
* **Data Visualization:** Pulls data from the database to create monthly summary graphs, categorized by type.
* **Interactive Map:**
* Main coordinate markers are pulled from the dropdown menu.
* Uses colors to differentiate severity levels (red, yellow, green).
* If the user enters "Other" for a location, the system will list it next to the map for review or use the Geocoding API to find nearby coordinates.