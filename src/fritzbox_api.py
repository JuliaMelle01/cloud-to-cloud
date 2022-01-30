class TrafficCapture:

    def __init__(self):
        self.data = 0

    def update_data(self, json_packet):
        bytes_sent = json_packet["layers"]["ip"]["ip_ip_len"]
        self.data += int(bytes_sent)
