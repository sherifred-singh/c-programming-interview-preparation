#!/usr/bin/env python3
"""
Automated Daily Module Generator for C Programming Interview Preparation (30-Day Track).
Detects the latest completed day and generates the next day's full suite:
- Compilable C programs with in-depth comments and interview follow-up Q&A
- Module-specific README.md with hardware takeaways and compilation commands
- Root README.md roadmap and index updates
"""

import os
import re
import sys
from curriculum_days_04_to_10 import DAYS_04_TO_10
from curriculum_days_11_to_20 import DAYS_11_TO_20
from curriculum_days_21_to_30 import DAYS_21_TO_30

# Combine all curriculum days
ALL_CURRICULUM = {}
ALL_CURRICULUM.update(DAYS_04_TO_10)
ALL_CURRICULUM.update(DAYS_11_TO_20)
ALL_CURRICULUM.update(DAYS_21_TO_30)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_latest_day():
    """Scans repository root for existing Day-XX directories."""
    max_day = 0
    for item in os.listdir(REPO_ROOT):
        full_path = os.path.join(REPO_ROOT, item)
        if os.path.isdir(full_path):
            match = re.match(r"^Day-(\d+)", item)
            if match:
                day_num = int(match.group(1))
                if day_num > max_day:
                    max_day = day_num
    return max_day


def generate_module_readme(day_info):
    """Generates the README.md content for the day's folder."""
    title = day_info["title"]
    overview = day_info["overview"]
    programs = day_info["programs"]

    lines = [
        f"# {title}\n",
        f"{overview}\n",
        "---\n",
        "## 📋 Program Index & Summary\n",
        "| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |",
        "| :-: | :--- | :--- | :---: | :---: | :--- |",
    ]

    for idx, p in enumerate(programs, 1):
        lines.append(
            f"| **{idx:02d}** | **`{p['filename']}`** | {p['focus']} | {p['time_complexity']} | {p['space_complexity']} | {p['insight']} |"
        )

    lines.append("\n---\n")
    lines.append("## 💡 Embedded Notes & Key Hardware Takeaways\n")

    for idx, p in enumerate(programs, 1):
        lines.append(f"### {idx}. {p['focus']}")
        lines.append(f"- **Key Silicon Insight:** {p['insight']}")
        lines.append(f"- **Technical Design Question:** *{p['follow_up_q']}*")
        lines.append(f"- **Engineering Rationale:** {p['follow_up_a']}\n")

    lines.append("---\n")
    lines.append("## 🛠 How to Compile & Run\n")
    lines.append("```bash")
    lines.append("# Compile all programs in this module with strict C99 warnings")
    for p in programs:
        base_name = p['filename'].replace('.c', '')
        lines.append(f"gcc -Wall -Wextra -std=c99 -pedantic {p['filename']} -o {base_name} && ./{base_name}")
    lines.append("```\n")

    return "\n".join(lines)


def update_root_readme(day_num, day_info):
    """Updates root README.md roadmap table and program index."""
    root_readme_path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.exists(root_readme_path):
        return

    with open(root_readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    folder = day_info["folder_name"]
    title_short = day_info["title"].split(":", 1)[1].strip()
    prog_count = len(day_info["programs"])

    # Update row for Day XX in the table
    # Pattern: | **Day 04** | ... | ⏳ Next Up | or ⏳ Upcoming |
    old_row_pattern = rf"\|\s*\*\*Day {day_num:02d}\*\*\s*\|\s*\*\*([^\*]+)\*\*\s*\|\s*([^\|]+)\|\s*⏳\s*(?:Next Up|Upcoming)\s*\|"
    new_row = f"| **[Day {day_num:02d}](./{folder}/)** | **{title_short}** | \\2| ✅ Complete ({prog_count} Program{'s' if prog_count > 1 else ''}) |"
    
    content = re.sub(old_row_pattern, new_row, content)

    # Next day row set to ⏳ Next Up if exists
    next_day = day_num + 1
    if next_day <= 30:
        next_row_pattern = rf"(\|\s*\*\*Day {next_day:02d}\*\*\s*\|[^\|]+\|[^\|]+\|\s*)⏳ Upcoming(\s*\|)"
        content = re.sub(next_row_pattern, r"\g<1>⏳ Next Up\g<2>", content)

    # Add to Master Program Index if not already present
    day_header = f"### Day {day_num:02d} — {title_short}"
    if day_header not in content:
        index_entries = [f"\n{day_header}"]
        for idx, p in enumerate(day_info["programs"], 1):
            index_entries.append(f"{idx}. **`{p['filename']}`** — {p['focus']}. {p['insight']}")
        
        # Append before compilation section
        comp_marker = "## 🛠 Compilation & Validation"
        if comp_marker in content:
            content = content.replace(comp_marker, "\n".join(index_entries) + "\n\n---\n\n" + comp_marker)

    with open(root_readme_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def main():
    latest_day = find_latest_day()
    next_day = latest_day + 1
    print(f"Current Latest Completed Day: Day {latest_day:02d}")
    print(f"Target Next Day: Day {next_day:02d}")

    if next_day > 30:
        print("🎉 All 30 Days of the Embedded C Interview Preparation Suite are already complete!")
        sys.exit(0)

    if next_day not in ALL_CURRICULUM:
        print(f"Error: Curriculum data for Day {next_day:02d} not found.")
        sys.exit(1)

    day_info = ALL_CURRICULUM[next_day]
    target_dir = os.path.join(REPO_ROOT, day_info["folder_name"])
    os.makedirs(target_dir, exist_ok=True)

    print(f"Creating module: {day_info['folder_name']}")

    # Write C programs
    for p in day_info["programs"]:
        prog_path = os.path.join(target_dir, p["filename"])
        with open(prog_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(p["code"].strip() + "\n")
        print(f" - Created program: {p['filename']}")

    # Write module README.md
    module_readme_path = os.path.join(target_dir, "README.md")
    module_readme_content = generate_module_readme(day_info)
    with open(module_readme_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(module_readme_content)
    print(f" - Created module README: {day_info['folder_name']}/README.md")

    # Update root README.md
    update_root_readme(next_day, day_info)
    print(f" - Updated root README.md roadmap and index")

    # Save commit message for GitHub Actions
    title_short = day_info["title"].split(":", 1)[1].strip()
    commit_msg = f"Day {next_day:02d} - {title_short} interview preparation suite"
    with open(os.path.join(REPO_ROOT, ".current_day_commit_msg"), "w", encoding="utf-8") as f:
        f.write(commit_msg)

    print(f"\n[SUCCESS] Successfully generated Day {next_day:02d}: {title_short}!")


if __name__ == "__main__":
    main()
