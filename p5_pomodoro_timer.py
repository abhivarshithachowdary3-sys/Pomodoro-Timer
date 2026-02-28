import time
import json
import os
from datetime import datetime

sessions_file = "study_sessions.json"

def load_sessions():
    if os.path.exists(sessions_file):
        with open(sessions_file, "r") as file:
            return json.load(file)
    return []

def save_sessions(sessions):
    with open(sessions_file) as file:
        json.dump(sessions, file, indent = 4)


def countdown_timer(duration_minutes, timer_type):
    total_seconds = int(duration_minutes * 60)

    print(f"\n{timer_type.upper()} session started: {duration_minutes} minutes")
    print("Press ctrl + C to cancel")

    try:
        while total_seconds > 0:
            mins = total_seconds // 60
            secs = total_seconds % 60
            print(f"Time remaining: {mins:02d}:{secs:02d}", end="\r")
            time.sleep(1)
            total_seconds -= 1
        
        # Timer completed!
        print("\n" + "="*40)
        print(f"🎉 {timer_type.upper()} SESSION COMPLETE! 🎉")
        print("="*40)
        
        # Simple beep (works on most systems)
        print("\a")  # Terminal beep
        
        return True  # Successfully completed
        
    except KeyboardInterrupt:
        print("\n\nTimer cancelled by user.")
        return False  # Cancelled


def add_session(sunject, duration, session_type):
    session = {
        "Subject": subject,
        "Session Duration": duration,
        "Session Type": session_type,
        "Completed At": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "Date": datetime.now().strftime("%Y-%m-%d")
    }

    sessions.append(session)
    save_sessions(sessions)
    print(f"✓ Session saved: {subject} - {duration} min")

def view_sessions():
    if len(sessions) == 0:
        print("No sessions Yet! Start your first Timer")
        return
    
    print("\n"+"=")
    print("         STUDY SESSION HISTORY")
    print("="*50)

    sessions_by_date = {}
    for session in sessions:
        date = session["date"]
        if date not in sessions_by_date:
            sessions_by_date[date] = []
        sessions_by_date[date].append(session)
    
    # Display by date
    for date in sorted(sessions_by_date.keys(), reverse=True):
        print(f"\n📅 {date}")
        print("-" * 50)
        
        total_work_time = 0
        for session in sessions_by_date[date]:
            time = session["completed_at"].split()[1]  # Get just time part
            icon = "📚" if session["type"] == "work" else "☕"
            
            print(f"  {icon} {time} - {session['subject']} ({session['duration']} min)")
            
            if session["type"] == "work":
                total_work_time += session["duration"]
        
        print(f"\n  Total study time: {total_work_time} minutes")

def show_statistics():
    """Display study statistics"""
    if len(sessions) == 0:
        print("\nNo data yet! Complete some study sessions first.")
        return
    
    print("\n" + "="*50)
    print("             STUDY STATISTICS")
    print("="*50)
    
    # Calculate totals
    total_work_sessions = 0
    total_work_time = 0
    total_break_time = 0
    subjects = {}
    
    for session in sessions:
        if session["type"] == "work":
            total_work_sessions += 1
            total_work_time += session["duration"]
            
            subject = session["subject"]
            if subject not in subjects:
                subjects[subject] = 0
            subjects[subject] += session["duration"]
        else:
            total_break_time += session["duration"]
    
    print(f"\n📊 Total work sessions: {total_work_sessions}")
    print(f"⏱️  Total work time: {total_work_time} minutes ({total_work_time // 60}h {total_work_time % 60}m)")
    print(f"☕ Total break time: {total_break_time} minutes")
    
    if subjects:
        print("\n📚 Time by subject:")
        for subject, minutes in sorted(subjects.items(), key=lambda x: x[1], reverse=True):
            print(f"   {subject}: {minutes} minutes")

# Load existing sessions
sessions = load_sessions()

print("="*40)
print("     POMODORO STUDY TIMER")
print("="*40)

# Main menu loop
while True:
    print("\n--- MENU ---")
    print("1. Start work session (25 min)")
    print("2. Start break (5 min)")
    print("3. View session history")
    print("4. View statistics")
    print("5. Exit")
    
    choice = input("\nChoose option (1-5): ")
    
    if choice == "1":
        subject = input("What are you studying? ")
        
        if subject.strip() == "":
            print("Subject cannot be empty!")
            continue
        
        completed = countdown_timer(25, "work")
        
        if completed:
            add_session(subject, 25, "work")
            
            # Offer break
            take_break = input("\nTake a 5-minute break? (y/n): ").lower()
            if take_break == "y":
                countdown_timer(5, "break")
                add_session("Break", 5, "break")
    
    elif choice == "2":
        completed = countdown_timer(5, "break")
        if completed:
            add_session("Break", 5, "break")
    
    elif choice == "3":
        view_sessions()
    
    elif choice == "4":
        show_statistics()
    
    elif choice == "5":
        print("\n✓ Sessions saved! Keep studying! 📚")
        break
    
    else:
        print("Invalid choice! Please enter 1-5.")
