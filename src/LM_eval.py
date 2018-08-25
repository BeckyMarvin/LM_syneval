import argparse
import pickle
import os
import subprocess
import operator
from progress.bar import Bar
from tester import TestWriter
from template.TestCases import TestCase

parser = argparse.ArgumentParser(description="Parameters for testing a language model")

parser.add_argument('--template_dir', type=str, default='../EMNLP2018/templates',
                    help='Location of the template files')
parser.add_argument('--output_file', type=str, default='all_test_sents.txt',
                    help='File to store all of the sentences that will be tested')
parser.add_argument('--model', type=str, default='../models/model.pt',
                    help='The model to test')
parser.add_argument('--lm_data', type=str, default='../models/model.bin',
                    help='The model .bin file that accompanies the model (for faster loading)')
parser.add_argument('--tests', type=str, default='all',
                    help='Which constructions to test (agrmt/npi/all)')
parser.add_argument('--model_type', type=str, required=True,
                    help='Which kind of model (RNN/multitask/ngram)')

args = parser.parse_args()

writer = TestWriter(args.template_dir, args.output_file)
testcase = TestCase()
if args.tests == 'agrmt':
    tests = testcase.agrmt_cases
elif args.tests == 'npi':
    tests = testcase.npi_cases
else:
    tests = testcase.all_cases

all_test_sents = {}
for test_name in tests:
    test_sents = pickle.load(open(template_dir+"/"+test_name+".pickle", 'rb'))
    all_test_sents[test_name] = test_sents

writer.write_tests(all_test_sents)
name_lengths = writer.name_lengths
key_lengths = writer.key_lengths
test_LM(name_lengths, key_lengths, args.model, args.lm_data)

def test_LM(name_lengths, key_lengths, model, lm_data):
    if args.model_type.lower() == "ngram":
        logging.info("Testing unigram...")
        os.system('./test_unigram.sh > unigram.output')
        unigram_results = score_unigram(name_lengths, key_lengths)
        with open(args.model_type+"_unigram_results.pickle", 'wb') as f:
            pickle.dump(unigram_results, f)
        logging.info("Testing ngram...")
        os.system('./test_ngram.sh > ngram.output')
        results = score_ngram(name_lengths, key_lengths, unigram_results)
    else:       
        logging.info("Testing RNN...")
        os.system('../example_scripts/test.sh '+ model + ' ' + lm_data + ' > '+ 'rnn.output')
        results = score_rnn(name_lengths, key_lengths)
    with open(args.model_type+"_results.pickle", 'wb') as f:
        pickle.dump(results, f)

def score_unigram(name_lengths, key_lengths):
    print "Scoring unigram..."
    fin = open("unigram.output", 'r')
    all_scores = {}
    sent = ""
    prevLineEmpty = True
    i = 0
    for line in fin:
        if "p( " in line:
            word = line.split("p( ")[1].split(" |")[0]
            score = float(line.split("[ ")[-1].split(" ]")[0])
            if word not in all_scores:
                all_scores[word] = score
    fin.close()
    return all_scores

def score_ngram(name_lengths, key_lengths, unigram_results):
    fin = open("ngram.output", 'r')
    all_scores = {}
    i = 0
    finished = True
    sent = []
    prev_sentid = -1
    for line in fin:
        if "p(" in line:
            finished = False
        if not finished and "</s>" not in line:
            word = line.split("p( ")[1].split(" |")[0]
            score = float(line.split("[ ")[-1].split(" ]")[0])
            sent.append((word,score))
            if word == ".":
                name_found = False
                for (k1,v1) in sorted(name_lengths.items(), key=operator.itemgetter(1)):
                    if i < v1 and not name_found:
                        name_found = True
                        if k1 not in all_scores:
                            all_scores[k1] = {}
                        key_found = False
                        for (k2,v2) in sorted(key_lengths[k1].items(), key=operator.itemgetter(1)):
                            if i <  v2 and not key_found:
                                key_found = True
                                if k2 not in all_scores[k1]:
                                    all_scores[k1][k2] = []
                                all_scores[k1][k2].append(sent)
                sent = []
                if i != prev_sentid+1:
                    logging.info("Error at sents "+sentid+" and "+prev_sentid)
                prev_sentid = i
                finished = True
                i += 1
        else:
            finished = True
    fin.close()
    return all_scores


def score_rnn(name_lengths, key_lengths):
    logging.info("Scoring RNN...")
    with open('rnn.output', 'r') as f:
        all_scores = {}
        first = False
        score = 0.
        sent = []
        prev_sentid = -1
        for line in fin:
            if line.strip() == "":
                first = True
            elif "===========================" in line:
                first = False
                break
            elif first and len(line.strip().split()) == 6 and "torch.cuda" not in line:
                wrd, sentid, wrd_score = [line.strip().split()[i] for i in [0,1,4]]
                score = -1 * float(wrd_score) # multiply by -1 to turn surps back into logprobs
                sent.append((wrd, score))
                if wrd == ".":
                    name_found = False
                    for (k1,v1) in sorted(name_lengths.items(), key=operator.itemgetter(1)):
                        if float(sentid) < v1 and not name_found:
                            name_found = True
                            if k1 not in all_scores:
                                all_scores[k1] = {}
                            key_found = False
                            for (k2,v2) in sorted(key_lengths[k1].items(), key=operator.itemgetter(1)):
                                if int(sentid) <  v2 and not key_found:
                                    key_found = True
                                    if k2 not in all_scores[k1]:
                                        all_scores[k1][k2] = []
                                    all_scores[k1][k2].append(sent)
                    sent = []
                    if float(sentid) != prev_sentid+1:
                        logging.info("Error at sents "+sentid+" and "+prev_sentid)
                    prev_sentid = float(sentid)
    return all_scores

def clean_files(mode):
    if args.model_type.lower() == 'ngram':
        os.system('rm ngram.output unigram.output')
    else:
        os.system('rm rnn.output')
