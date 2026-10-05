from otree.api import *
import csv
import random


doc = """
Ultimatum Game Experiment App.
"""


class C(BaseConstants):
    NAME_IN_URL = 'app_5_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # GAME ELEMENTS
    TOKEN_VALUE = 2000
    TOKEN_ENDOWMENT = 4
    CHOICES_UG_PROPOSER = [
        (0, "No quiero darle fichas a mi pareja, quiero quedarme con 4 para mí."),
        (1, 'Quiero darle 1 ficha a mi compañero y quedarme con 3 para mí.'),
        (2, 'Quiero darle 2 fichas a mi compañero y quedarme con 2 para mí.'),
        (3, "Quiero darle 3 fichas a mi compañero y quedarme 1 para mí."),
        (4, "Quiero darle 4 fichas a mi compañero y no quedarme con ninguna para mí.")
    ]
    CHOICES_UG_RECEIVER = [
        (0, "Acepto que no recibo nada, y la otra persona se queda con las 4 fichas."),
        (1, 'Acepto la oferta si la otra persona me envía 1 ficha y se quedan con 3 fichas.'),
        (2, 'Acepto la oferta si la otra persona me envía 2 fichas y se quedn con 2 fichas.'),
        (3, "Acepto la oferta si la otra persona me envía 3 fichas y se queda con 1 ficha."),
        (4, "Acepto la oferta si la otra persona me envía 4 fichas y no se queda nada.")
    ]
    # INSTRUCTIONS TEMPLATES
    TEMPLATE_INSTRUCTIONS_ULTIMATUM_PROPOSER = '_static/texts_SPANISH/instr_ultimatum_proposer.html'
    TEMPLATE_INSTRUCTIONS_ULTIMATUM_RECEIVER = '_static/texts_SPANISH/instr_ultimatum_receiver.html'
    TEMPLATE_INSTRUCTIONS_PG = '_static/texts_SPANISH/instr_pg.html'
    # IMAGES TEMPLATES
    IMAGE_UG_INSTR = 'imgs/diagram_UG.png'
    IMAGE_UG_EXAMPLE1 = 'imgs/diagram_UG_example1.png'
    IMAGE_UG_EXAMPLE2 = 'imgs/diagram_UG_example2.png'




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # COMPREHENSION CHECKS SUM
    ultimatum_correct_answers = models.IntegerField()
    ultimatum_redo_questions = models.BooleanField(
        label="Algunas de sus respuestas en las preguntas anteriores no fueron correctas. Queremos darle la oportunidad de "
              "escuchar nuevamente las instrucciones completas y responder las preguntas. ¿Desea escuchar las instrucciones y responder las preguntas otra vez?",        #  Some of your answers in the previous questions were not correct. I want to give you the opportunity to listen
        #  once more to the full instructions, and answer the questions. Do you want to listen the instructions and answer once again the questions?
        choices=[
            (True, "Sí"),
            (False, "No")
        ],
        widget=widgets.RadioSelectHorizontal,
        blank=False)
    # PROPOSER comprehension checks
    ug_proposer_cc1 = models.IntegerField(
        label="5.1.1. No me queda más remedio que dar fichas al receptor.",
        #  I have no choice but to give tokens to the receiver.
        choices=[
            (0, 'Verdadera'), # True
            (1, 'Falsa') # False
        ],
        blank=False,
        widget=widgets.RadioSelectHorizontal
    )
    ug_proposer_cc2 = models.IntegerField(
        label="5.1.2. El receptor puede rechazar mi oferta.",
        # The receiver can refuse my offer.
        choices=[
            (1, 'Verdadera'), # True
            (0, 'Falsa') # False
        ],
        blank=False,
        widget=widgets.RadioSelectHorizontal
    )
    ug_proposer_cc3 = models.IntegerField(
        label="5.1.3. El receptor es ficticio.",
        # The receiver is fake.
        choices=[
            (0, 'Verdadera'), # True
            (1, 'Falsa') # False
        ],
        blank=False,
        widget=widgets.RadioSelectHorizontal
    )
    # RESPONDER COMPREHENSION CHECKS
    ug_receiver_cc1 = models.IntegerField(
        label="5.2.1. El proponente no tiene más remedio que enviarme fichas.",
        # The proposer has no choice but to send me tokens.
        choices=[
            (0, 'Verdadera'), # True
            (1, 'Falsa') # False
        ],
        blank=False,
        widget=widgets.RadioSelectHorizontal
    )
    ug_receiver_cc2 = models.IntegerField(
        label="5.2.2. Si el mínimo de fichas que quiero es menor que lo que ofrece el proponente, obtengo las fichas.",
        # If the minimum of tokens that I want is smaller than what the proposer offers, I get the tokens.
        choices=[
            (1, 'Verdadera'), # True
            (0, 'Falsa') # False
        ],
        blank=False,
        widget=widgets.RadioSelectHorizontal
    )
    ug_receiver_cc3 = models.IntegerField(
        label="5.2.3. El proponente es ficticio",
        # The proposer is fake.
        choices=[
            (0, 'Verdadera'), # True
            (1, 'Falsa') # False
        ],
        blank=False,
        widget=widgets.RadioSelectHorizontal
    )
    # CHOICES IN UG
    decision_proposer = models.IntegerField(
        label="",
        # How much do you offer to the other person and how much do you keep?
        choices=C.CHOICES_UG_PROPOSER,
        blank=False,
        widget=widgets.RadioSelect
    )
    decision_receiver = models.IntegerField(
        label="",
        # How much do you offer to the other person and how much do you keep?
        choices=C.CHOICES_UG_RECEIVER,
        blank=False,
        widget=widgets.RadioSelect
    )

# FUNCTIONS
def extract_games_and_payoffs(p):
    # Read CSV manually
    if p.session.config['name'] == "session_C4P_SPANISH_w1":
        with open("data_internal/payoffs/games_pilot.csv", newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    else:
        with open("data_internal/payoffs/games_wave_1.csv", newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    # Convert numeric fields
    for row in rows:
        row['group'] = int(row['group'])
        row['etv'] = int(row['etv'])
        row['side_ultimatum'] = int(row['side_ultimatum'])
        row['decision_UG'] = float(row['decision_UG'])
        row['decision_PG'] = float(row['decision_PG'])

    participant = p.participant

    # Pre-filter based on treatment_other
    def filter_df(rows, treatment):
        if treatment == 0:
            return rows
        elif treatment == 1:
            return [r for r in rows if r['group'] == 0]
        elif treatment == 2:
            return [r for r in rows if r['group'] == 1]
        elif treatment == 3:
            return [r for r in rows if r['group'] == 0 and r['etv'] == 1]
        elif treatment == 4:
            return [r for r in rows if r['group'] == 1 and r['etv'] == 1]
        return rows

    source = filter_df(rows, participant.treatment_other)

    # Define candidates based on side_ultimatum
    if participant.side_ultimatum == 0:
        ug_candidates = [r for r in source if r['side_ultimatum'] == 1]
        pg_candidates = source
    else:
        ug_candidates = [r for r in source if r['side_ultimatum'] == 0]
        pg_candidates = source

    # Helper to safely sample
    def safe_sample(candidates, column):
        if len(candidates) > 1:
            return random.choice(candidates)[column]
        elif len(candidates) == 1:
            return candidates[0][column]
        else:
            return None

    participant.other_UG_decision = safe_sample(ug_candidates, 'decision_UG')
    participant.other_PG_decision = safe_sample(pg_candidates, 'decision_PG')


def correct_answers_ultimatum(player):
    participant = player.participant
    if participant.side_ultimatum == 0:
        cc1 = player.field_maybe_none('ug_proposer_cc1')
        cc2 = player.field_maybe_none('ug_proposer_cc2')
        cc3 = player.field_maybe_none('ug_proposer_cc3')
        if None in (cc1, cc2, cc3):
            player.ultimatum_correct_answers = 0
        else:
            player.ultimatum_correct_answers = cc1 + cc2 + cc3
    else:
        cc1 = player.field_maybe_none('ug_receiver_cc1')
        cc2 = player.field_maybe_none('ug_receiver_cc2')
        cc3 = player.field_maybe_none('ug_receiver_cc3')
        if None in (cc1, cc2, cc3):
            player.ultimatum_correct_answers = 0
        else:
            player.ultimatum_correct_answers = cc1 + cc2 + cc3


def payoff_UG(participant):
    if participant.side_ultimatum == 0:
        if participant.decision_UG >= participant.other_UG_decision:
            participant.payoff_UG = C.TOKEN_ENDOWMENT - participant.decision_UG
        else:
            participant.payoff_UG = 0
    else:
        if participant.decision_UG <= participant.other_UG_decision:
            participant.payoff_UG = participant.other_UG_decision
        else:
            participant.payoff_UG = 0


# PAGES
class Page1(Page):
    pass
    @staticmethod
    def before_next_page(player, timeout_happened):
        extract_games_and_payoffs(player)
        participant = player.participant
        print(participant.other_UG_decision)
        print(participant.other_PG_decision)


class Page2(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.side_ultimatum == 0:
            return [
                'ug_proposer_cc1',
                'ug_proposer_cc2',
                'ug_proposer_cc3'
            ]
        elif participant.side_ultimatum == 1:
            return [
                'ug_receiver_cc1',
                'ug_receiver_cc2',
                'ug_receiver_cc3'
            ]
        else:
            return []
    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_answers_ultimatum(player)


class Page3(Page):
    form_model = 'player'
    form_fields = ['ultimatum_redo_questions']

    @staticmethod
    def is_displayed(player):
        return player.field_maybe_none('ultimatum_correct_answers') < 3

class Page4(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.side_ultimatum == 0:
            return [
                'ug_proposer_cc1',
                'ug_proposer_cc2',
                'ug_proposer_cc3'
            ]
        elif participant.side_ultimatum == 1:
            return [
                'ug_receiver_cc1',
                'ug_receiver_cc2',
                'ug_receiver_cc3'
            ]
        else:
            return []
    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_answers_ultimatum(player)
    @staticmethod
    def is_displayed(player):
        return player.ultimatum_correct_answers < 3 and player.ultimatum_redo_questions


class Page5_1(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.side_ultimatum==0:
            return [
                'decision_proposer'
            ]
        else:
            pass
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.side_ultimatum==0
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.decision_UG = player.decision_proposer
        payoff_UG(participant)


class Page5_2(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.side_ultimatum==1:
            return [
                'decision_receiver'
            ]
        else:
            pass
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.side_ultimatum==1
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.decision_UG = player.decision_receiver
        payoff_UG(participant)

page_sequence = [
    Page1, # Introduction games
    Page2, # Instructions + questions
    Page3, # Ask to re-do
    Page4, # Re-do instructions + questions
    Page5_1, # Decision proposer
    Page5_2 # Decision receiver
]
