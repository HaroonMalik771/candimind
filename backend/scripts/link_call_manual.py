import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Interview, InterviewResult

def link_call(call_id, candidate_name_fragment):
    db = SessionLocal()
    try:
        # 1. Find Interview (Latest)
        interviews = db.query(Interview).order_by(Interview.id.desc()).all()
        target_interview = None
        for i in interviews:
            if candidate_name_fragment.lower() in i.candidate_name.lower():
                target_interview = i
                break
        
        if not target_interview:
            print(f"❌ Candidate '{candidate_name_fragment}' not found.")
            return

        print(f"✅ Found Interview: {target_interview.candidate_name} (ID: {target_interview.id})")
        
        # 2. Check/Create Result
        result = db.query(InterviewResult).filter(InterviewResult.interview_id == target_interview.id).first()
        
        if not result:
            print("Creating NEW InterviewResult record...")
            result = InterviewResult(
                interview_id=target_interview.id,
                vapi_call_id=call_id,
                transcript="",
                summary="",
                evaluation=None,
                call_duration=0
            )
            db.add(result)
        else:
            print(f"Updating EXISTING InterviewResult (Old Call ID: {result.vapi_call_id})...")
            result.vapi_call_id = call_id
            
        db.commit()
        print(f"✅ Successfully linked Call ID {call_id} to {target_interview.candidate_name}!")
        print("You can now click 'Fetch Results' in the dashboard.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        call_id = sys.argv[1]
        candidate = sys.argv[2]
    else:
        # Fallback / Example
        call_id = "019c48d0-1951-7449-84ea-1f23042c4b46"
        candidate = "john"
        
    print(f"Linking {call_id} to {candidate}...")
    link_call(call_id, candidate)
