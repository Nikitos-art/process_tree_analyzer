from Evtx.Evtx import Evtx
import os
import xml.etree.ElementTree as ET
from collections import defaultdict


class ProcessTreeAnalyzer:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.total_records = 0
        self.event_counts = {}
        self.process_tree = defaultdict(list)
        self.process_info = {}

    def analyze(self):
        for file in os.listdir(self.log_dir):
            path = os.path.join(self.log_dir, file)

            with Evtx(path) as log:
                for record in log.records():
                    self.total_records += 1
                    xml = record.xml()

                    self._count_event_id(xml)
                    self._extract_process_data(xml)

    def _count_event_id(self, xml):
        start_tag = "<EventID"
        end_tag = "</EventID>"

        start_idx = xml.find(start_tag)
        if start_idx != -1:
            start_idx = xml.find(">", start_idx) + 1
            end_idx = xml.find(end_tag, start_idx)

            if end_idx != -1:
                event_id = xml[start_idx:end_idx].strip()
                self.event_counts[event_id] = self.event_counts.get(event_id, 0) + 1

    def _extract_process_data(self, xml):
        try:
            root = ET.fromstring(xml)
            ns = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}

            pid, ppid, pname, cmd = None, None, None, None

            for d in root.findall(".//ns:EventData/ns:Data", namespaces=ns):
                name = d.attrib.get("Name", "").lower()
                val = d.text

                if name in ["newprocessid", "processid"]:
                    pid = val
                elif name == "parentprocessid":
                    ppid = val
                elif name in ["newprocessname", "image", "processname"]:
                    pname = val
                elif name == "commandline":
                    cmd = val

            if pid and ppid:
                self.process_tree[ppid].append(pid)
                self.process_info[pid] = {
                    "name": pname or "Unknown",
                    "cmd": cmd or "",
                    "ppid": ppid,
                }

        except Exception:
            pass  # silently skip malformed XML

    def get_root_processes(self):
        return [
            pid for pid in self.process_info
            if self.process_info[pid]["ppid"] not in self.process_info
        ]

    def print_summary(self):
        print("=" * 50)
        print(f"Total records processed: {self.total_records}")
        print(f"Distinct Event IDs found: {len(self.event_counts)}\n")

        print("Event ID Counts:")
        for eid, count in sorted(self.event_counts.items(), key=lambda kv: int(kv[0])):
            print(f"  {eid}: {count}")

        print("=" * 50)

    def print_process_trees(self):
        print("\nProcess Tree(s):")
        for root in self.get_root_processes():
            self._print_tree(root, level=0, visited=set())

    def _print_tree(self, pid, level=0, visited=None):
        if pid in visited:
            return

        visited.add(pid)
        proc = self.process_info.get(pid, {"name": "Unknown", "ppid": None})

        indent = " " * (level * 4)
        print(f"{indent}{proc['name']} (PID={pid}, PPID={proc.get('ppid')})")

        for child in self.process_tree.get(pid, []):
            self._print_tree(child, level + 1, visited)



if __name__ == "__main__":
    analyzer = ProcessTreeAnalyzer("logs")
    analyzer.analyze()
    analyzer.print_summary()
    analyzer.print_process_trees()


# from Evtx.Evtx import Evtx
# import os
# import xml.etree.ElementTree as ET
# from collections import defaultdict

# x = 0
# event_counts = {}
# process_tree = defaultdict(list)
# process_info = {}

# # Iterate over all .evtx files
# for file in os.listdir("logs"):
#     path = f"logs/{file}"
#     with Evtx(path) as log:
#         for record in log.records():
#             x += 1
#             xml = record.xml()

#             # Count event IDs (your original logic)
#             start_tag = "<EventID"
#             end_tag = "</EventID>"
#             start_idx = xml.find(start_tag)
#             if start_idx != -1:
#                 start_idx = xml.find(">", start_idx) + 1
#                 end_idx = xml.find(end_tag, start_idx)
#                 if end_idx != -1:
#                     current_id = xml[start_idx:end_idx].strip()
#                     event_counts[current_id] = event_counts.get(current_id, 0) + 1

#             # Try to parse XML for PID/PPID relationships
#             try:
#                 root = ET.fromstring(xml)
#                 ns = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}

#                 pid, ppid, pname, cmd = None, None, None, None
#                 for d in root.findall(".//ns:EventData/ns:Data", namespaces=ns):
#                     name = d.attrib.get("Name", "").lower()
#                     val = d.text
#                     if name in ["newprocessid", "processid"]:
#                         pid = val
#                     elif name in ["parentprocessid"]:
#                         ppid = val
#                     elif name in ["newprocessname", "image", "processname"]:
#                         pname = val
#                     elif name == "commandline":
#                         cmd = val

#                 # Only record if we have both PID and PPID
#                 if pid and ppid:
#                     process_tree[ppid].append(pid)
#                     process_info[pid] = {
#                         "name": pname or "Unknown",
#                         "cmd": cmd or "",
#                         "ppid": ppid,
#                     }

#             except Exception:
#                 continue

# # Print summary
# print("=================" * 5)
# print(f"Total records processed: {x}")
# print(f"Distinct Event IDs found: {len(event_counts)}\n")

# print("Event ID Counts:")
# for eid, count in sorted(event_counts.items(), key=lambda kv: int(kv[0])):
#     print(f"  {eid}: {count}")
# print("=================" * 5)


# def print_tree(pid, level=0, visited=None):
#     if visited is None:
#         visited = set()
#     if pid in visited:
#         return
#     visited.add(pid)

#     proc = process_info.get(pid, {"name": "Unknown"})
#     indent = " " * (level * 4)
#     print(f"{indent}{proc['name']} (PID={pid}, PPID={proc.get('ppid')})")

#     for child in process_tree.get(pid, []):
#         print_tree(child, level + 1, visited)

# # Find potential root processes (whose PPID is not seen as any PID)
# root_pids = [pid for pid in process_info if process_info[pid]["ppid"] not in process_info]

# print("\n\nProcess Tree(s):")
# for root in root_pids:
#     print_tree(root)
