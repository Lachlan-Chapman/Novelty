#!/bin/bash
pip freeze > dependency/packages.txt
PYTHONPATH=src pydeps src/main.py --rankdir LR -x pygame --noshow --cluster -o dependency/architecture.svg
PYTHONPATH=src pydeps src/main.py --rankdir LR --cluster --max-cluster-size=1000 -x pygame --noshow -o dependency/modules.svg
PYTHONPATH=src pydeps src/main.py --rankdir LR -x pygame --noshow -o dependency/dependencies.svg