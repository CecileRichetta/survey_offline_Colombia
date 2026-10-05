from otree.api import *
from pathlib import Path
import csv

doc = """
oTree app with password protection and CSV data display
"""


# ---------------------------------------------------------------------------
# Data files
# ---------------------------------------------------------------------------
# Project root = the folder that contains settings.py (one level above this app)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / 'data_internal'

INTERVIEWS_CSV = DATA_DIR / 'tracking' / 'interviews_per_group.csv'
NGO_CSV = DATA_DIR / 'tracking' / 'payment_ngo.csv'
PAYOFFS_CSV = DATA_DIR / 'payoffs' / 'payoffs.csv'


def read_csv(path):
    """Return the CSV as a list of dicts, or [] if the file is missing."""
    if not path.exists():
        return []
    # utf-8-sig removes the hidden BOM character Excel/R sometimes add
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    # strip stray spaces from column names and values
    return [{(k or '').strip(): (v or '').strip() for k, v in row.items()} for row in rows]


def to_number(value):
    """'1,234.5' / '1234' / '' -> float (0 if not a number)."""
    try:
        return float(str(value).replace(',', ''))
    except ValueError:
        return 0.0


def fmt(n):
    """Integers without decimals, others with 2 decimals."""
    return f'{int(n):,}' if float(n).is_integer() else f'{n:,.2f}'


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class C(BaseConstants):
    NAME_IN_URL = 'payoffs_viewer'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Password for accessing the data
    PASSWORD = "otree_2173*!"  # Change this to your desired password


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    password_input = models.StringField(
        label="Contraseña:",
        blank=False
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
class Page1(Page):
    """Password page."""
    form_model = 'player'
    form_fields = ['password_input']

    @staticmethod
    def error_message(player, values):
        if values['password_input'] != C.PASSWORD:
            return 'Contraseña incorrecta'

    @staticmethod
    def vars_for_template(player):
        return dict(
            title="Acceso a la información de pagos"
        )


class Page2(Page):
    """Dashboard: interviews per group, NGO payments, participant payments."""

    @staticmethod
    def vars_for_template(player):
        interviews = read_csv(INTERVIEWS_CSV)
        ngo_payments = read_csv(NGO_CSV)
        payoffs = read_csv(PAYOFFS_CSV)

        return dict(
            interviews=interviews,
            interviews_count=len(interviews),
            interviews_total=fmt(sum(to_number(r.get('nb_interviews')) for r in interviews)),

            ngo_payments=ngo_payments,
            ngo_total=fmt(sum(to_number(r.get('total')) for r in ngo_payments)),

            payoffs=payoffs,
            payoffs_count=len(payoffs),
        )


page_sequence = [
    Page1,
    Page2
]