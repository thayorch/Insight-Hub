import os
import json
import requests
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="Issue Tracking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IssueReport(BaseModel): 
    issue: str 
    details: str 
    location: str

# Set up Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_API_KEY"))

# Set up Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
supabase: Client | None = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

# Set up LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

def send_line_message(title: str, level: int, location: str, issue: str, category: str, details: str):
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("LINE Messaging API credentials not set. Message:", title)
        return
        
    url = 'https://api.line.me/v2/bot/message/broadcast'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    
    color = "#ef4444" if level == 3 else "#eab308"
    
    flex_message = {
        "messages": [
            {
                "type": "flex",
                "altText": f"แจ้งเตือนปัญหา Level {level}: {issue}",
                "contents": {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": color,
                        "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "color": "#ffffff",
                                "size": "lg"
                            }
                        ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "ประเด็นปัญหา", "color": "#8c8c8c", "size": "sm"},
                                    {"type": "text", "text": issue, "wrap": True, "weight": "bold"}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "สถานที่", "color": "#8c8c8c", "size": "sm"},
                                    {"type": "text", "text": location, "wrap": True}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "หมวดหมู่", "color": "#8c8c8c", "size": "sm"},
                                    {"type": "text", "text": category, "wrap": True}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "รายละเอียด", "color": "#8c8c8c", "size": "sm"},
                                    {"type": "text", "text": details, "wrap": True}
                                ]
                            }
                        ]
                    }
                }
            }
        ]
    }
    
    try:
        requests.post(url, headers=headers, json=flex_message)
    except Exception as e:
        print("Failed to send LINE message:", e)

import typing_extensions as typing

class AnalysisResult(typing.TypedDict):
    category: str
    base_risk_level: int
    reason: str

SYSTEM_PROMPT = """You are the AI that helps analyze data and report incidents and complaints to the area management system. Your job is to evaluate 'issues' and 'details' provided by users.

The analysis rules are as follows:

1. Category: Select only 1 most appropriate category from the following list:
- "Safety & Persons" (e.g. strangers, quarrels, lost items, suspicious persons) 
- "Structure & Traffic" (e.g. damaged roads, blocked cars, cracked buildings, water leaks) 
- "Common areas" (e.g. dirty bathrooms, broken fitness equipment, not cool air conditioning) 
- "Environment" (e.g. overflowing garbage, bad smells, loud noises, off-road lights)

2. Initial level of severity (base_risk_level): Select only 1 level from the following list:
- 3: (Emergency Threat) An event that directly affects a person's safety. At risk of life, property, or immediate need for assistance (e.g., someone carrying a weapon, car accident, fire) 
- 1: (General problems or compliments) General suggestions. Structural problems that do not cause immediate serious harm or compliment 
*Note: Level 2 is calculated from frequencies in the database. You only output 1 or 3.

3. Reason: Provide a brief explanation for your evaluation.
"""

model = genai.GenerativeModel( 
    'gemini-3.5-flash', 
    system_instruction=SYSTEM_PROMPT
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Issue Tracking API"}

import traceback

@app.post("/api/analyze-issue")
async def analyze_issue(report: IssueReport): 
    prompt = f"Issue: {report.issue}\nDetails: {report.details}" 
    
    try: 
        response = model.generate_content( 
            prompt, 
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": AnalysisResult
            } 
        ) 
        result = json.loads(response.text) 
        
        final_level = result.get('base_risk_level', 1)
        category = result.get('category', 'Unknown')
        
        if supabase:
            # Upgrade Logic: If Level 1, check if > 2 instances in past 24h for same category nearby
            if final_level == 1:
                yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
                
                # Fetch recent issues of the same category
                res = supabase.table('issues').select('location') \
                    .eq('category', category) \
                    .gte('created_at', yesterday) \
                    .execute()
                    
                recent_issues = res.data if res.data else []
                nearby_count = 0
                
                # Helper to extract coords
                def extract_coords(loc_str):
                    if not loc_str: return None
                    try:
                        if '|' in loc_str:
                            loc_str = loc_str.split('|')[-1]
                        parts = loc_str.split(',')
                        if len(parts) >= 2:
                            return (float(parts[0].strip()), float(parts[1].strip()))
                    except ValueError:
                        pass
                    return None
                    
                report_coords = extract_coords(report.location)
                
                for past_issue in recent_issues:
                    loc = past_issue.get('location', '')
                    if loc == report.location:
                        nearby_count += 1
                    else:
                        past_coords = extract_coords(loc)
                        if report_coords and past_coords:
                            # Approximate distance check (0.001 deg is ~111 meters)
                            if abs(report_coords[0] - past_coords[0]) < 0.001 and abs(report_coords[1] - past_coords[1]) < 0.001:
                                nearby_count += 1
                
                if nearby_count >= 2:
                    final_level = 2
                    result['reason'] += f" [Automated Upgrade: This is a recurring issue. Found {nearby_count} similar incidents nearby in the past 24 hours.]"
                    result['base_risk_level'] = 2
            
            # Save the record
            record = {
                'issue': report.issue,
                'details': report.details,
                'location': report.location,
                'category': category,
                'risk_level': final_level,
                'reason': result.get('reason', '')
            }
            supabase.table('issues').insert(record).execute()
        
        result['final_risk_level'] = final_level
        
        # Handle Notifications
        if final_level == 3:
            send_line_message(
                title="🚨 EMERGENCY [Level 3]",
                level=3,
                location=report.location,
                issue=report.issue,
                category=category,
                details=report.details
            )
        elif final_level == 2:
            send_line_message(
                title="⚠️ RECURRING PROBLEM [Level 2]",
                level=2,
                location=report.location,
                issue=report.issue,
                category=category,
                details=report.details
            )

        return result 
    except Exception as e: 
        tb = traceback.format_exc()
        print("ERROR:", tb)
        raise HTTPException(status_code=500, detail=str(e) + " | Traceback: " + tb)

@app.get("/api/issues")
async def get_issues():
    try:
        if supabase:
            res = supabase.table('issues').select('*').order('created_at', desc=True).execute()
            return {"status": "success", "data": res.data}
        else:
            return {"status": "error", "message": "Supabase not configured"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

class IssueUpdate(BaseModel):
    issue: Optional[str] = None
    details: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    risk_level: Optional[int] = None

@app.patch("/api/issues/{issue_id}")
async def update_issue(issue_id: str, update: IssueUpdate):
    try:
        if supabase:
            update_data = {k: v for k, v in update.model_dump().items() if v is not None}
            res = supabase.table('issues').update(update_data).eq('id', issue_id).execute()
            return {"status": "success", "data": res.data}
        else:
            return {"status": "error", "message": "Supabase not configured"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/issues/{issue_id}")
async def delete_issue(issue_id: str):
    try:
        if supabase:
            res = supabase.table('issues').delete().eq('id', issue_id).execute()
            return {"status": "success", "message": "Deleted"}
        else:
            return {"status": "error", "message": "Supabase not configured"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
