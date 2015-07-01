# DESHIN: Dynamic and Extractive Summarizer towards Human Interests on News #
*Said "dishing" - _Serving nutritious texts on smaller dishes._

> Authors:
>> Raul Sena, Victor Bursztyn and Ygor Canalli. - {raulsf,vbursztyn,canalli}@cos.ufrj.br

> Corpus credits:
>> CSTNews (by Aleixo, Pardo et al.) - http://www.icmc.usp.br/~taspardo/sucinto/index.html

#1. Requirements:
* Python 2.7 (restriction due to OR-tools dependency)
* MongoDB
* Virtualenv (includes suitable versions for Python and pip):
 * Create your virtualenv
  * pip install -r requirements.txt
* OR-tools
 * In case pip fails at OR-tools, please follow the instructions to install it manually [ https://developers.google.com/optimization/installing ]
  * In the worst case, download and easy_install its egg directly [ https://pypi.python.org/simple/ortools/ ]
* NLTk Trainer on MacMorpho
 * Activate your virtualenv
  * At project's root:
   * python -m nltk.downloader punkt mac_morpho stopwords
    * python $VIRTUAL_ENV/src/nltk-trainer-master/train_tagger.py mac_morpho --filename aggregator/pos_tagger/mac_morpho_pos_tagger.pickle --no-eval

Ensure you have all dependencies correctly installed before attempting to run DESHIN.

#2. Usage:
* Pre-processing:
 * Activate your virtualenv
  * bash run_etl.sh
* Batch summarizer:
 * Activate your virtualenv
  * bash run_experiment.sh
