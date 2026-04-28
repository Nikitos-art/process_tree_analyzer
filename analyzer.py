# This script iterates over a directory and parses the .evtx files contained in it. The output is 
# the number of distinct event IDs 
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view
import os
# x - number of total events
# y - number of specific events

y = 0
x = 0
event_counts = {} 

for file in os.listdir("logs"):
    path = f"logs/{file}"

    with Evtx(path) as log:
        for record in log.records():
            x += 1
            xml = record.xml()
            
            start_tag = "<EventID"
            end_tag = "</EventID>"
            start_idx = xml.find(start_tag)

            if start_idx != -1:
                start_idx = xml.find(">", start_idx) + 1
                end_idx = xml.find(end_tag, start_idx)
                if end_idx != -1:
                    current_id = xml[start_idx:end_idx].strip()
                    event_counts[current_id] = event_counts.get(current_id, 0) + 1

# Print summary
print("=================" * 5)
print(f"Total records processed: {x}")
print(f"Distinct Event IDs found: {len(event_counts)}\n")

print("Event ID Counts:")
for eid, count in sorted(event_counts.items(), key=lambda kv: int(kv[0])):
    print(f"  {eid}: {count}")
print("=================" * 5)