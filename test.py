import yaml
import sys
try:
    with open(sys.argv[1], 'r') as f:
        yaml.safe_load(f)
    print("Valid YAML!")
except Exception as e:
    print(f"Invalid YAML: {e}")
