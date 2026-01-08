from CommunicationsProtocol import ProtocolLayer


class DataLinkLayer(ProtocolLayer.ProtocolLayer):
    def __init__(self, DLL_rx,DLL_tx, SDR_rx, SDR_tx):
        super().__init__(DLL_rx,DLL_tx, SDR_rx, SDR_tx)
        self.name = "Data Link Layer"


class GroundStationDataLinkLayer(DataLinkLayer):
    def __init__(self, DLL_rx,DLL_tx, SDR_rx, SDR_tx):
        super().__init__(DLL_rx,DLL_tx, SDR_rx, SDR_tx)


class AudimusDataLinkLayer(DataLinkLayer):
    def __init__(self, DLL_rx,DLL_tx, SDR_rx, SDR_tx):
        super().__init__(DLL_rx,DLL_tx, SDR_rx, SDR_tx)



