#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if [ -d venv ]; then
  echo -e "${RED}Virtual environment already exists.${NC}"
else
  echo -e "${GREEN}Creating virtual environment...${NC}"
  python3 -m venv venv
  source venv/bin/activate
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}Virtual environment created successfully.${NC}"
  else
    echo -e "${RED}Failed to create virtual environment.${NC}"
    exit 1
  fi
  
  if [ -f requirements.txt ]; then
    echo -e "${GREEN}Installing requirements...${NC}"
    pip install -r requirements.txt
  else
    echo -e "${RED}requirements.txt not found.${NC}"
  fi
fi
