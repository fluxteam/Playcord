import playcord
import sys
import traceback
import os
import httpx
from readsettings import ReadSettings
from pathlib import Path

if __name__ == '__main__':
    config = ReadSettings(str(Path.home().resolve() / "playcord.toml"))
    try:
        playcord.main(config)
    except httpx.HTTPStatusError:
        if "access_token" in config.data:
            del config["access_token"]
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except Exception as error:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        message = os.linesep.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
        print(message)
        stop = input()