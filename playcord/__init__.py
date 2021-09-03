import sys
from rich.console import Console
from playcord.utils import get_login_url
from playcord.account import Account
from urllib.parse import urlparse, parse_qs
from pypresence import Presence
import webbrowser
import time
from readsettings import ReadSettings
from pathlib import Path

def main(config : ReadSettings):
    console = Console()
    # If no arguments has provided open auth URL and exit.
    if len(sys.argv) != 2:
        webbrowser.open(get_login_url())
        sys.exit(0)
    # Otheriwse, get auth code.
    else:
        console.print("Playcord", style = "bright_white")
        console.print("https://github.com/ysfchn/Playcord", style = "bright_white")
        console.print("Show your PlayStation presence as Discord Rich Presence!\n", style = "bright_white")
        # Create a blank account object.
        account = None
        # Get auth code from query string.
        code = parse_qs(urlparse(sys.argv[1]).query).get("code", [None])[0]
        # If code is None, check for config for existing sessions.
        if (not code) and ("refresh_token" in config.data):
            console.print("An active session has found...", style = "grey78")
            account = Account.login_refresh(config["refresh_token"])
        # If code is not blank, login.
        elif code:
            console.print("Signing in...", style = "bright_yellow")
            account = Account.login(code)
        # If code is blank, open login browser and exit.
        else:
            webbrowser.open(get_login_url())
            sys.exit(0)
        # Save refresh token.
        config["refresh_token"] = account.session.refresh_token
        profile = account.profile()
        console.print(f"[green4]Signed in as [green3]{profile.id}[/green3]. [/green4]")
        console.print("To exit, close the window or press Ctrl + C.\n", style = "white")
        # Connect to Discord
        console.print("Connecting to Discord...", style = "bright_yellow")
        rpc = Presence("877219232096596010")
        rpc.connect()
        console.print("[green4]Connected to Discord![/green4]")
        console.print("Your status will be refreshed in every 15 seconds.\n", style = "white")
        current_time = int(time.time())
        time.sleep(10)
        # Send update
        while True:
            if account.needs_refresh:
                console.print("Session requires refreshing, hold on...", style = "grey78")
                account.refresh()
                config["refresh_token"] = account.session.refresh_token
            console.clear()
            rpc.update(
                details = profile.id + ("" if not profile.platform else " ( " + profile.platform + " )"),
                state = \
                    "Offline" if not profile.online else \
                    "Idle" if not profile.game else \
                    profile.game.name,
                large_text = "Playcord",
                large_image = "logo",
                start = current_time
            )
            console.print(
                "─" * 20,
                profile.id,
                profile.platform or "No device found.",
                "[bold][green4]■ IN GAME[/green4][/bold]" if profile.playing else \
                "[bold][yellow1]■ IDLE[/yellow1][/bold]" if profile.online else \
                "[bold][grey78]■ OFFLINE[/grey78][/bold]",
                "No any game running." if not profile.game else profile.game.name,
                "─" * 20,
                "[white]You can minimize the console window. Your presence will be updated in every 15 seconds.[/white]",
                "[white]If you want to stop showing Rich Presence, simply close the window or press Ctrl + C.[/white]",
                sep = "\n"
            )
            profile = account.profile()
            time.sleep(15)