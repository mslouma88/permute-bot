from database import get_agents, get_shift

def find_replacements(date, shift):

    agents = get_agents()

    replacements = []

    for a in agents:

        agent_id = a[2]

        s = get_shift(agent_id, date)

        if not s:

            replacements.append(agent_id)

    return replacements