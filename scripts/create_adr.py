import os
import sys
import re
from datetime import date


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"


def adr_menu():
    print(f"{CYAN}What would you like to do?{RESET}")
    print("1. Create a new ADR")
    print("2. List existing ADRs")
    print("3. Update an ADR")
    print("4. Exit")

    return input(f"{CYAN}-> Select an option (1-4): {RESET}").strip()

def show_adr_status_help():
    print("\n--- ADR Status Help ---")
    print("• Proposed:   The idea is currently under discussion.")
    print("• Accepted:   The decision is approved and being implemented.")
    print("• Rejected:   The idea was dismissed (kept for historical record).")
    print("• Deprecated: No longer recommended, but still in the project.")
    print("• Superseded: This decision has been replaced by a newer ADR.")
    print("-----------------------\n")

def choose_status():
    while (True):
        adr_status_input = f"{CYAN}-> Enter the ADR status (Proposed, Accepted, Rejected, Deprecated, Superseded)\n{YELLOW}/help to get more info about each status{RESET}\n# {RESET}".strip()
        adr_status = input(adr_status_input).strip()
        if not adr_status:
            print(f"{RED}❌ Status cannot be empty.{RESET}")
            sys.exit(1)
        if adr_status.lower() == "/help":
            show_adr_status_help()
            continue
        if adr_status.lower() not in ["proposed", "accepted", "rejected", "deprecated", "superseded"]:
            print(f"{RED}❌ Invalid status. Please enter 'Proposed', 'Accepted','Rejected', 'Deprecated', or 'Superseded'.{RESET}")
            continue
        break
    return adr_status


def create_adr():
    # TITLE   
    title = input(f"{CYAN}-> Enter the ADR title:\n{RESET}# {RESET}").strip()
    if not title:
        print(f"{RED}❌ Title cannot be empty.{RESET}")
        sys.exit(1)

    adr_status = choose_status()
    adr_dir = "docs/adr"
    existing_adrs = [f for f in os.listdir(adr_dir) if f.endswith(".md")]
    next_num = len(existing_adrs)    
    filename = f"{next_num:04d}-{title.lower().replace(' ', '-')}.md"
    filepath = os.path.join(adr_dir, filename)

    template = f"""# ADR-{next_num:04d}: {title.upper()}


**Date:** {date.today()}

## STATUS

{adr_status}

## CONTEXT/PROBLEM

Describe the problem and why we need to make a decision now.


## DECISION

What is the proposed solution?
Why ? What are the key points of the decision?

#### Advantages

- 
- 
#### Disadvantages

- 
- 

## Alternatives

### Option A : 

#### Advantages

- 
- 
#### Disadvantages

- 
- 

### Option B : 

#### Advantages

- 
- 
#### Disadvantages

- 
- 

## CONSEQUENCES

### ✅ Positive

- Benefit 1
- Benefit 2

### ❌ Negative

- Drawback 1
- Drawback 2

## IMPLEMENTATION

- Task 1
- Task 2
- How to use 1

## NOTES

> Notes

"""

    with open(filepath, "w") as f:
        f.write(template)

    print(f"{GREEN}✅ ADR created: {filepath}{RESET}")

def list_adrs():
    adr_dir = "docs/adr"
    adrs = [f for f in os.listdir(adr_dir) if f.endswith(".md")]
    if not adrs:
        print(f"{YELLOW}No ADRs found.{RESET}")
        return
    print(f"{CYAN}--- Existing ADRs ---{RESET}")
    for adr in sorted(adrs):
        print(f"{YELLOW}- {adr}{RESET}")
    print(f"{CYAN}---------------------{RESET}\n")



def get_prev_status(adr_path):
    with open(adr_path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip() == "## STATUS":
            if i + 2 < len(lines):
                return lines[i + 2].strip()
    return "Unknown"

def update_adr():
    print("Type ADR number to update (ex: 0001, 0010...), or type 'exit' to return to the menu.")
    adr_dir = "docs/adr"
    list_adrs()
    adr_to_edit = input(f"{CYAN}-> Enter ADR number to update:\n{RESET}# ").strip()

    adr_numbers = [f.split("-")[0] for f in os.listdir(adr_dir) if f.endswith(".md")]
    if adr_to_edit.lower() == "exit":
        return
    if adr_to_edit not in adr_numbers:
        print(f"{RED}❌ ADR number {adr_to_edit} not found.{RESET}")
        return
    adr_file = next(f for f in os.listdir(adr_dir) if f.startswith(adr_to_edit) and f.endswith(".md"))
    adr_path = os.path.join(adr_dir, adr_file)

    print(f"{adr_path}")
    prev_status = get_prev_status(adr_path)
    print(f"{prev_status}")
    print(f"The previous status of this ADR is: {YELLOW}{prev_status}{RESET}\nChoose the new one...")
    new_status = choose_status()


    with open(adr_path, "r") as f:
        content = f.read()
    pattern = r"(## STATUS\s*\n\n)\w+"
    replacement = r"\1" + new_status
    new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    with open(adr_path, "w") as f:
        f.write(new_content)

    print(f"{GREEN}✅ ADR updated: {adr_path}{RESET}")


def adr_assistant():
    # MENU
    print(f"{PURPLE}=" * 50)
    print(" ADR MANAGER ".center(50, "="), f"{RESET}")
    print(f"{PURPLE}=" * 50, f"{RESET}\n")
    while True:
        choice = adr_menu()
        if choice == "1":
            print(f"{PURPLE}=" * 50)
            print(" CREATE ADR ".center(50, "="), f"{RESET}")
            print(f"{PURPLE}=" * 50, f"{RESET}\n")
            create_adr()
            break
        elif choice == "2":
            print(f"{PURPLE}=" * 50)
            print(" LIST ADRS ".center(50, "="), f"{RESET}")
            print(f"{PURPLE}=" * 50, f"{RESET}\n")
            list_adrs()
        elif choice == "3":
            print(f"{PURPLE}=" * 50)
            print(" UPDATE ADR ".center(50, "="), f"{RESET}")
            print(f"{PURPLE}=" * 50, f"{RESET}\n")
            update_adr()
        elif choice == "4":
            print(f"{GREEN}Exiting...{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}❌ Invalid choice. Please select a valid option (1-4).{RESET}\n")
            

if __name__ == "__main__":
    adr_assistant()