import sys
from dsklayout.util import import_all_from
import_all_from(sys.modules[__package__], '.src5', '.'.join(__package__.split('.')[0:-1]))
