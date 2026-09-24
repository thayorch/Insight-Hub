import os
import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from groq import Groq, RateLimitError
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

# Set up Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or ""
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set. Set it in backend/.env before making requests.")
groq_client = Groq(api_key=GROQ_API_KEY)

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

def is_nearby(loc_a, loc_b):
    coords_a = extract_coords(loc_a)
    coords_b = extract_coords(loc_b)
    if not coords_a or not coords_b:
        return loc_a == loc_b
    # 0.001 deg is ~111 meters
    return abs(coords_a[0] - coords_b[0]) < 0.001 and abs(coords_a[1] - coords_b[1]) < 0.001

SYSTEM_PROMPT = """You are the AI that helps analyze data and report incidents and complaints to the area management system. Your job is to evaluate 'issues' and 'details' provided by users.

The analysis rules are as follows:

1. Category: Select only 1 most appropriate category from the following list:
- "Safety & Persons" (e.g. strangers, quarrels, lost items, suspicious persons) 
- "Structure & Traffic" (e.g. damaged roads, blocked cars, cracked buildings, water leaks) 
- "Common areas" (e.g. dirty bathrooms, broken fitness equipment, not cool air conditioning) 
- "Environment" (e.g. overflowing garbage, bad smells, loud noises, off-road lights)

2. Initial level of severity (base_risk_level): Select only 1 level from the following list. Judge by actual impact, not by keywords alone:

- 3 (สีแดง - Red): The issue directly violates a student's serious, formal RIGHTS (e.g. discrimination, harassment, unfair treatment by staff, being denied a service/benefit they are entitled to, privacy violation, financial exploitation, blocked from an exam or registration without valid reason) OR directly threatens physical SAFETY (e.g. weapon, fire, structural collapse, serious accident, violent assault, life-threatening medical situation). The test: if this is not fixed urgently, would it cause serious damage to the university's image? If yes -> 3.
  Examples: "มีคนแปลกหน้าถือมีดในหอพัก", "นักศึกษาถูกเจ้าหน้าที่ปฏิเสธสิทธิ์สอบโดยไม่มีเหตุผล", "สายไฟฟ้าขาดตกใกล้ทางเดิน", "เกิดเหตุทะเลาะวิวาทมีการทำร้ายร่างกาย"

- 1 (สีเขียว - Green): A general, everyday issue — including minor manners/fairness complaints between students (e.g. queue-cutting, littering, noise, rudeness) that do NOT involve a staff decision, discrimination, or a threat to safety. A single instance does not damage the university's image. Also covers general inconveniences, suggestions, compliments, and routine maintenance.
  Examples: "แอร์ในห้องสมุดไม่เย็น", "ถังขยะเต็มบริเวณโรงอาหาร", "อยากให้เพิ่มที่จอดจักรยาน", "ชมเชยพนักงานทำความสะอาด", "มีคนแซงคิวร้านกาแฟ"

*Note: Level 2 (สีเหลือง - Yellow) means a problem that keeps recurring often — no single instance is an emergency, but the repeating pattern could damage the university's image if left unaddressed. Level 2 is calculated automatically from recurrence in the database, not by you. You must only output 1 or 3; never output 2 yourself.

3. Reason: Provide a brief, specific explanation (in Thai) tying your decision back to the criteria above — which right, safety concern, or image impact applies, or why none does.

4. Duplicate detection: The user message may include a list of EXISTING OPEN ISSUES nearby (each with an id). Compare the new report against them. Only mark it a duplicate if it describes the SAME real-world problem (same underlying incident or ongoing condition) — not merely the same category or same general area. Two different problems at the same location are NOT duplicates. If it is a duplicate, set "duplicate_of" to that issue's id; otherwise set it to null.

Respond with ONLY a JSON object matching this exact shape, no other text:
{"category": string, "base_risk_level": 1 or 3, "reason": string, "duplicate_of": string or null}
"""

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Issue Tracking API"}

import traceback
import time

def generate_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.3
            )
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt * 5)

DUPLICATE_ESCALATE_AT = 3  # report_count reaching this bumps an open Level 1 issue to Level 2

@app.post("/api/analyze-issue")
async def analyze_issue(report: IssueReport):
    try:
        candidates = []
        if supabase:
            res = supabase.table('issues').select('id, issue, details, location, category, risk_level, status, report_count') \
                .in_('status', ['unresolved', 'in_progress']) \
                .execute()
            for row in (res.data or []):
                if is_nearby(row.get('location', ''), report.location):
                    candidates.append(row)

        prompt = f"Issue: {report.issue}\nDetails: {report.details}"
        if candidates:
            candidate_lines = "\n".join(
                f"- id={c['id']}: [{c['category']}] {c['issue']} — {c['details']}" for c in candidates
            )
            prompt += f"\n\nEXISTING OPEN ISSUES NEARBY:\n{candidate_lines}"
        else:
            prompt += "\n\nEXISTING OPEN ISSUES NEARBY: none"

        response = generate_with_retry([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        result = json.loads(response.choices[0].message.content)

        category = result.get('category', 'Unknown')
        final_level = result.get('base_risk_level', 1)
        reason = result.get('reason', '')
        duplicate_id = result.get('duplicate_of')
        matched = next((c for c in candidates if c['id'] == duplicate_id), None) if duplicate_id else None

        if supabase and matched:
            new_count = matched.get('report_count', 1) + 1
            new_level = matched['risk_level']
            if new_level == 1 and new_count >= DUPLICATE_ESCALATE_AT:
                new_level = 2

            update_data = {'report_count': new_count}
            if new_level != matched['risk_level']:
                update_data['risk_level'] = new_level
                update_data['reason'] = matched.get('reason') or ''
                update_data['reason'] += f" [Automated Upgrade: Reported {new_count} times, this is a recurring issue.]"
            supabase.table('issues').update(update_data).eq('id', matched['id']).execute()

            if new_level == 2 and matched['risk_level'] != 2:
                send_line_message(
                    title="⚠️ RECURRING PROBLEM [Level 2]",
                    level=2,
                    location=matched['location'],
                    issue=matched['issue'],
                    category=matched['category'],
                    details=matched['details']
                )

            return {
                'category': matched['category'],
                'base_risk_level': matched['risk_level'],
                'reason': reason,
                'final_risk_level': new_level,
                'duplicate': True,
                'matched_issue': matched['issue'],
                'report_count': new_count
            }

        if supabase:
            record = {
                'issue': report.issue,
                'details': report.details,
                'location': report.location,
                'category': category,
                'risk_level': final_level,
                'reason': reason,
                'report_count': 1
            }
            supabase.table('issues').insert(record).execute()

        result['final_risk_level'] = final_level
        result['duplicate'] = False

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
    status: Optional[str] = None
    assignee: Optional[str] = None

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
