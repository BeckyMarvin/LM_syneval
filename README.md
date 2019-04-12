# Targeted Syntactic Evaluation of LMs
This repository contains data and evaluation code for the following paper:

R. Marvin and T. Linzen. 2018. Targeted Syntactic Evaluation of Language Models. Proceedings of EMNLP. 

## HOW TO USE THIS CODE

### Language model training data

We used the same training data as Gulordava et al. (2018). Each corpus consists of around 100M tokens from English Wikipedia. We used training (80M) and validation (10M) subsets in our experiments. All corpora were shuffled at sentence level. Links to download the data are below:

[train](https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/train.txt) / [valid](https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/valid.txt) / [test](https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/test.txt) / [vocab](https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/vocab.txt)


### Training the language models

We provide the code used to train both LSTMS.

To train a basic LSTM language model:
```
python main.py --lm_data data/lm_data --save models/lstm_lm.pt --save_lm_data models/lstm_lm.bin
```

To train a multitask LSTM model (jointly trained to do language modeling and CCG supertagging):
```
python main.py --lm_data data/lm_data --ccg_data data/ccg_data --save models/lstm_multi.pt --save_lm_data models/lstm_multi.bin
```

Alternatively, you can train a language model or multitask model by using the `train_lm.sh` or `train_multitask.sh` scripts (found in `example_scripts`). Alternate hyperparameters can be specified in the `hyperparameters.txt` file.

For our ngram model, we used the [SRILM toolkit](http://www.speech.sri.com/projects/srilm/) to train a 5-gram language model. If you use a different ngram package, the code for testing your ngram model in `LM_eval.py` will likely have to be modified slightly. 

### Testing the language models
PERPLEXITY ONLY: 
Language model:
```
python main.py --test --lm_data data/lm_data --save models/$model_pt --save_lm_data models/$model_bin
```

Multitask model:
```
python main.py --test --lm_data data/lm_data
```

MORE DETAILED SYNTACTIC EVALUATION:
1. Make templates.

You can make the default templates by running
```
python make_templates.py $TEMPLATE_DIR
```

where $TEMPLATE_DIR is the directory where all of the different kinds of tests will be stored.

If you want to modify the test cases or the lexical items, you can do so in `template/Templates.py` or `template/Terminals.py`, respectively. All the test cases that will be generated can be found in `template/TestCases.py`. 

2. Test the model.
```
python LM_eval.py --model models/$model_pt --lm_data models/$model_bin --model_type $TYPE
```
where $TYPE is rnn, multitask, or ngram. You must specify the name of the checkpoint file for your model, in addition to model's .bin file (this speeds up the loading process).

To see a full list of the commands for testing your model, run
```
python LM_eval.py -h
```
3. Analyze the results.

Now that we have log probabilities from the ngram and RNN models on all of the sentences we're interested in, we want to see how well these models did on various pairs of sentences. 

These results have been stored in Python dictionaries, and are organized by the type of construction as well as which components are matched/mismatched (e.g. singular subject and plural verb, etc.)

You can run
```
python analyze_results.py --results_file $RESULTS_FILE --model_type $TYPE --mode $MODE
```
where $RESULTS is the path to the file where the RNN LM/multitask or ngram results were dumped, $MODEL_TYPE is the type of model (rnn/multitask/ngram) and $MODE is an optional argument that can be 'full' or 'condensed' or 'overall' (default is 'overall').

At the 'condensed' level, we report the accuracies for each sub-division of the sentences we're interested in analyzing. For example, you might want to know the percent of time the model preferred the grammatical over ungrammatical sentence when there was a main subject/verb mismatch vs. the percent of time the model preferred the grammatical over ungrammatical sentence when there was an embedded subject/verb mismatch. This info level suppresses individual sentence pairs and shows you the scores for these subgroups.

In addition to the scores above, at the 'full' level, we will sample some sentences that the model gets correct/incorrect and display the log probabilities of the model at each word in the sentence. This kind of measure can be used to determine if there are strong lexical biases in the model that have an effect on the overall performance.

If you don't specify a 'full' or 'condensed' info level, then only the total accuracies for each test will be reported.

The full list of commands for analyzing results can be found by typing
```
python analyze_results.py -h
```
For example, if you specify --anim, you can look at whether the animacy of the subjects/verbs has an effect on the language models' ability to succeed at certain syntactic constructions. 