#!/bin/bash
# Starts the survey in the background, creates the session if needed and
# opens the page where the enumerator enters the ID.
source "$(dirname "$(readlink -f "$0")")/config.sh"

# First use of this tablet: ask for the enumerator code.
# ("Actualizar" also uses this script, and must not ask for it.)
if [ "$1" != "--sin-navegador" ]; then
  c4p_ask_enumerator || exit 1
fi

c4p_start_otree
case $? in
  0) ;;
  2)
    echo "Esta versión de la encuesta necesita una base de datos nueva."
    echo "Con internet, vuelva al menú y escriba 3 (Actualizar)."
    exit 1 ;;
  *)
    echo "LA ENCUESTA NO PUDO INICIAR."
    echo "Tome una foto de esta pantalla y envíela a su supervisor."
    exit 1 ;;
esac

if ! c4p_ensure_session; then
  echo "LA ENCUESTA NO PUDO PREPARARSE."
  echo "Tome una foto de esta pantalla y envíela a su supervisor."
  exit 1
fi

[ "$1" = "--sin-navegador" ] && exit 0

echo "Abriendo la encuesta en el navegador..."
command -v termux-open-url >/dev/null && termux-open-url "$C4P_ROOM_URL"
echo
echo "Si el navegador no se abre, ábralo usted y escriba:"
echo "  localhost:$C4P_PORT/room/$C4P_ROOM"
