from pywizlight import wizlight, PilotBuilder, discovery
import asyncio

async def main():
    print("adjusting light")
    light = wizlight("192.168.50.40")
    timeout = 10 
    await light.turn_on(PilotBuilder(rgb = (255, 0, 0)))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())