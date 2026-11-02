"""Campus event registration simulator. Uses fictional sample data only."""
from __future__ import annotations
import csv, json, logging, re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
LOGS = BASE / "logs"
EVENTS_FILE = DATA / "events.json"
REG_FILE = DATA / "registrations.json"
CSV_FILE = DATA / "attendance.csv"
LOGS.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)
logging.basicConfig(filename=LOGS / "application.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def load_json(path: Path, default):
    try:
        with path.open(encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, OSError) as exc:
        logging.error("Could not load %s: %s", path.name, exc)
        print(f"Data file {path.name} is missing or corrupted; using an empty list.")
        return default

def save_json(path: Path, value):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as f: json.dump(value, f, indent=2)

def valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[A-Za-z]{2,}", value.strip()))

def valid_participant_id(value: str) -> bool:
    return bool(re.fullmatch(r"P\d{4}", value.strip().upper()))

def add_event(events, event_id: str, name: str, capacity: int):
    if not event_id.strip() or not name.strip() or capacity < 1: raise ValueError("ID/name required and capacity must be positive")
    if any(e["id"] == event_id.strip().upper() for e in events): raise ValueError("Event ID already exists")
    events.append({"id": event_id.strip().upper(), "name": name.strip(), "capacity": capacity})

def register(events, regs, event_id, participant_id, name, email):
    event_id, participant_id = event_id.strip().upper(), participant_id.strip().upper()
    try:
        if not valid_participant_id(participant_id): raise ValueError("Participant ID must look like P0001")
        if not valid_email(email): raise ValueError("Enter a valid email-like address")
        event = next((e for e in events if e["id"] == event_id), None)
        if event is None: raise ValueError("Event not found")
        if any(r["event_id"] == event_id and r["participant_id"] == participant_id for r in regs): raise ValueError("Duplicate participant/event registration")
        if sum(r["event_id"] == event_id for r in regs) >= event["capacity"]: raise ValueError("Event is full")
        regs.append({"event_id": event_id, "participant_id": participant_id, "name": name.strip(), "email": email.strip(), "registered_at": datetime.now().astimezone().isoformat(timespec="seconds")})
        logging.info("Registration added participant=%s event=%s", participant_id, event_id)
    except ValueError as exc:
        logging.warning("Validation failure event=%s participant=%s: %s", event_id, participant_id, exc)
        raise

def cancel(regs, event_id, participant_id):
    for i, r in enumerate(regs):
        if r["event_id"] == event_id.strip().upper() and r["participant_id"] == participant_id.strip().upper():
            regs.pop(i); logging.info("Registration cancelled participant=%s event=%s", participant_id, event_id); return True
    return False

def export_attendance(events, regs):
    with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["event_id", "event_name", "participant_id", "name", "email", "registered_at"]); w.writeheader()
        for r in regs:
            event = next((e for e in events if e["id"] == r["event_id"]), {"name": "Unknown event"})
            w.writerow({**r, "event_name": event["name"]})

def summary(events, regs):
    for e in events:
        count = sum(r["event_id"] == e["id"] for r in regs)
        print(f"{e['id']} {e['name']}: {count} registered; {e['capacity']-count} seats available")

def main():
    events, regs = load_json(EVENTS_FILE, []), load_json(REG_FILE, [])
    while True:
        print("\n1 Add event  2 Register  3 Cancel  4 List/export  5 Summary  0 Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                add_event(events, input("Event ID: "), input("Event name: "), int(input("Capacity: "))); save_json(EVENTS_FILE, events); print("Event added.")
            elif choice == "2":
                register(events, regs, input("Event ID: "), input("Participant ID (P0001): "), input("Fictional name: "), input("Fictional email: ")); save_json(REG_FILE, regs); print("Registered.")
            elif choice == "3":
                if cancel(regs, input("Event ID: "), input("Participant ID: ")): save_json(REG_FILE, regs); print("Cancelled.")
                else: print("Registration not found.")
            elif choice == "4":
                for r in regs: print(r)
                export_attendance(events, regs); print(f"Attendance exported to {CSV_FILE}")
            elif choice == "5": summary(events, regs)
            elif choice == "0": break
            else: print("Choose a listed option.")
        except (ValueError, EOFError) as exc: print(f"Could not complete: {exc}")

if __name__ == "__main__": main()
