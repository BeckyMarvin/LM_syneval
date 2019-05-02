#!/bin/bash
source ../hyperparameters.txt

python $lm_dir/main.py \
    --lm_data $lm_data_dir \
    --ccg_data $ccg_data_dir \
    --cuda \
    --epochs $epochs \
    --model $model \
    --save $model_dir/lstm_multi.pt \
    --save_lm_data $model_dir/lstm_multi.bin \
    --log-interval $log_freq \
    --nlayers $nlayers \
    --batch_size $batch_size \
    --nhid $num_hid \
    --lr $lr \
    --trainfname $train \
    --validfname $valid \
    --testfname $test
