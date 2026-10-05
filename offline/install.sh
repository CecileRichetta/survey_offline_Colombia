#!/bin/bash
# One-time installation of the offline C4P survey on a tablet.
# Safe to run again: steps already done are skipped.

main() {
  source "$(dirname "$0")/config.sh"
  local T="$C4P_PROJECT/tablet"

  echo "=== 1/6 Storage access ==="
  if [ ! -d "$HOME/storage" ] && command -v termux-setup-storage >/dev/null; then
    echo "Tap ALLOW on the pop-up."
    termux-setup-storage
    sleep 5
  fi

  echo "=== 2/6 System packages (5-10 min) ==="
  # 'yes ""' answers every question with Enter (= default)
  yes "" | pkg upgrade -y
  pkg install -y python build-essential libffi openssl rust git rclone

  echo "=== 3/6 oTree ==="
  [ -d "$C4P_VENV" ] || python -m venv "$C4P_VENV"
  source "$C4P_VENV/bin/activate"
  python -c "import otree" 2>/dev/null || pip install otree --no-cache-dir
  deactivate

  echo "=== 4/6 Enumerator ID ==="
  local ENUM
  ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
  if [ -n "$ENUM" ]; then
    echo "Enumerator ID already set: $ENUM"
  else
    while true; do
      read -r -p "Enumerator ID (e.g. enumerator_01): " ENUM
      [[ "$ENUM" =~ ^[A-Za-z0-9_-]+$ ]] && break
      echo "Letters, numbers, _ or - only, no spaces."
    done
    echo "$ENUM" > "$C4P_ID_FILE"
  fi

  echo "=== 5/6 SwitchDrive ==="
  # Remove a remote from the old protocol (personal account access)
  if rclone listremotes | grep -qx "$C4P_REMOTE:" && \
     ! rclone config show "$C4P_REMOTE" | grep -q "$SWD_SHARE_TOKEN"; then
    echo "Removing the old SwitchDrive configuration."
    rclone config delete "$C4P_REMOTE"
  fi
  if rclone listremotes | grep -qx "$C4P_REMOTE:"; then
    echo "SwitchDrive already configured."
  else
    local PW
    echo "Paste the SwitchDrive LINK password (nothing is shown):"
    read -r -s PW
    echo
    rclone config create "$C4P_REMOTE" webdav \
      url="$SWD_URL" vendor=owncloud user="$SWD_SHARE_TOKEN" \
      pass="$PW" --obscure >/dev/null
    unset PW
  fi
  if rclone lsd "$C4P_REMOTE:" >/dev/null 2>&1; then
    echo "SwitchDrive connection OK."
  else
    echo "WARNING: cannot reach SwitchDrive (password or internet?)."
    echo "Fix with: rclone config delete $C4P_REMOTE"
    echo "then run this installation again."
  fi

  echo "=== 6/6 Shortcuts ==="
  cd "$C4P_PROJECT" || exit 1
  for f in "${C4P_LOCAL_DATA[@]}"; do
    git update-index --skip-worktree "$f" 2>/dev/null
  done
  # Remove settings from the old manual protocol (now in config.sh)
  [ -f "$HOME/.bashrc" ] && \
    sed -i '/OTREE_\|ENUMERATOR_ID/d' "$HOME/.bashrc"
  for s in run upload update; do
    printf '#!/bin/bash\nexec bash "%s/%s.sh" "$@"\n' "$T" "$s" \
      > "$HOME/$s.sh"
    chmod +x "$HOME/$s.sh"
  done

  echo
  echo "Installation finished."
  echo "  ./run.sh     start oTree (session 1)"
  echo "  ./upload.sh  send the data (session 2)"
  echo "  ./update.sh  get the latest survey version"
}

main "$@"
exit
