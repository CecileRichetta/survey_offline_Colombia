#!/bin/bash
# Start the local oTree server. Leave this Termux session open.
source "$(dirname "$0")/config.sh"

if curl -s -o /dev/null "$C4P_URL"; then
  echo "oTree is already running. Nothing to do."
  exit 0
fi

# Ask Android not to put Termux to sleep (Termux only)
command -v termux-wake-lock >/dev/null && termux-wake-lock

cd "$C4P_PROJECT" || exit 1
# Database file on disk, in the project folder
export DATABASE_URL="sqlite:///db.sqlite3"
source "$C4P_VENV/bin/activate"

echo "Starting oTree on $C4P_URL ..."
echo "Keep this session open. To stop oTree: Ctrl+C"
# prodserver writes every answer to disk immediately (db.sqlite3).
# devserver keeps data in memory and can lose it if Termux is killed.
exec otree prodserver "127.0.0.1:$C4P_PORT"
