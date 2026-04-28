from Evtx.Evtx import Evtx
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from event_ids import EVENT_ID_DESCRIPTIONS

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

    def print_top_events(self, top_n=10):
        print(f"\nTop {top_n} Event IDs:\n")

        sorted_events = sorted(
            self.event_counts.items(),
            key=lambda kv: kv[1],
            reverse=True
        )[:top_n]

        for eid, count in sorted_events:
            desc = EVENT_ID_DESCRIPTIONS.get(eid, "Unknown")
            print(f"{eid}: {count} -> {desc}")

    def print_event_table(self):
        print("\nEvent Summary:\n")

        headers = ["Description", "Event ID", "Count"]
        rows = []

        for eid, count in sorted(self.event_counts.items(), key=lambda kv: int(kv[0])):
            desc = EVENT_ID_DESCRIPTIONS.get(eid, "Unknown")
            rows.append([desc, eid, str(count)])

        col_widths = [
            max(len(row[i]) for row in ([headers] + rows))
            for i in range(len(headers))
        ]

        def format_row(row):
            return " | ".join(
                word.ljust(col_widths[i]) for i, word in enumerate(row)
            )

        print(format_row(headers))
        print("-+-".join("-" * w for w in col_widths))

        for row in rows:
            print(format_row(row))

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
    analyzer.print_event_table()
    analyzer.print_process_trees()