# DESHIN: Dynamic and Extractive Summarizer towards Human Interests on News #
*Said "dishing" - _Serving nutritious texts on smaller dishes._

> Authors:
>> Raul Sena, Victor Bursztyn and Ygor Canalli. - {raulsf,vbursztyn,canalli}@cos.ufrj.br

> Corpus credits:
>> CSTNews (by Aleixo, Pardo et al.) - http://www.icmc.usp.br/~taspardo/sucinto/index.html

#1. Requirements:
* MongoDB
* Virtualenv - After installing it:
 * virtualenv venv
  * . venv/bin/activate
   * pip install -r requirements.txt

P.S: If you experienced the following error: "ImportError: No module named pymongo" you can try these commands:

``` $ easy_install -U setuptools
$ python -m easy_install pymongo ```

#2. Usage:
* Pre-processing:
 * . venv/bin/activate
  * bash run_etl.sh
* Batch summarizer:
 * . venv/bin/activate
  * bash run_experiment.sh
