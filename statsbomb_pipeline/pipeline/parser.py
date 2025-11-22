from helpers.event_parser import parse_event_file

rows = parse_event_file("../data/events/7430.json")

print(f"Extracted actions: {len(rows)}")
print(rows[:5])  # preview first 5 parsed actions
