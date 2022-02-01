class Calculator:
    """
    ...
    """

    def __init__(self, traffic_amount, carbon_per_traffic, angle_per_carbon):
        self.traffic_amount = traffic_amount * 0.000000001
        self.carbon_per_traffic = carbon_per_traffic
        self.angle_per_carbon = angle_per_carbon
        self.used_carbon = self.traffic_data_to_carbon()
        self.degrees_to_turn = self.carbon_to_angle()

    def traffic_data_to_carbon(self):
        return self.traffic_amount*self.carbon_per_traffic

    def carbon_to_angle(self):
        return self.angle_per_carbon * self.used_carbon
