
from .ScriptEntry import ScriptEntry
from .ScriptDisplay import ScriptDisplay
from .CompDisplay import ComputationDisplay
from .ScriptFourm import ScriptFourm
from .CompEntry import CompEntry

import logging
import logging.config

# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logger_formatter)

logger.addHandler(ch)
logger.debug('Completed configuring logger for {name}!'.format(name=__name__))
