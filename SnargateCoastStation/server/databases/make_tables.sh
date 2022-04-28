#!/bin/sh

cat admin_schema.txt | sqlite3 admin.db
cat calls_schema.txt | sqlite3 calls.db
cat rxtx_schema.txt | sqlite3 rxtx.db
cat check_schema.txt | sqlite3 check.db
cat resolve_schema.txt | sqlite3 resolve.db
cat txpwr_schema.txt | sqlite3 txpwr.db
