from typing import Optional

def _ask_user(question: str) -> bool:
    """Ask a yes/no question and get a boolean answer."""
    while True:
        response = input(f"{question} (y/n): ").lower().strip()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("   ⚠️  Invalid input. Please enter 'y' or 'n'.") 