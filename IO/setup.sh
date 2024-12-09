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
fi
