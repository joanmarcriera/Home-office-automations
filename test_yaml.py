import sys, json
try:
    import json
    lines = sys.stdin.readlines()
    print("Lines loaded")
except Exception as e:
    print(e)
