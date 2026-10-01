from otree.api import *


doc = """
Treatment hope
"""


class C(BaseConstants):
    NAME_IN_URL = 'app_4_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # CONSTANTS
    BINARY_ANSWER = [
        (1, 'Sí'),  # Yes
        (0, 'No'), # No
        (998, "No sabe (no leer)"),  # Don't know
        (999, 'No responde (no leer)') # Prefer not to say
    ]
    HOPE_READ = [
        (1, "Sí"), # I read it out loud
        (0, 'No') # The person read it
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    text_check = models.IntegerField(
        label="4.1. ¿Han llegado ya los investigadores a una conclusión sobre las probabilidades de éxito de la reconciliación en Colombia?",
        # For the enumerator: did you the person read the text autonomously?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelect,
        blank=False
    )
    hope_recall = models.IntegerField(
        label="4.2. ¿Alguna vez ha sentido esperanza de que el proceso de paz en Colombia tenga éxito? Por favor, tome un momento para reflexionar sobre esto.",
        # Have you ever felt hopeful that the social reconciliation between former fighters and local communities, in the context of the peace process in the North, will be successful? Please take a moment to reflect on this.
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelect,
        blank=False
    )
    hope_reason = models.LongStringField(
        label="4.3. Si alguna vez ha tenido esa sensación, por favor cuéntenos en 1 o 2 frases.",
        # If you have ever had such a feeling, please tell us about it in 1-2 sentences.
        blank=True
    )


# PAGES
class Page1_1(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant #
        if participant.treatment_hope == 1 and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'text_check',
                'hope_recall',
                'hope_reason'
            ]
        else:
            return []
    def is_displayed(player):
        participant = player.participant
        return participant.treatment_hope == 1 and player.session.config['name'] == "session_C4P_SPANISH_w1"


class Page1_2(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant #
        if participant.treatment_hope == 0 and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'text_check'
            ]
        else:
            return []
    def is_displayed(player):
        participant = player.participant
        return participant.treatment_hope == 0 and player.session.config['name'] == "session_C4P_SPANISH_w1"


page_sequence = [
    Page1_1,
    Page1_2
]
