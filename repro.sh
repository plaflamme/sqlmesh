#!/bin/bash

rm -rf examples/sushi/data/*
sqlmesh --log-to-stdout --gateway=duckdb_persistent -p examples/sushi plan --no-prompts --auto-apply | grep -i -e signals -e sushi.customers
echo 'Plan done, waiting 5 minutes for next interval'
sleep 301
echo running
sqlmesh --log-to-stdout --gateway=duckdb_persistent -p examples/sushi run | grep -i -e signals -e sushi.customers
