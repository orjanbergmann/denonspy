import os
from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass

import asyncio
import denonavr

from rpi_lcd import LCD


@dataclass
class Screen:
    line1: str = ''
    line2: str = ''
    line3: str = ''
    line4: str = ''


DENON_IP = os.getenv('DENON_IP')
lcd = LCD()

def send_to_lcd(screen):
    lcd.text(screen.line1, 1)
    lcd.text(screen.line2, 2)
    lcd.text(screen.line3, 3)
    lcd.text(screen.line4, 4)

def send_to_screen(screen):
    print('-'*20)
    print(screen.line1)
    print(screen.line2)
    print(screen.line3)
    print(screen.line4)
    print('-'*20)

def do_screen_volume(volume):
    chars = int(volume / 5)
    screen = Screen(
        line1=f'    Volume: {volume}',
        line2=f'',
        line3=f"{'#'*chars}",
        line4=f"{'#'*chars}"
    )
    send_to_screen(screen)
    send_to_lcd(screen)

def do_volume_change(value):
    volume = float(value) / (10.0 if len(value) == 3 else 1.0)
    do_screen_volume(volume)

async def update_callback(zone, event, parameter):
    match event:
        case 'MV':
            do_volume_change(parameter)
        case _:
            print("Zone: " + zone + " Event: " + event + " Parameter: " + parameter)

async def main():
    greeting = Screen(line2=f' Denon:  {DENON_IP}')
    send_to_lcd(greeting)
    send_to_screen(greeting)
    
    d = denonavr.DenonAVR(DENON_IP)
    await d.async_setup()
    await d.async_telnet_connect()
    await d.async_update()
    d.register_callback("ALL", update_callback)

if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        bye = Screen(line2=f' Shutdown, bye!')
        send_to_lcd(bye)
        send_to_screen(bye)
    finally:
        print('Abort!')
        lcd.clear()

