from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import (Constants,)


class Introduction(Page):
    pass

class Decide_shell(Page):
    form_model = 'player'
    form_fields = ['units']

    def vars_for_template(self):
        self.group.market()

        if (self.session.config['bandit']) and (self.round_number > 1):
            return {
                'decision': 'cournot_best/Decide_bandit.html',
                # 'min_units': self.group.min_units_per,
                # 'max_units': self.group.max_units_per,
                'prev_units': self.player.in_round(self.round_number-1).units
            }

        elif (self.session.config['bandit'] == False) or (self.round_number == 1):
            return {
                'decision': 'cournot_best/Decide.html',
                'min_units': self.group.min_units_per,
                'max_units': self.group.max_units_per
            }

class Decide_bandit(Page):
    def vars_for_template(self):
        self.group.market()

        if (self.session.config['bandit']) and (self.round_number > 1) and (self.player.bandit_pr == True):
            return {
                # 'decision': 'cournot_best/Decide_bandit.html',
                # 'min_units': self.group.min_units_per,
                # 'max_units': self.group.max_units_per,
                'prev_units': self.player.in_round(self.round_number-1).units
            }


class Decide(Page):
    form_model = 'player'
    form_fields = ['units']

    def vars_for_template(self):

        self.group.market()
        return {
            'min_units': self.group.min_units_per,
            'max_units': self.group.max_units_per
        }


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant to decide."

    def after_all_players_arrive(self):
        self.group.set_payoffs()




class Results(Page):

    def vars_for_template(self):

        return {
        'other_player_units': self.player.other_player().units
        }


class Results_shell(Page):

    def vars_for_template(self):

        if self.session.config['treatment'] == 'test':
            return {
                'Treatment': 'cournot_best/Results.html'
            }
        if self.session.config['treatment'] == 'Q':
            return {
                'Treatment': 'cournot_best/Results_Q.html'
            }
        if self.session.config['treatment'] == 'Qq':
            return {
                'Treatment': 'cournot_best/Results_Qq.html'
            }
        if self.session.config['treatment'] == 'Qqpi':
            return {
                'Treatment': 'cournot_best/Results_Qqpi.html'
            }


    # the only thing this page does is {% include Treatment %}
    # Treatment represents an html page that varies based on treatment
    pass



page_sequence = [
  #  Introduction,
    Decide_shell,
    ResultsWaitPage,
    Results_shell
]
