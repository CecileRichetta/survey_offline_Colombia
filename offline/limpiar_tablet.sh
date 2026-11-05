#!/bin/bash
# FINAL CLEAN-UP of a tablet, once, after training and before fieldwork.
# Not in the enumerators' menu: run by the support team only.
#   1. Erases all data on the tablet (a copy first goes to SwitchDrive, in
#      C4P_Data/capacitacion/<code>/, apart from the real data)
#   2. Gets the latest version from GitHub
#   3. Erases the enumerator code
# If the copy cannot be sent, nothing is deleted. Safe to run again.
# (Everything is inside main() so bash reads the whole script first.)

main() {
  source "$(dirname "$(readlink -f "$0")")/config.sh"
  cd "$C4P_PROJECT" || exit 1

  local ENUM STAMP SAVE ANSWER f
  ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
  [ -n "$ENUM" ] || ENUM=sin_codigo

  echo "=============================="
  echo "  LIMPIEZA FINAL DE LA TABLET"
  echo "=============================="
  echo
  echo "Se hace UNA SOLA VEZ, ANTES del trabajo de campo."
  echo "Borra TODOS los datos de esta tablet. Necesita internet."
  echo "NUNCA la use si ya hay encuestas reales."
  echo
  read -r -p "Escriba BORRAR (en mayúsculas) para continuar: " ANSWER
  if [ "$ANSWER" != "BORRAR" ]; then
    echo "Cancelado. No se cambió nada."
    exit 1
  fi

  echo
  echo "=== 1/3 Borrar todos los datos ==="
  c4p_stop_otree

  # A copy of the training data, apart from the real data
  STAMP=$(date +%Y-%m-%d_%H%M%S)
  SAVE="$C4P_UPLOAD_ROOT/$STAMP"
  mkdir -p "$SAVE"
  chmod 700 "$C4P_UPLOAD_ROOT"
  [ -f db.sqlite3 ] && cp db.sqlite3 "$SAVE/db_$STAMP.sqlite3"
  for f in data_internal/*/*.csv _static/data_external/treatment_balance.csv; do
    [ -f "$f" ] && cp "$f" "$SAVE/$(basename "$f" .csv)_$STAMP.csv"
  done
  if ! c4p_send_waiting_uploads "capacitacion/$ENUM"; then
    echo
    echo "CANCELADO: no se pudo enviar la copia (¿internet?)."
    echo "NO se borró nada. Revise el internet y repita este paso."
    exit 1
  fi

  # Database and files made by the survey that are not in the repository
  rm -f db.sqlite3 db.sqlite3-*
  rm -f data_internal/payoffs/paid.csv data_internal/tracking/interviews.csv \
        data_internal/*/*_old_*.csv data_internal/*/*.tmp _static/data_external/*.tmp
  # The other data files come back clean from the repository (step 2)
  for f in "${C4P_LOCAL_DATA[@]}"; do
    git update-index --no-skip-worktree "$f" 2>/dev/null
  done
  git checkout -- "${C4P_LOCAL_DATA[@]}"
  # Everything else this tablet kept
  c4p_clear_waiting_uploads
  rm -rf "$HOME"/c4p_backup_*
  rm -f "$C4P_LOG" "$C4P_LAST_UPLOAD_FILE" "$C4P_SESSION_WAVE_FILE"
  echo "Datos borrados."

  echo
  echo "=== 2/3 Última actualización desde GitHub ==="
  # Exactly the version on GitHub, including its clean data files
  if ! git fetch || ! git reset --hard origin/HEAD; then
    echo
    echo "LOS DATOS SE BORRARON, PERO LA ACTUALIZACIÓN FALLÓ."
    echo "Revise el internet y repita este paso."
    exit 1
  fi
  # From now on, git leaves the data written on this tablet alone
  for f in "${C4P_LOCAL_DATA[@]}"; do
    git update-index --skip-worktree "$f" 2>/dev/null
  done
  source "$C4P_SCRIPTS/config.sh"
  c4p_make_shortcuts
  cat "$C4P_SCRIPTS/DB_VERSION" > "$C4P_DB_VERSION_FILE"
  echo "Versión actualizada."

  echo
  echo "=== 3/3 Borrar el código de encuestador ==="
  rm -f "$C4P_ID_FILE"
  echo "Código borrado."

  echo
  echo "LIMPIEZA COMPLETA. No use más esta tablet: entréguela así."
}

main "$@"
exit
