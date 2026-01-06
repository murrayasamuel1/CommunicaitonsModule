import ProtocolLayer

class SessionLayer(ProtocolLayer.ProtocolLayer):
    def __init__(self, SL_rx,SL_tx, DLL_rx, DLL_tx):
        super().__init__(SL_rx,SL_tx, DLL_rx, DLL_tx)
        self.name = "Session Layer"

class GroundStationSessionLayer(SessionLayer):
    def __init__(self, SL_rx,SL_tx, DLL_rx, DLL_tx):
        super().__init__(SL_rx,SL_tx, DLL_rx, DLL_tx)


class AudimusSessionLayer(SessionLayer):
    def __init__(self, SL_rx,SL_tx, DLL_rx, DLL_tx):
        super().__init__(SL_rx,SL_tx, DLL_rx, DLL_tx)


