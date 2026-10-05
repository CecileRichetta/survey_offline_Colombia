# Shared settings for the offline tablets (sourced by the other scripts).
# This repository is public: only put values here that are safe to be
# public. The oTree server only listens on the tablet itself (127.0.0.1),
# so the admin password and REST key below cannot be used from outside.
# NEVER put the SwitchDrive link password here: install.sh asks for it.

export OTREE_PRODUCTION=1
export OTREE_AUTH_LEVEL=STUDY
export OTREE_ADMIN_PASSWORD=C4P_colombia
export OTREE_REST_KEY=otree_rest_colombia

C4P_ROOT="$HOME/otree-experiments"
C4P_PROJECT="$C4P_ROOT/survey_offline_Colombia"
C4P_VENV="$C4P_ROOT/venv"
C4P_PORT=8000
C4P_URL="http://127.0.0.1:$C4P_PORT"

# Where the enumerator ID of this tablet is stored (set by install.sh)
C4P_ID_FILE="$HOME/.c4p_enumerator"

# SwitchDrive destination: the shared link to the C4P_Data folder
# (https://drive.switch.ch/index.php/s/<token>). The link only gives
# access to that folder. Its password is asked by install.sh.
C4P_REMOTE=swdrive
SWD_URL="https://drive.switch.ch/public.php/webdav/"
SWD_SHARE_TOKEN="oSnYi965MAQdHkH"

# Files written by the survey on the tablet. They are tracked in git,
# so install.sh tells git to leave the local copies alone on "git pull".
C4P_LOCAL_DATA=(
  data_internal/payoffs/payoffs.csv
  data_internal/payoffs/games_wave_1.csv
  data_internal/for_wave_2/recall.csv
  data_internal/for_wave_2/participant_wave_1.csv
  data_internal/tracking/interviews_per_group.csv
  data_internal/tracking/payment_ngo.csv
  _static/data_external/treatment_balance.csv
)
