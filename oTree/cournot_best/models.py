from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
)
import random
from otree import (session, settings)

doc = """
In Cournot competition, firms simultaneously decide the units of products to
manufacture. The unit selling price depends on the total units produced. In
this implementation, there are 2 firms competing for 1 period.
"""


class Constants(BaseConstants):
    name_in_url = 'cournot'
    players_per_group = 3
    num_rounds = 6
    print("execute constants class")
    instructions_template = 'cournot_best/instructions.html'  ###This must match the directory name within templates

    Results = models.StringField()


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_capacity = models.IntegerField()
    max_units_per = models.IntegerField()
    min_units_per = models.IntegerField()

    def market(self):
        # self.min_units_per = 3
        if self.session.config['market'] == 'm1':
            self.total_capacity = 100
            self.max_units_per = 25
            self.min_units_per = 0

        if self.session.config['market'] == 'm2':
            self.total_capacity = 500
            self.min_units_per = 40
            self.max_units_per = 125

    print("group class")
    prev_total_units = models.IntegerField()
    unit_price = models.CurrencyField()
    total_units = models.IntegerField(
        doc="""Total units produced by all players"""
    )

    prev_payoff = models.CurrencyField()
    prev_units = models.IntegerField()

    def set_payoffs(self):

        players = self.get_players()
        print("Defining Result Variables")
        # self.market()
        print(p.units for p in players)
        self.total_units = sum([p.units for p in players])

        ######################## INVERSE DEMAND FUNCTIONS #######################
        if self.session.config['market'] == 'm1':
            self.unit_price = 100 - self.total_units
            #       p=100-Q     #
        if self.session.config['market'] == 'm2':
            self.unit_price = 45 - (3 * self.total_units) ** (1 / 2)

        if self.round_number > 1:

            self.prev_total_units = self.in_round(self.round_number - 1).total_units
            print("total units in previous round = ", self.prev_total_units)

            for p in players:
                p.prev_payoff = p.in_round(self.round_number - 1).payoff

                p.prev_units = p.in_round(self.round_number - 1).units  # right side of the = says "player in previous round 'units'"
                print("individual previous round units", p.prev_units)

        ##############  PROFIT FUNCTIONS ######################
        for p in players:
            if self.session.config['market'] == 'm1':
                p.payoff = (self.unit_price - 1) * p.units
            if self.session.config['market'] == 'm2':
                p.payoff = self.unit_price * p.units - p.units ** (3 / 2)


class Player(BasePlayer):
    units = models.IntegerField()
    max_units_per = models.IntegerField()
    min_units_per = models.IntegerField()


    def market(self):
        if self.round_number > 1 and self.session.config['bandit']:
            # self.other_player()
            # self.my_player()
            self.units = self.prev_units

        if self.session.config['market'] == 'm1':
            self.max_units_per = 25
            self.min_units_per = 0

        if self.session.config['market'] == 'm2':
            self.max_units_per = 125
            self.min_units_per = 40

    # def units(self):
    #     if self.round_number > 1 and self.session.config['bandit']:
    #         return self.player.in_round(self.round_number-1).units

    def units_max(self):
        self.market()
        return self.max_units_per

    def units_min(self):
        self.market()
        return self.min_units_per



    ### DO NOT DELETE!!! The lines below are referenced as p.prev_unit and p.prev_payoff in Group
    prev_units = models.IntegerField()
    prev_payoff = models.CurrencyField()
    bandit_pr = models.IntegerField()

    def my_player(self):
        if self.round_number > 1:
            # self.bandit_pr = (random.randint(1, 3) == 2)
            self.prev_units = self.in_round(self.round_number - 1).units

    def other_player(self):
        if self.round_number > 1:
            self.prev_units = self.in_round(self.round_number - 1).units
            self.prev_units = self.in_round(self.round_number - 1).payoff
        return self.get_others_in_group()[0]

