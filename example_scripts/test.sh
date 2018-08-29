#!/bin/bash

source ../hyperparameters.txt

python $lm_dir/main.py \
    --test \
    --lm_data $1 \
    --cuda \
    --save $2 \
    --save_lm_data $3 \
    --testfname $4 \
    --words
    # replace the lines above with these to test multitask model
    # --save $model_dir/lstm_multi.pt
    # --save_lm_data $model_dir/lstm_multi.bin 
