#!/bin/bash
# One-time installation of the offline C4P survey on a tablet.
# Safe to run again: steps already done are skipped.

main() {
  source "$(dirname "$(readlink -f "$0")")/config.sh"

  echo "=== 1/4 Programas (5-10 minutos) ==="
  # 'yes ""' answers every question with Enter (= default)
  yes "" | pkg upgrade -y
  pkg install -y python build-essential libffi openssl rust git rclone

  echo "=== 2/4 oTree (puede tardar 15 minutos o más) ==="
  [ -d "$C4P_VENV" ] || python -m venv "$C4P_VENV"
  source "$C4P_VENV/bin/activate"
  python -c "import otree" 2>/dev/null || pip install "otree==6.0.15" --no-cache-dir
  deactivate

  echo "=== 3/4 Código de encuestador ==="
  local ENUM OK
  ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
  if [ -n "$ENUM" ]; then
    echo "Esta tablet ya tiene el código: $ENUM"
  else
    while true; do
      read -r -p "Escriba su código de encuestador (4 dígitos): " ENUM
      if [[ ! "$ENUM" =~ ^[0-9]{4}$ ]]; then
        echo "Deben ser exactamente 4 dígitos."
        continue
      fi
      read -r -p "Usted escribió $ENUM. ¿Es correcto? Escriba s (sí) o n (no): " OK
      [ "$OK" = "s" ] || [ "$OK" = "S" ] && break
    done
    echo "$ENUM" > "$C4P_ID_FILE"
  fi

  echo "=== 4/4 SwitchDrive ==="
  # Remove a remote from the old protocol (personal account access)
  if rclone listremotes | grep -qx "$C4P_REMOTE:" && \
     ! rclone config show "$C4P_REMOTE" | grep -q "$SWD_SHARE_TOKEN"; then
    rclone config delete "$C4P_REMOTE"
  fi
  local PW TRY CONNECTED=no
  if rclone listremotes | grep -qx "$C4P_REMOTE:" && rclone lsd "$C4P_REMOTE:" >/dev/null 2>&1; then
    CONNECTED=yes
  else
    for TRY in 1 2 3; do
      rclone config delete "$C4P_REMOTE" 2>/dev/null
      echo "Pegue la contraseña que le dio su supervisor y presione Enter."
      echo "(mantenga el dedo sobre la pantalla y elija Paste; no se verá nada, es normal)"
      read -r -s PW
      echo
      rclone config create "$C4P_REMOTE" webdav \
        url="$SWD_URL" vendor=owncloud user="$SWD_SHARE_TOKEN" \
        pass="$PW" --obscure >/dev/null
      unset PW
      if rclone lsd "$C4P_REMOTE:" >/dev/null 2>&1; then
        CONNECTED=yes
        break
      fi
      echo "No funcionó (¿contraseña o internet?). Intentemos otra vez."
    done
  fi

  cd "$C4P_PROJECT" || exit 1
  for f in "${C4P_LOCAL_DATA[@]}"; do
    git update-index --skip-worktree "$f" 2>/dev/null
  done
  # Remove settings from the old manual protocol (now in config.sh)
  [ -f "$HOME/.bashrc" ] && sed -i '/OTREE_\|ENUMERATOR_ID/d' "$HOME/.bashrc"
  c4p_make_shortcuts

  echo
  if [ "$CONNECTED" = yes ]; then
    echo "INSTALACIÓN TERMINADA. Conexión con SwitchDrive: OK."
  else
    echo "LA INSTALACIÓN TERMINÓ, PERO SIN CONEXIÓN CON SWITCHDRIVE."
    echo "Avise a su supervisor antes de hacer encuestas."
  fi
  echo
  echo "Último paso en Android:"
  echo "Ajustes > Aplicaciones > Termux > Batería > Sin restricciones"
  echo
  read -r -p "Presione Enter para abrir el menú " _
  [ -t 0 ] && export C4P_MENU=1 && exec bash "$C4P_SCRIPTS/menu.sh"
}

main "$@"
exit
