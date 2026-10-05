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
  cp -r data_internal "$BACKUP/" 2>/dev/null
  cp _static/data_external/*.csv "$BACKUP/" 2>/dev/null
  cp db.sqlite3 "$BACKUP/" 2>/dev/null
  echo "Local data backed up in $BACKUP"

  # Tell git never to overwrite the data files written on the tablet
  for f in "${C4P_LOCAL_DATA[@]}"; do
    git update-index --skip-worktree "$f" 2>/dev/null
  done

  if git pull --ff-only; then
    # Refresh the shortcuts (in case the scripts moved)
    for s in run upload update; do
      printf '#!/bin/bash\nexec bash "%s/%s.sh" "$@"\n' \
        "$C4P_SCRIPTS" "$s" > "$HOME/$s.sh"
    done
    echo "Update complete."
    echo "Restart oTree (Ctrl+C in session 1, then ./run.sh)."
  else
    echo "UPDATE FAILED. Do not delete anything."
    echo "Send a screenshot of this screen to the Geneva team."
    exit 1
  fi
}

main "$@"
exit
