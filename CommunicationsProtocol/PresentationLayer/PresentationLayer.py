from CommunicationsProtocol import ProtocolLayer
import Audimus_pb2

class PresentationLayer(ProtocolLayer.ProtocolLayer):
    def __init__(self, PL_rx,PL_tx, SL_rx, SL_tx, data_file):
        super().__init__(PL_rx,PL_tx, SL_rx, SL_tx)
        self.name = "Presentation Layer"
        self.key_epoch = 0
        self.data_file = data_file
        self.session_number = self.read_session_number()


    def process_rx(self, msg):
        message = self.decode(msg)
        if message.session_number > self.session_number:
            self.update_session_number(message.session_number)
        return message.application_data

    def process_tx(self, application_data):
        msg = self.encode(application_data)
        return msg

    def encode(self, message):
        msg = Audimus_pb2.Presentation_Data()
        msg.key_epoch = self.key_epoch
        msg.session_number = self.session_number
        msg.application_data = message
        return msg.SerializeToString()

    def decode(self, msg):
        message = Audimus_pb2.Presentation_Data()
        message.ParseFromString(msg)
        return message

    def encrypt(self):
        pass

    def authenticate(self):
        pass

    def read_session_number(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                session_number = file.read()
                return (int(session_number) + 1)

        except FileNotFoundError:
            print(
                f"Error: The file '{self.data_file}' was not found, could not retrieve session number")
        except Exception as e:
            print(f"An error occurred: {e}")


    def update_session_number(self, new_session_number):
        self.session_number = new_session_number
        with open(self.data_file, "w", encoding="utf-8") as f: f.write(str(new_session_number))





class GroundStationPresentationLayer(PresentationLayer):
    def __init__(self, PL_rx,PL_tx, SL_rx, SL_tx):
        super().__init__(PL_rx, PL_tx, SL_rx, SL_tx, "CommunicationsProtocol/GroundStationPresentationLayerData")



class AudimusPresentationLayer(PresentationLayer):
    def __init__(self, PL_rx,PL_tx, SL_rx, SL_tx):
        super().__init__(PL_rx, PL_tx, SL_rx, SL_tx, "CommunicationsProtocol/AudimusPresentationLayerData")





