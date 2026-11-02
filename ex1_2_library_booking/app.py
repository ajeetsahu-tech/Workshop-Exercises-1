"""Synthetic library seat/equipment booking simulator."""
from __future__ import annotations
import csv, json
from collections import Counter
from datetime import date, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "data" / date.today().isoformat(); OUT.mkdir(parents=True, exist_ok=True)
RESOURCES = [{"id":"SEAT01","type":"seat","location":"Quiet room"},{"id":"PROJ01","type":"projector","location":"Room A"},{"id":"LAP01","type":"laptop","location":"Desk 2"}]
BOOKINGS_FILE = OUT / "bookings.json"; AUDIT = OUT / "audit.jsonl"
def load_bookings():
    try:
        with BOOKINGS_FILE.open(encoding="utf-8") as f: value=json.load(f)
        if not isinstance(value,list): raise ValueError("expected a JSON list")
        return value
    except FileNotFoundError: return []
    except (json.JSONDecodeError, OSError, ValueError) as e:
        print(f"Booking data unavailable ({e}); starting with no bookings."); return []
def save(bookings):
    with BOOKINGS_FILE.open("w",encoding="utf-8") as f: json.dump(bookings,f,indent=2)
def audit(action, booking):
    with AUDIT.open("a",encoding="utf-8") as f: f.write(json.dumps({"at":datetime.now().astimezone().isoformat(timespec="seconds"),"action":action,"booking_id":booking["id"],"resource_id":booking["resource_id"]})+"\n")
def parse_slot(day, start, end):
    d=date.fromisoformat(day); s=datetime.strptime(start,"%H:%M").time(); e=datetime.strptime(end,"%H:%M").time()
    if s>=e: raise ValueError("End time must be after start time")
    return d,s,e
def book(bookings, resource_id, day, start, end, fictional_user):
    resource_id=resource_id.upper()
    if not any(r["id"]==resource_id for r in RESOURCES): raise ValueError("Unknown resource")
    d,s,e=parse_slot(day,start,end)
    if d<date.today(): raise ValueError("Date must be today or later")
    for b in bookings:
        if b["status"]=="active" and b["resource_id"]==resource_id and b["date"]==day:
            bs=datetime.strptime(b["start"],"%H:%M").time(); be=datetime.strptime(b["end"],"%H:%M").time()
            if s<be and bs<e: raise ValueError("Resource already booked for an overlapping slot")
    b={"id":f"B{len(bookings)+1:04d}","resource_id":resource_id,"date":day,"start":start,"end":end,"user":fictional_user.strip(),"status":"active"}
    if not b["user"]: raise ValueError("Fictional name is required")
    bookings.append(b); audit("booked",b); return b
def cancel(bookings, booking_id):
    b=next((x for x in bookings if x["id"]==booking_id.upper() and x["status"]=="active"),None)
    if not b: return False
    b["status"]="cancelled"; audit("cancelled",b); return True
def export_schedule(bookings, day):
    path=OUT/f"schedule-{day}.csv"
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["id","resource_id","date","start","end","user","status"]); w.writeheader(); w.writerows(b for b in bookings if b["date"]==day and b["status"]=="active")
    return path
def report(bookings):
    counts=Counter(b["resource_id"] for b in bookings if b["status"]=="active")
    cancelled=[b for b in bookings if b["status"]=="cancelled"]
    lines=["Resource usage (active bookings):"]+[f"{r['id']} ({r['type']}): {counts[r['id']]}" for r in RESOURCES]+["",f"Cancelled bookings: {len(cancelled)}"]+[f"{b['id']} {b['resource_id']} {b['date']} {b['start']}-{b['end']}" for b in cancelled]
    path=OUT/"usage-report.txt"; path.write_text("\n".join(lines)+"\n",encoding="utf-8"); print("\n".join(lines)); return path
def main():
    bookings=load_bookings()
    while True:
        print("\n1 Catalogue 2 Book 3 Cancel 4 Lookup 5 Daily schedule 6 Report 0 Exit")
        c=input("Choice: ").strip()
        try:
            if c=="1": print(json.dumps(RESOURCES,indent=2))
            elif c=="2":
                b=book(bookings,input("Resource ID: "),input("Date YYYY-MM-DD: "),input("Start HH:MM: "),input("End HH:MM: "),input("Fictional name: ")); save(bookings); print("Booked",b["id"])
            elif c=="3":
                if cancel(bookings,input("Booking ID: ")): save(bookings); print("Cancelled")
                else: print("Active booking not found")
            elif c=="4":
                key=input("Booking ID: ").upper(); print(next((b for b in bookings if b["id"]==key),"Booking not found"))
            elif c=="5":
                day=input("Date YYYY-MM-DD: "); parse_slot(day,"00:00","23:59"); print(export_schedule(bookings,day))
            elif c=="6": report(bookings)
            elif c=="0": break
            else: print("Choose a listed option")
        except (ValueError,EOFError) as e: print("Could not complete:",e)
if __name__=="__main__": main()
