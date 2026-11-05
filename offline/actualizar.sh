#!/bin/bash
# Download the latest version of the survey from GitHub, keeping the data
# collected on this tablet. If the new version needs a new database, this
# also sends all the data, checks it and creates the new database.
# Then the survey is started again.
# (Everything is inside main() so bash reads the whole script
#  before git pull can change this file.)

main() {
  source "$(dirname "$(readlink -f "$0")")/config.sh"
  cd "$C4P_PROJECT" || exit 1

  echo "ACTUALIZAR (necesita internet)"
  echo

  # Safety copy of the local data before touching anything
  local BACKUP="$HOME/c4p_backup_$(date +%Y-%m-%d_%H%M%S)"
  mkdir -p "$BACKUP"
  chmod 700 "$BACKUP"
  cp -r data_internal "$BACKUP/" 2>/dev/null
  cp _static/data_external/*.csv "$BACKUP/" 2>/dev/null
  cp db.sqlite3 "$BACKUP/" 2>/dev/null

  # Tell git never to overwrite the data files written on the tablet
  for f in "${C4P_LOCAL_DATA[@]}"; do
    git update-index --skip-worktree "$f" 2>/dev/null
  done

  if ! git pull --ff-only; then
    echo
    echo "LA ACTUALIZACIÓN FALLÓ. No borre nada."
    echo "Revise el internet y escriba 3 otra vez. Si sigue fallando,"
    echo "tome una foto de esta pantalla y envíela a su supervisor."
    exit 1
  fi
  # The copy holds personal data: it is not needed any more
  rm -rf "$BACKUP"

  # Re-read config.sh: it may have changed
  source "$C4P_SCRIPTS/config.sh"
  c4p_make_shortcuts
  [ -f "$C4P_VENV/bin/activate" ] || { echo "ERROR: instalación incompleta."; exit 1; }

  if c4p_db_outdated; then
    echo
    echo "Esta versión necesita una base de datos nueva."
    bash "$C4P_SCRIPTS/reiniciar_base.sh" || exit 1
  else
    c4p_stop_otree
  fi

  bash "$C4P_SCRIPTS/iniciar.sh" --sin-navegador || exit 1
  echo
  echo "ACTUALIZACIÓN COMPLETA."
}

main "$@"
exit
