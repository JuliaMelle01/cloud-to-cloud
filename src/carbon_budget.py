class CurrentCarbonBudget:
    """
    A class monitoring the daily and current carbon budget.
    """

    def __init__(self, daily_carbon_budget):
        #: Set daily carbon budget
        self.total_carbon_budget = daily_carbon_budget
        #: Current left carbon budget
        self.carbon_budget = daily_carbon_budget
        #: Saved carbon per day
        self.saved_carbon = 0

    def update(self, used_carbon):
        """
        Updates the current carbon budget according the captured
        data traffic.

        :param used_carbon: A float indicating how much carbon was
        used
        """
        new_carbon_budget = self.carbon_budget - used_carbon
        if new_carbon_budget < 0:
            self.carbon_budget = 0
        else:
            self.carbon_budget = new_carbon_budget

    def reset(self):
        """
        Resets the carbon budget and updates the daily savings made.
        :return:
        """
        self.saved_carbon = self.carbon_budget
        self.carbon_budget = self.total_carbon_budget


class SavingBudget:
    """
    An adapter class where the total long term savings could
    be managed.
    """

    def __init__(self):
        #: Long term carbon savings
        self.savings = 0
