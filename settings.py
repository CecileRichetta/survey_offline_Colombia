from os import environ

# Offline version (tablets). The database is set by offline/run.sh,
# and the admin password / secret key come from offline/config.sh and the tablet.

ROOMS = [
    dict(
        name="C4PTHP_COL",
        display_name="C4PTHP_COL",
        participant_label_file="_rooms/participant_label_colombia.txt",  # change when final study to _inc
        use_secure_urls=False  # safe here: oTree only listens on the tablet itself (127.0.0.1)
    )
#    dict(
#        name="C4PTHP_COL_TRAINING_1",
#        display_name="C4PTHP_COL_TRAINING_1",
#        participant_label_file="_rooms/participant_label_colombia.txt",  # change when final study to _inc
#        use_secure_urls=False
#    ),
#    dict(
#        name="C4PTHP_COL_TRAINING_2",
#        display_name="C4PTHP_COL_TRAINING_2",
#        participant_label_file="_rooms/participant_label_colombia.txt",  # change when final study to _inc
#        use_secure_urls=False
#    ),
]

SESSION_CONFIGS = [
    dict(
        name='session_C4P_SPANISH_w1',
        app_sequence=[
            'app_1_esp', 'app_2_esp', 'app_3_esp', 'app_4_esp', 'app_5_esp', 'app_6_esp',
            'app_7_esp', 'app_8_esp', 'app_9_esp', 'app_11_esp'
        ],
        num_demo_participants=6
    ),
    dict(
        name='session_C4P_SPANISH_w2',
        app_sequence=[
            'app_1_esp', 'app_2_esp', 'app_3_esp', 'app_4_esp', 'app_5_esp', 'app_6_esp',
            'app_7_esp', 'app_8_esp', 'app_9_esp', 'app_11_esp'
        ],
        num_demo_participants=6,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'supervisor','enumerator',
    'dropout', 'participation_fee',
    'group', 'military_binary', 'etv', 'treatment_hope', 'side_ultimatum', 'treatment_other',
    'sample',
    'decision_UG', 'decision_PG',
    'other_UG_decision', 'other_PG_decision',
    'payoff_UG', 'payoff_PG',
    'total_payoff_token', 'payoff_games', 'total_compensation',
    'payment_platform', 'payment_phone', 'id_number', 'payment_address',
    'recall_phone',
]

SESSION_FIELDS = []

LANGUAGE_CODE = 'es'
REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

DEMO_PAGE_INTRO_HTML = """ """
# Random key created on each tablet by offline/run.sh (this repository is public)
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'dev-only-not-secret')
