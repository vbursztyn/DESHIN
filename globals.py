COLLECTIONS_PATH="../data/collections/collections.txt"
SUBJECTS_BASE_PATH = "../data/subjects/"
ARTICLES_RELATIVE_PATH="/Textos-fonte/"
ARTICLE_TITLE_SUFFIX="_titulo"
SUMMARY_RELATIVE_PATH="/Sumarios/"
SUMMARY_SUFFIX="_extrato_humano"

DB_CONFIG = { "host" : "127.0.0.1:27017", "db" : "test" }
DB_NAMESPACE_COLLECTIONS = "DESHINCollections"
DB_NAMESPACE_SUBJECTS = "DESHINSubjects"
DB_DEFAULT_COLLECTIONS_KEY = "collections"

FEATURES_MIN_THRESHOLD = 0.1

POS_TAGGER_PATH = "aggregator/pos_tagger/mac_morpho_pos_tagger.pickle"

RESULTS_PATH = "final_results.json"