from json import load
from collections import OrderedDict
from os.path import splitext, dirname, join


locals().update(load(open('%s.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict))
filename = join(dirname(__file__), filename)
