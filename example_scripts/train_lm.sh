#!/bin/bash
source ../hyperparameters.txt

python $lm_dir/main.py \
    --lm_data $lm_data_dir \
    --cuda \
    --epochs $epochs \
    --model $LSTM \
    --nhid $num_hid \
    --save $model_dir/lstm_lm.pt \
    --save_lm_data $model_dir/lstm_lm.bin \
    --log-interval $log_freq \
    --batch $batch_size \
    --dropout $dropout \
    --lr $lr
