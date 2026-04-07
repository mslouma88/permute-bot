import pdfplumber
import re

def parse_planning(file):

    planning = []

    with pdfplumber.open(file) as pdf:

        text = ""

        for page in pdf.pages:
            text += page.extract_text()

    agents = re.findall(r'[A-Z]+ [A-Za-z]+', text)

    shifts = re.findall(r'(J\d\d|N\d\d|CP)', text)

    day = 1

    agent_index = 0

    for shift in shifts:

        if shift.startswith("J"):
            shift_type = "DAY"

        elif shift.startswith("N"):
            shift_type = "NIGHT"

        else:
            shift_type = "OFF"

        agent = agents[agent_index % len(agents)]

        planning.append({
            "date": str(day),
            "agent": agent,
            "shift": shift_type
        })

        day += 1
        agent_index += 1

    return planning