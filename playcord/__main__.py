import playcord
import sys
import traceback
import os
from playcord.gui import main

if __name__ == '__main__':
    try:
        main().main_loop()
        # playcord.main(config)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except Exception as error:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        message = os.linesep.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
        print(message)