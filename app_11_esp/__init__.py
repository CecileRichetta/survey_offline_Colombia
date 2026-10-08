from random import choices

from otree.api import *
import csv
import os
import shutil
import re
from functools import wraps
from pathlib import Path
from datetime import datetime, timezone, timedelta

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
    TZ_COLOMBIA = timezone(timedelta(hours=-5))
    #
    PLATFORM_PAYMENT_1 = [
        ("Daviplata", "Sí, Daviplata"),
        ("Nequi", "Sí, Nequi"),
        ("999", "No tengo ninguna de las dos, se girará a nombre de un tercero"),
    ]
    PLATFORM_PAYMENT_2 = [
        ("Daviplata", "Daviplata"),
        ("Nequi", "Nequi"),
    ]
    CONTACT_SOURCE = [
        (1, "Muestra cartográfica"),
        (2, "Referido de otro encuestado"),
        (3, "Líder o representante comunitario"),
        (4, "Institución (fuerza pública, educativa, gremio)")
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payment_platform_1 = models.StringField(
        label="11.1. Para el pago de la compensación recibida por la encuesta y las actividades, "
              "le enviaremos el dinero de forma electrónica. ¿Cuenta usted con Nequi o Daviplata?",
        # phone number for payment
        choices=C.PLATFORM_PAYMENT_1,
        widget=widgets.RadioSelect,
        blank=False
    )
    payment_phone_1 = models.StringField(
        label="11.2 Indique el número de teléfono asociado a al que se le girará la compensación.",
        blank=True
    )
    payment_platform_2 = models.StringField(
        label="11.3 Indique si el tercero tiene su número de celular asociado a  Nequi o Daviplata",
        choices=C.PLATFORM_PAYMENT_2,
        widget=widgets.RadioSelect,
        blank=True
    )
    payment_phone_2 = models.StringField(
        label="11.4. Indique el número de teléfono del tercero asociado a [Nequi/Daviplata] al que se le girará la compensación.",
        blank=True
    )
    payment_name = models.StringField(
        label="11.5 Nombre exacto de como se encuentra suscrito el Daviplata, Nequi de quién recibirá el giro.",
        blank=False
    )
    recall_name = models.StringField(
        label="11.6 Por favor, indique su nombre completo para el recontacto.",
        blank=False
    )
    recall_phone_bi = models.IntegerField(
        label="11.7 ¿El número de teléfono para el recontacto es el mismo que nos dio para el pago de la compensación?",
        choices=[
            (1, "Sí"),
            (0, "No")
        ],
        widget=widgets.RadioSelect,
        blank=False
    )
    recall_phone_2 = models.StringField(
        label="11.8 Por favor, proporcione un número telefónico de contacto.",
        blank=True
    )
    recall_email = models.StringField(
        label="11.9. Por favor, proporcione una dirección de correo electrónico válida.",
        blank=False
    )
    recall_address = models.StringField(
        label="11.10 Por favor, proporcione una dirección geográfica para el recontacto a la fase II",
        blank=False
    )
    contact_source = models.IntegerField(
        label="11.11 Solo para el encuestador: ¿Cómo se contactó a la persona encuestada?",
        choices=C.CONTACT_SOURCE,
        widget=widgets.RadioSelect,
        blank=False
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
    data_folder = Path("data_internal/payoffs")
    timestamp = datetime.now(C.TZ_COLOMBIA).strftime("%Y_%m_%d_%H:%M")
    csv_file_path = data_folder / "payoffs.csv"
    temp_file = csv_file_path.with_suffix('.tmp')

    if player.payment_platform_1 != "999":
        participant.payment_platform = player.payment_platform_1
        participant.payment_phone = player.payment_phone_1
        participant.payment_phone = clean_phone(participant.payment_phone)
    else:
        participant.payment_platform = player.payment_platform_2
        participant.payment_phone = player.payment_phone_2
        participant.payment_phone = clean_phone(participant.payment_phone)

    # Create directory if it doesn't exist
    data_folder.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'participant_label', 'date_interview', 'payment_name',
        'payment_platform', 'payment_number',
        'participation_fee', 'payoff_games', 'total_compensation'
    ]
    new_row = {
        'participant_label': participant.label,
        'date_interview': timestamp,
        'payment_name': player.payment_name,
        'payment_platform': participant.payment_platform,
        'payment_number': participant.payment_phone,
        'participation_fee': participant.participation_fee,
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

        player.payment_phone_1 = "Anonymous"
        player.payment_phone_2 = "Anonymous"
        player.payment_platform_1 = "Anonymous"
        player.payment_platform_2 = "Anonymous"
        player.payment_name = "Anonymous"

    except Exception as e:
        if temp_file.exists():
            os.remove(temp_file)
        print(f"Erreur dans export_payoffs_headenumerator: {e}")
        raise e

@simple_safe_operation
def export_recall(player):
    participant = player.participant
    data_folder = Path("data_internal/for_wave_2")
    csv_file_path = data_folder / "recall.csv"
    temp_file = csv_file_path.with_suffix('.tmp')
    # Create directory if it doesn't exist
    data_folder.mkdir(parents=True, exist_ok=True)

    if player.recall_phone_bi == 0:
        participant.recall_phone = player.recall_phone_2
        participant.recall_phone = clean_phone(participant.recall_phone)
    else:
        participant.recall_phone = participant.payment_phone
        participant.recall_phone = clean_phone(participant.recall_phone)

    try:
        new_data = {
            'participant_label': participant.label,
            'participant_name': player.recall_name,
            'participant_phone': participant.recall_phone,
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
        participant.recall_phone = "Anonymous"
        participant.payment_phone = "Anonymous"
        player.recall_name = "Anonymous"
        player.recall_email = "Anonymous"
        player.recall_address = "Anonymous"

    except Exception as e:
        # Nettoyer le fichier temp en cas d'erreur
        if temp_file.exists():
            os.remove(temp_file)
        print(f"Erreur dans export_recall: {e}")
        raise e

def export_interviews_per_group(player):
    participant = player.participant
    data_folder = Path("data_internal/tracking")
    csv_file_path = data_folder / "interviews_per_group.csv"
    temp_file = csv_file_path.with_suffix('.tmp')

    data_folder.mkdir(parents=True, exist_ok=True)

    group_label = f"grupo_{participant.sample}"
    enumerator_id = participant.enumerator
    supervisor_id = participant.supervisor

    fieldnames = ['supervisor_id','enumerator_id', 'group', 'nb_interviews']

    try:
        rows = []
        found = False

        if csv_file_path.exists():
            # Read all existing rows
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['supervisor_id'] == str(supervisor_id) and row['enumerator_id'] == str(enumerator_id) and row['group'] == group_label:
                        # Row exists: increment
                        row['nb_interviews'] = int(row['nb_interviews']) + 1
                        found = True
                    rows.append(row)

        if not found:
            # Row doesn't exist: add new one
            rows.append({
                'supervisor_id': supervisor_id,
                'enumerator_id': enumerator_id,
                'group': group_label,
                'nb_interviews': 1
            })

        # Write to temp file first
        with open(temp_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        # Atomically replace original with temp
        shutil.move(str(temp_file), str(csv_file_path))

    except Exception as e:
        if temp_file.exists():
            os.remove(temp_file)
        print(f"Error in export_interviews_per_group: {e}")
        raise e

def clean_phone(raw):
    """Strip spaces, dashes, dots and parentheses, plus an optional +57 / 57 prefix."""
    digits = re.sub(r'[\s\-\.\(\)]', '', raw or '')
    if digits.startswith('+57'):
        digits = digits[3:]
    elif digits.startswith('57') and len(digits) == 12:
        digits = digits[2:]
    return digits

def is_mobile_co(raw):
    return re.fullmatch(r'3\d{9}', clean_phone(raw)) is not None

def is_phone_co(raw):
    # mobile (3XXXXXXXXX) or landline (60XXXXXXXX)
    return re.fullmatch(r'(3\d{9}|60\d{8})', clean_phone(raw)) is not None

# PAGES
class Page1_1(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        participant = player.participant
        # Wave 1: all fields including recall
        if participant.dropout is False and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'payment_platform_1',
                'payment_phone_1',
                'payment_platform_2',
                'payment_phone_2',
                'payment_name',
                'recall_name',
                'recall_phone_bi',
                'recall_phone_2',
                'recall_email',
                'recall_address',
            ]
        # Wave 2: payment fields only
        elif participant.dropout is False and player.session.config['name'] == "session_C4P_SPANISH_w2":
            return [
                'payment_platform_1',
                'payment_phone_1',
                'payment_platform_2',
                'payment_phone_2',
                'payment_name',
            ]
    @staticmethod
    def vars_for_template(player):
        return dict(
            is_wave1=player.session.config['name'] == "session_C4P_SPANISH_w1"
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        export_payoffs_headenumerator(player)
        export_recall(player)
        export_interviews_per_group(player)
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return (not participant.dropout) and (
                player.session.config['name'] == "session_C4P_SPANISH_w1" or
                player.session.config['name'] == "session_C4P_SPANISH_w2"
        )
    @staticmethod
    def error_message(player, values):
        MSG_MOBILE = ('Por favor, indique un número de celular válido: '
                      '10 dígitos que empiezan por 3 (ej. 300 123 4567).')
        MSG_PHONE = ('Por favor, indique un número de teléfono válido: '
                     '10 dígitos (celular que empieza por 3, o fijo que empieza por 60).')

        p1 = values.get('payment_platform_1')
        if p1 and p1 != '999':
            if not (values.get('payment_phone_1') or '').strip():
                return 'Por favor, indique un número de teléfono.'
            if not is_mobile_co(values['payment_phone_1']):
                return MSG_MOBILE
        if p1 == '999':
            if not values.get('payment_platform_2'):
                return 'Por favor, elija una plataforma de pago.'
            if not (values.get('payment_phone_2') or '').strip():
                return 'Por favor, indique un número de teléfono.'
            if not is_mobile_co(values['payment_phone_2']):
                return MSG_MOBILE
        if values.get('recall_phone_bi') == 0:
            if not (values.get('recall_phone_2') or '').strip():
                return 'Por favor, indique un número de teléfono.'
            if not is_phone_co(values['recall_phone_2']):
                return MSG_PHONE


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
                (player.session.config['name'] == "session_C4P_SPANISH_w2" and participant.treatment_hope == 1)
        )

class Page3(Page):
    form_model = 'player'
    form_fields = ["contact_source"]

page_sequence = [
    Page1_1,
    Page1_2,
    Page2,
    Page3
]
