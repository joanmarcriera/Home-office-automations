#!/usr/bin/env python3
import json
import os
import sys
import argparse

def load_data(filename):
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(data_path, 'r') as f:
        return json.load(f)

def list_tools(tools, category=None):
    print(f"{'Name':<30} | {'Category':<30}")
    print("-" * 70)
    for tool in tools:
        if category and category.lower() not in tool['category'].lower():
            continue
        print(f"{tool['name']:<30} | {tool['category']:<30}")

def show_doc(tool_id, tools):
    tool = next((t for t in tools if t['id'] == tool_id), None)
    if not tool:
        print(f"Error: Tool with id '{tool_id}' not found.")
        return

    doc_path = os.path.join(os.path.dirname(__file__), '..', tool['doc_path'])
    if os.path.exists(doc_path):
        with open(doc_path, 'r') as f:
            print(f.read())
    else:
        print(f"Error: Documentation file not found at {doc_path}")

def main():
    parser = argparse.ArgumentParser(description="AI Hub Tool: Explore home lab tools and documentation.")
    subparsers = parser.add_subparsers(dest="command")

    # List tools command
    list_parser = subparsers.add_parser("list", help="List all tools")
    list_parser.add_argument("--cat", help="Filter tools by category")

    # Doc command
    doc_parser = subparsers.add_parser("doc", help="Show documentation for a specific tool")
    doc_parser.add_argument("id", help="ID of the tool")

    args = parser.parse_args()

    try:
        data = load_data('all_tools.json')
        tools = data['tools']
    except Exception as e:
        print(f"Error loading tools data: {e}")
        sys.exit(1)

    if args.command == "list":
        list_tools(tools, args.cat)
    elif args.command == "doc":
        show_doc(args.id, tools)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
