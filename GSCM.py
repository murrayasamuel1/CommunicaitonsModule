import asyncio

import DataLinkLayer
import PresentationLayer
import SessionLayer


async def satellite_tx(writer, SDR_tx):
    while True:

        msg = (await SDR_tx.get())
        writer.write(msg)          # msg must be bytes
        await writer.drain()


async def satellite_rx(reader, SDR_rx):
    while True:
        msg = await reader.read(1024)

        await SDR_rx.put(msg)

async def handle_client(reader, writer):

    #initiate queues

    #presentation layer queues
    PL_rx = asyncio.Queue()
    PL_tx = asyncio.Queue()

    #session layer queues
    SL_rx = asyncio.Queue()
    SL_tx = asyncio.Queue()

    #data link layer queues
    DLL_rx = asyncio.Queue()
    DLL_tx = asyncio.Queue()

    #SDR_queue
    SDR_rx = asyncio.Queue()
    SDR_tx = asyncio.Queue()



    #create instances of each layer
    pl = PresentationLayer.GroundStationPresentationLayer(PL_rx, PL_tx, SL_rx, SL_tx)
    sl = SessionLayer.GroundStationSessionLayer(SL_rx, SL_tx, DLL_rx, DLL_tx)
    dll = DataLinkLayer.GroundStationDataLinkLayer(DLL_rx, DLL_tx, SDR_rx, SDR_tx)

    #run satellite rx and tx coroutines
    rx = asyncio.create_task(satellite_rx(reader, SDR_rx))
    tx = asyncio.create_task(satellite_tx(writer, SDR_tx))

    #run presentation layer coroutines
    pl_tx_handler = asyncio.create_task(pl.tx())
    pl_rx_handler = asyncio.create_task(pl.rx())

    # run session layer coroutines
    sl_tx_handler = asyncio.create_task(sl.tx())
    sl_rx_handler = asyncio.create_task(sl.rx())

    #run data link layer coroutines
    dll_tx_handler = asyncio.create_task(dll.tx())
    dll_rx_handler = asyncio.create_task(dll.rx())


    #run session layer coroutines
    # send bytes, not strings
    await PL_tx.put("hi")
    await asyncio.sleep(1)
    await PL_tx.put("my")
    await asyncio.sleep(1)
    await PL_tx.put("name")
    await asyncio.sleep(1)
    await PL_tx.put("is")
    await asyncio.sleep(1)
    await PL_tx.put("sam")

    # wait for responses




async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
