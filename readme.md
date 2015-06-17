# DESHIN: Dynamic and Extractive Summarizer towards Human Interests on News #
*Said "dishing" - _Serving nutritious texts on smaller dishes._

> Authors:
>> Raul Sena, Victor Bursztyn and Ygor Canalli. - {raulsf,vbursztyn,canalli}@cos.ufrj.br

#1. Requirements:
* MongoDB
* Virtualenv - After installing it:
 * virtualenv venv
  * . venv/bin/activate
   * pip install -r requirements.txt

#2. Usage:
* Pre-processing:
 * . venv/bin/activate
  * bash run_etl.sh
* Batch summarizer:
 * . venv/bin/activate
  * bash run_experiment.sh