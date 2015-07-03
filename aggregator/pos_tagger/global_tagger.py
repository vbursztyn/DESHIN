

from globals import POS_TAGGER_PATH

import pickle


fPosTagger = open(POS_TAGGER_PATH)
tagger = pickle.load(fPosTagger)