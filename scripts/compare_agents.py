#!/usr/bin/env python3
import json
import os
import sys
import argparse

def load_agents():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'agents.json')
    with open(data_path, 'r') as f:
        return json.load(f)['agents']

def list_agents(agents, language=None):
    print(f"{'Name':<30} | {'Languages':<30} | {'Superpower'}")
    print("-" * 100)
    for agent in agents:
        if language and language.lower() not in [l.lower() for l in agent['languages']]:
            continue
        langs = ", ".join(agent['languages'])
        print(f"{agent['name']:<30} | {langs:<30} | {agent['superpower']}")

def compare_agents(agents, id1, id2):
    a1 = next((a for a in agents if a['id'] == id1), None)
    a2 = next((a for a in agents if a['id'] == id2), None)

    if not a1:
        print(f"Error: Agent with id '{id1}' not found.")
        return
    if not a2:
        print(f"Error: Agent with id '{id2}' not found.")
        return

    print(f"{'Feature':<15} | {a1['name']:<40} | {a2['name']:<40}")
    print("-" * 100)
    print(f"{'Languages':<15} | {', '.join(a1['languages']):<40} | {', '.join(a2['languages']):<40}")
    print(f"{'Best For':<15} | {a1['best_for']:<40} | {a2['best_for']:<40}")
    print(f"{'Superpower':<15} | {a1['superpower']:<40} | {a2['superpower']:<40}")
    print(f"{'MCP Support':<15} | {str(a1['mcp_support']):<40} | {str(a2['mcp_support']):<40}")
    print(f"{'Repository':<15} | {a1['repository']:<40} | {a2['repository']:<40}")

def show_details(agents, agent_id):
    agent = next((a for a in agents if a['id'] == agent_id), None)
    if not agent:
        print(f"Error: Agent with id '{agent_id}' not found.")
        return

    print(f"Name: {agent['name']}")
    print(f"ID: {agent['id']}")
    print(f"Languages: {', '.join(agent['languages'])}")
    print(f"Best For: {agent['best_for']}")
    print(f"Superpower: {agent['superpower']}")
    print(f"Description: {agent['description']}")
    print(f"MCP Support: {agent['mcp_support']}")
    print(f"Repository: {agent['repository']}")

def main():
    parser = argparse.ArgumentParser(description="Compare and explore AI agent frameworks.")
    subparsers = parser.add_subparsers(dest="command")

    # List command
    list_parser = subparsers.add_parser("list", help="List all agents")
    list_parser.add_argument("--lang", help="Filter by language")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two agents side-by-side")
    compare_parser.add_argument("id1", help="ID of the first agent")
    compare_parser.add_argument("id2", help="ID of the second agent")

    # Details command
    details_parser = subparsers.add_parser("details", help="Show full details for an agent")
    details_parser.add_argument("id", help="ID of the agent")

    args = parser.parse_args()

    try:
        agents = load_agents()
    except Exception as e:
        print(f"Error loading agents data: {e}")
        sys.exit(1)

    if args.command == "list":
        list_agents(agents, args.lang)
    elif args.command == "compare":
        compare_agents(agents, args.id1, args.id2)
    elif args.command == "details":
        show_details(agents, args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
