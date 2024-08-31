#!/bin/bash

python3 level2_server.py &

python3 level2_client.py &

wait

echo "complete"

