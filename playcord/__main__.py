import playcord
import sys
import traceback
import os
import httpx
from playcord.config import Configuration

if __name__ == '__main__':
    try:
        playcord.main()
    except httpx.HTTPStatusError:
        config = Configuration()
        if "access_token" in config["session"]:
            config["session"].pop("access_token")
        config.save()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except Exception as error:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        message = os.linesep.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
        print(message)
        stop = input()