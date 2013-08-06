from json import load
from collections import OrderedDict
from os.path import splitext


locals().update(load(open('%s.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict))
