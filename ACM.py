import asyncio

import DataLinkLayer
import PresentationLayer
import SessionLayer


async def client_tx(writer, SDR_tx):
    print("client sender started")
    while True:
        msg = await SDR_tx.get()      # wait for outgoing message
        writer.write(msg)               # send it
        await writer.drain()            # flush


async def client_rx(reader, SDR_rx):
    print("client receiver started")
    while True:
        msg = await reader.read(1024)   # wait for incoming data
        if not msg:
            break                       # server closed connection
        await SDR_rx.put(msg)         # push into RX queue


async def run_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    # presentation layer queues
    PL_rx = asyncio.Queue()
    PL_tx = asyncio.Queue()

    # session layer queues
    SL_rx = asyncio.Queue()
    SL_tx = asyncio.Queue()

    # data link layer queues
    DLL_rx = asyncio.Queue()
    DLL_tx = asyncio.Queue()

    # SDR_queue
    SDR_rx = asyncio.Queue()
    SDR_tx = asyncio.Queue()

    # create instances of each layer
    pl = PresentationLayer.AudimusPresentationLayer(PL_rx, PL_tx, SL_rx, SL_tx)
    sl = SessionLayer.AudimusSessionLayer(SL_rx, SL_tx, DLL_rx, DLL_tx)
    dll = DataLinkLayer.AudimusDataLinkLayer(DLL_rx, DLL_tx, SDR_rx, SDR_tx)

    #run satellite rx and tx coroutines
    rx = asyncio.create_task(client_rx(reader, SDR_rx))
    tx = asyncio.create_task(client_tx(writer, SDR_tx))

    # run presentation layer coroutines
    pl_tx_handler = asyncio.create_task(pl.tx())
    pl_rx_handler = asyncio.create_task(pl.rx())

    # run session layer coroutines
    sl_tx_handler = asyncio.create_task(sl.tx())
    sl_rx_handler = asyncio.create_task(sl.rx())

    # run data link layer coroutines
    dll_tx_handler = asyncio.create_task(dll.tx())
    dll_rx_handler = asyncio.create_task(dll.rx())

    # send bytes, not strings
    await PL_tx.put("hi")
    await asyncio.sleep(1)
    await PL_tx.put("my")
    await asyncio.sleep(1)
    await PL_tx.put("name")
    await asyncio.sleep(1)
    await PL_tx.put("is")
    await asyncio.sleep(1)
    await PL_tx.put("ben")



    await asyncio.gather(tx, rx)


async def main():
    await run_client("127.0.0.1", 8888)


if __name__ == "__main__":
    asyncio.run(main())
