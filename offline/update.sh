#!/bin/bash
# Download the latest version of the survey from GitHub,
# keeping the data collected on this tablet.
# (Everything is inside main() so bash reads the whole script
#  before git pull can change this file.)

main() {
  source "$(dirname "$0")/config.sh"
  cd "$C4P_PROJECT" || exit 1

  # Safety copy of the local data before touching anything
  local BACKUP="$HOME/c4p_backup_$(date +%Y-%m-%d_%H%M%S)"
  mkdir -p "$BACKUP"
  chmod 700 "$BACKUP"
  cp -r data_internal "$BACKUP/" 2>/dev/null
  cp _static/data_external/*.csv "$BACKUP/" 2>/dev/null
  cp db.sqlite3 "$BACKUP/" 2>/dev/null
  echo "Local data backed up in $BACKUP"

  # Tell git never to overwrite the data files written on the tablet
  for f in "${C4P_LOCAL_DATA[@]}"; do
    git update-index --skip-worktree "$f" 2>/dev/null
  done

  if git pull --ff-only; then
    # Refresh the shortcuts (re-read config.sh: it may have changed)
    source "$C4P_SCRIPTS/config.sh"
    c4p_make_shortcuts
    echo "Update complete."
    if [ -f db.sqlite3 ] && \
       [ "$(cat "$C4P_SCRIPTS/DB_VERSION" 2>/dev/null)" != "$(cat "$C4P_DB_VERSION_FILE" 2>/dev/null)" ]; then
      echo "This version needs a new database: type  ./reset.sh"
      echo "(it sends all data to SwitchDrive first, then stops oTree)."
      echo "Then start oTree again with ./run.sh and create the session."
    else
      echo "Restart oTree (Ctrl+C in session 1, then ./run.sh)."
    fi
  else
    echo "UPDATE FAILED. Do not delete anything."
    echo "Send a screenshot of this screen to the Geneva team."
    exit 1
  fi
}

main "$@"
exit
