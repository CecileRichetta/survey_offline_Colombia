from otree.api import *
from pathlib import Path
import csv

doc = """
oTree app with password protection and CSV data display
"""


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
        label="Password:",
        blank=False
    )


# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = ['password_input']

    def error_message(self, values):
        if values['password_input'] != C.PASSWORD:
            return 'Incorrect password'
        # incorrect password

    def vars_for_template(self):
        return dict(
            title="Information for payment of respondents"
        )
    # data access portal


class Page2(Page):
    def vars_for_template(self):
        # Read CSV data
        csv_data = []
        data_folder = Path("_static/data_internal/payoffs")
        csv_file_path = data_folder / "payoffs.csv"
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_data.append({
                    'participant_label': row.get('participant_label', ''),
                    'date_interview': row.get('date_interview', ''),
                    'participant_number': row.get('participant_number', ''),
                    'participant_cedula': row.get('participant_cedula', ''),
                    'participant_unica': row.get('participant_unica', ''),
                    'participation_fee': row.get('participation_fee'),
                    'payoff_games': row.get('payoff_games', ''),
                    'total_compensation': row.get('total_compensation', '')
                })

        return dict(
            csv_data=csv_data,
            total_records=len(csv_data)
        )


page_sequence = [
    Page1,
    Page2
]