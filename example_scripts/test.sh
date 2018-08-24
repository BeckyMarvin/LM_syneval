#!/bin/bash

source ../hyperparameters.txt

python $lm_dir/main.py
    --test
    --lm_data $lm_data_dir
    --cuda
    # two lines below test language model
    --save $model_dir/lstm_lm.pt
    --save_lm_data $model_dir/lstm_lm.bin
    # uncomment lines below to test multitask model
    # --save $model_dir/lstm_multi.pt
    # --save_lm_data $model_dir/lstm_multi.bin 
    --words