#!/bin/bash
cd "$(dirname "$0")"
./node_modules/.bin/vite --host 0.0.0.0 --port 3000
