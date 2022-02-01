class CurrentCarbonBudget:
    """
    ...
    """

    def __init__(self, daily_carbon_budget):
        self.total_carbon_budget = daily_carbon_budget
        self.carbon_budget = daily_carbon_budget
        self.saved_carbon = 0

    def update(self, used_carbon):
        new_carbon_budget = self.carbon_budget - used_carbon
        if new_carbon_budget < 0:
            self.carbon_budget = 0
        else:
            self.carbon_budget = new_carbon_budget

    def reset(self):
        self.saved_carbon = self.carbon_budget
        self.carbon_budget = self.total_carbon_budget


class SavingBudget:
    """
    ...
    """

    def __init__(self):
        self.savings = 0
