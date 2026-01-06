import ProtocolLayer
import Audimus_pb2

class PresentationLayer(ProtocolLayer.ProtocolLayer):
    def __init__(self, PL_rx,PL_tx, SL_rx, SL_tx):
        super().__init__(PL_rx,PL_tx, SL_rx, SL_tx)
        self.name = "Presentation Layer"

    def encode(self, message):
        msg = Audimus_pb2.Test()
        msg.command = message
        return msg.SerializeToString()

    def decode(self, message):
        msg = Audimus_pb2.Test()
        msg.ParseFromString(message)
        return msg

    def encrypt(self):
        pass

    def authenticate(self):
        pass

    def process_rx(self, message):
        message = self.decode(message)
        print("PL received: ", message)

        return message

    def process_tx(self, message):
        print("PL sent: ", message)
        message = self.encode(message)
        return message

class GroundStationPresentationLayer(PresentationLayer):
    def __init__(self, PL_rx,PL_tx, SL_rx, SL_tx):
        super().__init__(PL_rx,PL_tx, SL_rx, SL_tx)


class AudimusPresentationLayer(PresentationLayer):
    def __init__(self, PL_rx,PL_tx, SL_rx, SL_tx):
        super().__init__(PL_rx,PL_tx, SL_rx, SL_tx)


