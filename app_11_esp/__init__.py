from otree.api import *
import csv
import os
import shutil
import re
from functools import wraps
from pathlib import Path
from datetime import datetime

doc = """
Final app 
- recall -> if no, debrief
- final thank you
"""


class C(BaseConstants):
    NAME_IN_URL = 'app_12_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TEMPLATE_DEBRIEF_FORM = '_static/texts_SPANISH/debrief_form.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payment_phone1 = models.StringField(
        label="11.1. Para el pago de la compensación recibida por la encuesta y las actividades, le enviaremos dinero móvil. "
              "¿A qué número de teléfono podemos enviarle el dinero?",
        # phone number for payment
        blank=False
    )
    payment_email = models.StringField(
        label="11.1.1. Por favor, proporcione una dirección de correo electrónico válida:",
        blank=True
    )
    payment_cedula = models.StringField(
        label="11.1.2. Número de cédula del receptor de la compensación:",
        blank=False
    )
    payment_unica1 = models.StringField(
        label="11.1.3. Este número telefónico está asignado a su cuenta de: Respuesta única",
        choices=[
            ("Daviplata", "1. Daviplata"),
            ("Nequi", "2. Nequi"),
            ("999", "999. Ninguno")
        ],
        widget=widgets.RadioSelect,
        blank=False
    )
    payment_unica2 = models.StringField(
        label="11.1.4. Si la persona responde ninguno preguntar: Respuesta única",
        choices=[
            ("Bono éxito", "1. Bono éxito (encuestador alerta esta opción sólo elegirla si esta en ciudad principal)"),
            ("Efecty", "2. Efecty")
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    recall_firstwave = models.BooleanField(
        label="11.2. Como se mencionó al inicio del cuestionario, este es un estudio en dos partes. "
              "Para comunicarnos con usted, utilizaremos su nombre completo, número de teléfono y una dirección de correo electrónico."
              "¿Le gustaría participar en la segunda etapa de esta encuesta?",
        # As mentionned at the beginning of the questionnaire, this is a two-parts study. Would you like to participate in the second wave of this survey?
        choices=[
            (True, "Sí"),
            (False, "No")
        ],
        widget=widgets.RadioSelect,
        blank=False
    )
    recall_phone1 = models.IntegerField(
        label="11.2.1. Por favor, proporcione un número telefónico de Contacto (puede ser diferente al que entrega de la compensación):",
        blank=True
    )
    recall_email = models.StringField(
        label="11.2.2. Por favor, proporcione una dirección de correo electrónico válida (puede ser diferente al que entrega de la compensación):",
        blank=True
    )
    recall_address = models.StringField(
        label="11.2.3. Por favor, proporcione una dirección geográfica para el recontacto a la encuesta 2:",
        blank=True
    )


# DECORATEUR
# VERSION SIMPLE ET ROBUSTE pour tes fonctions
def simple_safe_operation(func):
    """
    Version simple qui protège juste contre les crashes
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Erreur dans {func.__name__}: {e}")
            # Log l'erreur mais ne crash pas le participant
            return None
    return wrapper

@simple_safe_operation
def export_payoffs_headenumerator(player):
    participant = player.participant
    data_folder = Path("_static/data_internal/payoffs")
    timestamp = datetime.now().strftime("%Y_%m_%d_%H:%M")
    csv_file_path = data_folder / "payoffs.csv"
    temp_file = csv_file_path.with_suffix('.tmp')

    if player.payment_unica1 != "999":
        participant.payment_unica = player.payment_unica1
    else:
        participant.payment_unica = player.payment_unica2

    # Create directory if it doesn't exist
    data_folder.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'participant_label', 'date_interview', 'participant_number',
        'participant_email', 'participant_cedula', 'participant_unica',
        'participation_fee',
        'payoff_games', 'total_compensation'
    ]
    new_row = {
        'participant_label': participant.label,
        'date_interview': timestamp,
        'participant_number': player.payment_phone1,
        'participant_email': player.payment_email,
        'participant_cedula': player.payment_cedula,
        'participant_unica': participant.payment_unica,
        'participation_fee':participant.participation_fee,
        'payoff_games': participant.payoff_games,
        'total_compensation': participant.total_compensation
    }

    try:
        if csv_file_path.exists():
            # Copy original to temp, then append new row
            with open(csv_file_path, 'r', newline='') as original:
                with open(temp_file, 'w', newline='') as temp:
                    temp.write(original.read())
            with open(temp_file, 'a', newline='') as temp:
                writer = csv.DictWriter(temp, fieldnames=fieldnames)
                writer.writerow(new_row)
        else:
            # Create new file with header
            with open(temp_file, 'w', newline='') as temp:
                writer = csv.DictWriter(temp, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(new_row)

        # Replace original with temp
        os.replace(temp_file, csv_file_path)

        player.payment_phone1 = "Anonymous"
        player.payment_email = "Anonymous"
        player.payment_cedula = "Anonymous"
        player.payment_unica1 = "Anonymous"
        player.payment_unica2 = "Anonymous"

    except Exception as e:
        if temp_file.exists():
            os.remove(temp_file)
        print(f"Erreur dans export_payoffs_headenumerator: {e}")
        raise e

@simple_safe_operation
def export_recall(player):
    participant = player.participant
    data_folder = Path("_static/data_internal/for_wave_2")
    csv_file_path = data_folder / "recall.csv"
    temp_file = csv_file_path.with_suffix('.tmp')
    # Create directory if it doesn't exist
    data_folder.mkdir(parents=True, exist_ok=True)
    try:
        new_data = {
            'participant_label': participant.label,
            'participant_name': participant.recontact_1,
            'participant_phone': player.recall_phone1,
            'participant_email': player.recall_email,
            'participant_address': player.recall_address
        }

        # PROTECTION: Écrire dans temp d'abord
        if csv_file_path.exists():
            # Copier l'original vers temp
            shutil.copy2(csv_file_path, temp_file)

            # Ajouter la nouvelle ligne au temp
            with open(temp_file, 'a', newline='') as f:
                # Lire le header du fichier original pour l'ordre des colonnes
                with open(csv_file_path, 'r', newline='') as orig:
                    reader = csv.DictReader(orig)
                    fieldnames = reader.fieldnames

                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(new_data)
        else:
            # Créer nouveau fichier dans temp
            fieldnames = list(new_data.keys())
            with open(temp_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(new_data)

        # Si tout va bien, remplacer l'original
        shutil.move(temp_file, csv_file_path)

        # Si tout va bien, effacer les données
        participant.recontact_1 = "Anonymous"
        player.recall_phone1 = 111
        player.recall_email = "Anonymous"
        player.recall_address = "Anonymous"

    except Exception as e:
        # Nettoyer le fichier temp en cas d'erreur
        if temp_file.exists():
            os.remove(temp_file)
        print(f"Erreur dans export_recall: {e}")
        raise e


# PAGES
class Page1_1(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        participant = player.participant
        # Wave 1: all fields including recall
        if participant.dropout is False and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'payment_phone1',
                'payment_email',
                'payment_cedula',
                'payment_unica1',
                'payment_unica2',
                'recall_firstwave',
                'recall_phone1',
                'recall_email',
                'recall_address'
            ]
        # Wave 2: payment fields only
        elif participant.dropout is False and player.session.config['name'] == "session_C4P_SPANISH_w2":
            return [
                'payment_phone1',
                'payment_email',
                'payment_cedula',
                'payment_unica1',
                'payment_unica2'
            ]
    def before_next_page(player, timeout_happened):
        export_payoffs_headenumerator(player)
        # Only export recall for wave 1
        if player.session.config['name'] == "session_C4P_SPANISH_w1":
            if player.recall_firstwave is True:
                export_recall(player)
    def is_displayed(player):
        participant = player.participant
        return (not participant.dropout) and (
                player.session.config['name'] == "session_C4P_SPANISH_w1" or
                player.session.config['name'] == "session_C4P_SPANISH_w2"
        )
    def error_message(player, values):
        # Validate payment_unica2: required if payment_unica1 == "999"
        if 'payment_unica1' in values and values['payment_unica1'] == '999':
            if not values.get('payment_unica2') or values['payment_unica2'].strip() == '':
                return 'Por favor seleccione una opción de pago alternativa.'
        # Validate recall fields: required if recall_firstwave == True (only in wave 1)
        if 'recall_firstwave' in values and values['recall_firstwave'] == True:
            if not values.get('recall_phone1') or values['recall_phone1'] is None:
                return 'Por favor indique un número telefónico de contacto.'
            if not values.get('recall_email') or values['recall_email'].strip() == '':
                return 'Por favor indique una dirección de correo electrónico.'
            if not values.get('recall_address') or values['recall_address'].strip() == '':
                return 'Por favor indique una dirección geográfica para el recontacto.'

class Page1_2(Page):
    pass
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return not participant.dropout

class Page2(Page):
    pass
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return (not participant.dropout) and (
                (player.field_maybe_none('recall_firstwave') is False and participant.treatment_hope == 1) or
                (player.session.config['name'] == "session_C4P_SPANISH_w2" and participant.treatment_hope == 1)
        )

class Page3(Page):
    pass

page_sequence = [
    Page1_1,
    Page1_2,
    Page2,
    Page3
]
