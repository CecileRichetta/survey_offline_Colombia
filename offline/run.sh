#!/bin/bash
# Start the local oTree server. Leave this Termux session open.
source "$(dirname "$0")/config.sh"

if curl -s -o /dev/null "$C4P_URL"; then
  echo "oTree is already running. Nothing to do."
  exit 0
fi

cd "$C4P_PROJECT" || exit 1
source "$C4P_VENV/bin/activate"
c4p_make_shortcuts

# This survey version may need a fresh database (new questions).
# Starting it on the old database would break the survey.
DB_NEEDED=$(cat "$C4P_SCRIPTS/DB_VERSION")
DB_HERE=$(cat "$C4P_DB_VERSION_FILE" 2>/dev/null)
if [ -f db.sqlite3 ] && [ "$DB_NEEDED" != "$DB_HERE" ]; then
  echo "This survey version needs a new database on this tablet."
  echo "oTree was NOT started. Type:  ./reset.sh"
  echo "(it sends all data to SwitchDrive first; internet needed)"
  exit 1
fi
[ -f db.sqlite3 ] || echo "$DB_NEEDED" > "$C4P_DB_VERSION_FILE"

# Secret key of this tablet, created once (the repository is public)
if [ ! -s "$C4P_KEY_FILE" ]; then
  python -c "import secrets; print(secrets.token_urlsafe(32))" > "$C4P_KEY_FILE"
  chmod 600 "$C4P_KEY_FILE"
fi
export OTREE_SECRET_KEY=$(cat "$C4P_KEY_FILE")

# Ask Android not to put Termux to sleep (Termux only)
command -v termux-wake-lock >/dev/null && termux-wake-lock

# Database file on disk, in the project folder
export DATABASE_URL="sqlite:///db.sqlite3"

echo "Starting oTree on $C4P_URL ..."
echo "Keep this session open. To stop oTree: Ctrl+C"
# prodserver writes every answer to disk immediately (db.sqlite3).
# devserver keeps data in memory and can lose it if Termux is killed.
exec otree prodserver "127.0.0.1:$C4P_PORT"
