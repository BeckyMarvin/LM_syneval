# Targeted Syntactic Evaluation of LMs
This repository contains data and evaluation code for the following paper:

R. Marvin and T. Linzen. 2018. Targeted Syntactic Evaluation of Language Models. Proceedings of EMNLP. 

## HOW TO USE THIS CODE

### Training data based on Wikipedia

Each corpus consists of around 100M tokens, we used training (80M) and validation (10M) subsets in our experiments. All corpora were shuffled at sentence level.

-[train](https://s3.amazonaws.com/colorless-green-rnns/training-data/English/train.txt) / [valid](https://s3.amazonaws.com/colorless-green-rnns/training-data/English/valid.txt) / [test](https://s3.amazonaws.com/colorless-green-rnns/training-data/English/test.txt) / [vocab](https://s3.amazonaws.com/colorless-green-rnns/training-data/English/vocab.txt)


TRAINING:

We provide the code used to train both LSTMS.

To train a basic LSTM language model:
python main.py --lm_data data/lm_data --save models/lstm_lm.pt --save_lm_data models/lstm_lm.bin

To train a multitask LSTM model:
python main.py --lm_data data/lm_data --ccg_data data/ccg_data --save models/lstm_multi.pt --save_lm_data models/lstm_multi.bin

Alternatively, you can train a language model or multitask model by using our train_lm.sh or train_multitask.sh scripts. Alternate hyperparameters can be specified in the hyperparameters.txt file.



TESTING (either model - both are tested on sentences only):
to test on Wikipedia sentences (to get perplexity only)
Language model:
python main.py --test --lm_data data/lm_data --save models/$model_pt --save_lm_data models/$model_bin

Multitask model:
python main.py --test --lm_data data/lm_data

To test on our sentences & get more detailed info:

1) Make templates.

You can make the default templates by running

python make_templates.py $TEMPLATE_DIR

where $TEMPLATE_DIR is the directory where all of the different kinds of tests will be stored.

If you want to modify the test cases or the lexical items, you can do so in template/Templates.py or template/Terminals.py, respectively. All the test cases that will be generated can be found in template/TestCases.py. 

2) Test the ngram model.

python run_ngram_test.py $TEMPLATE_DIR $TESTS

where $TEMPLATE_DIR is the directory you specified in step 1) above, and $TESTS is either 'all' (if you want to run all of the agreement tests) or specific tests (e.g. 'obj_rel_no_adverb') if you only want to test certain agreement scenarios.

3) Test the LSTM model(s).

python run_RNN_test.py $TEMPLATE_DIR $TESTS

where $TEMPLATE_DIR is the directory specified in step 1) and $TESTS is the same as in the ngram testing instructions above. The same command should be run for both the basic language model and the multitask model, as both are tested on full sentences.

4) Analyze the results.

Now that we have log probabilities from the ngram and RNN models on all of the sentences we're interested in, we want to see how well these models did on various pairs of sentences. 

These results have been stored in Python dictionaries, and are organized by the type of construction as well as which components are matched/mismatched (e.g. singular subject and plural verb, etc.)

You can run

python analyze_results.py $RNN_RESULTS $NGRAM_RESULTS $INFO_LEVEL

where $RNN_RESULTS is the path to the file where the RNN results were dumped, $NGRAM_RESULTS is the path to the file where the ngram results were dumped, and $INFO_LEVEL is an optional argument that can be 'full' or 'condensed'.

At the 'condensed' level, we report the accuracies for each sub-division of the sentences we're interested in analyzing. For example, you might want to know the percent of time the model preferred the grammatical over ungrammatical sentence when there was a main subject/verb mismatch vs. the percent of time the model preferred the grammatical over ungrammatical sentence when there was an embedded subject/verb mismatch. This info level suppresses individual sentence pairs and shows you the scores for these subgroups.

In addition to the scores above, at the 'full' level, we will sample some sentences that the model gets correct/incorrect and display the log probabilities of the model at each word in the sentence. This kind of measure can be used to determine if there are strong lexical biases in the model that have an effect on the overall performance.

If you don't specify a 'full' or 'condensed' info level, then only the total accuracies for each test will be reported.


