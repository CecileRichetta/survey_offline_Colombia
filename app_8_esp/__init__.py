from otree.api import *


doc = """
Questions about trust.
"""


class C(BaseConstants):
    NAME_IN_URL = 'app_8_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    WVS_SCALE = [
        (0, "Hay que ser muy cauteloso al tratar con la mayoria de las personas"), # You have to be very cautious
        (1, "La mayoria de las personas son confiables"), # Most people can be trusted
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]
    WALLET_SCALE = [
        (0, "Nada probable"), # Not at all likely
        (1, "Poco probable"), # Not very likely
        (2, "Ni probable ni improbable "), # Neither likely nor unlikely
        (3, "Probable"), # Quite likely
        (4, "Muy probable"), # Very likely
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
        ]
    TRUST_SCALE = [
        (0, "Nada"), # Not at all
        (1, "Un poco"), # A little
        (2, "Algo"), # Somewhat
        (3, "Mucho"), # A lot
        (4, 'Completamente '), # Completely
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]
    IG_OG_TRUST_SCALE = [
        (0, "Completamente en desacuerdo"), # Completely disagree
        (1, "En desacuerdo"), # Disagree
        (2, "Ni de acuerdo ni en desacuerdo"), # Neither disagree nor agree
        (3, "De acuerdo"), # Agree
        (4, "Completamente de acuerdo"), # Completely agree
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Social trust
    social_trust_wvs = models.IntegerField(
        label="8.1. En términos generales, ¿diría que la mayoría de las personas son confiables o que es necesario "
              "ser muy cauteloso al tratar con la mayoría de las personas?",
        # Generally speaking, would you say that most people can be trusted or would you say it’s necessary to be "
        #               "very cautious when dealing with most people?
        choices=C.WVS_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    social_trust_wallet = models.IntegerField(
        label="8.2. Suponga que pierde su cartera/billetera con sus datos de dirección y alguien que vive en su barrio la encuentra en la calle. ¿Qué tan probable es que se la devuelvan sin que falte nada?",
        #               "someone living in the neighborhood you last lived in, in your home country. How likely is it that it would "
        #               "be returned to you with nothing missing?
        choices= C.WALLET_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    social_trust_2 = models.IntegerField(
        label="8.3. Por favor dígame, ¿qué tanto confía en: Su familia?",
        # Please tell me how much you trust: Your family.
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    social_trust_3 = models.IntegerField(
        label="8.4. Por favor dígame, ¿qué tanto confía en:  sus vecinos?",
        # Please tell me how much you trust: Your neighbors.
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    # Intergroup trust
    intergroup_trust_3 = models.IntegerField(
        # dynamic label on webpage
        choices=C.IG_OG_TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    intergroup_trust_4 = models.IntegerField(
        # dynamic label on webpage
        choices=C.IG_OG_TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    intergroup_trust_7 = models.IntegerField(
        # dynamic label on webpage
        choices=C.IG_OG_TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    # Outgroup trust
    outgroup_trust_3 = models.IntegerField(
        # dynamic label on webpage
        choices=C.IG_OG_TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    outgroup_trust_4 = models.IntegerField(
        # dynamic label on webpage
        choices=C.IG_OG_TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    outgroup_trust_7 = models.IntegerField(
        # dynamic label on webpage
        choices=C.IG_OG_TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    # institutional trust
    institutional_trust_1 = models.IntegerField(
        label="8.11. Por favor, dìgame cuánto confía en la siguiente institución: Presidente",
        # The president
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    institutional_trust_2 = models.IntegerField(
        label="8.12. Por favor, dìgame cuánto confía en la siguiente institución: la administración local"
              " o Alcaldía local",
        # The parliament
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    institutional_trust_7 = models.IntegerField(
        label="8.13. Por favor, dìgame cuánto confía en la siguiente institución: La policía.",
        # The Police
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    institutional_trust_8 = models.IntegerField(
        label="8.14. Por favor, dìgame cuánto confía en el Ejército Colombiano en su papel de proporcionar seguridad y apoyar los esfuerzos de paz.",
        # The army
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    institutional_trust_9 = models.IntegerField(
        label="8.15. Por favor, dígame cuánto confía en que el sistema judicial colombiano, incluidos los tribunales, administran justicia de forma justa.",
        # The courts of law
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    institutional_trust_10 = models.IntegerField(
        label="8.16. Por favor, dígame cuánto confía en los líderes religiosos en Colombia para actuar en el mejor interés de sus comunidades.",
        # The traditional leaders
        choices=C.TRUST_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )



# PAGES

class Page1(Page):
    form_model = 'player'
    form_fields = [
        'social_trust_wvs',
        'social_trust_wallet',
        'social_trust_2',
        'social_trust_3',
    ]


class Page2(Page):
    form_model = 'player'
    form_fields = [
        'intergroup_trust_3',
        'intergroup_trust_4',
        'intergroup_trust_7'
    ]


class Page3(Page):
    form_model = 'player'
    form_fields = [
        'outgroup_trust_3',
        'outgroup_trust_4',
        'outgroup_trust_7'
    ]


class Page4(Page):
    form_model = 'player'
    form_fields = [
        'institutional_trust_1',
        'institutional_trust_2',
        'institutional_trust_7',
        'institutional_trust_8',
        'institutional_trust_9',
        'institutional_trust_10'
    ]

page_sequence = [
    Page1, # social trust
    Page2, # ingroup trust
    Page3, # outgroup trust
    Page4 # institutional trust
]
