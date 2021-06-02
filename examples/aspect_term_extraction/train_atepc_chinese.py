# -*- coding: utf-8 -*-
# file: train_atepc.py
# time: 2021/5/21 0021
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

#  fine-tuning on custom dataset (w/o test dataset)

from pyabsa import train_atepc

# see hyper-parameters in pyabsa/main/training_configs.py
param_dict = {'model_name': 'lcf_atepc',
              'batch_size': 16,
              'seed': {996, 7, 666},
              'device': 'cuda',        # overrides auto_device parameter
              'num_epoch': 6,
              'optimizer': "adamw",    # {adam, adamw}
              'learning_rate': 0.00002,
              'pretrained_bert_name': "bert-base-chinese",
              'use_dual_bert': False,  # modeling the local and global context using different BERTs
              'use_bert_spc': False,   # Enable to enhance APC, not available for ATE or joint task of APC and ATE
              'max_seq_len': 80,
              'log_step': 5,           # Evaluate per steps
              'SRD': 3,                # Distance threshold to calculate local context
              'lcf': "cdw",            # {cdw, cdm, fusion}
              'dropout': 0.1,
              'l2reg': 0.00001,
              'polarities_dim': 3      # Categories of sentiment polarity
              }

save_path = 'state_dict'

# Mind that 'train_atepc' function only evaluates in last few epochs

train_set_path = 'atepc_datasets/Chinese/camera'
aspect_extractor = train_atepc(parameter_dict=param_dict,      # set param_dict=None to use default model
                               dataset_path=train_set_path,    # file or dir, dataset(s) will be automatically detected
                               model_path_to_save=save_path,   # set model_path_to_save=None to avoid save model
                               auto_evaluate=True,             # evaluate model while training if test set is available
                               auto_device=True                # Auto choose CUDA or CPU
                               )

train_set_path = 'atepc_datasets/Chinese/car'
aspect_extractor = train_atepc(parameter_dict=param_dict,      # set param_dict=None to use default model
                               dataset_path=train_set_path,    # file or dir, dataset(s) will be automatically detected
                               model_path_to_save=save_path,   # set model_path_to_save=None to avoid save model
                               auto_evaluate=True,             # evaluate model while training if test set is available
                               auto_device=True                # Auto choose CUDA or CPU
                               )

train_set_path = 'atepc_datasets/Chinese/notebook'
aspect_extractor = train_atepc(parameter_dict=param_dict,      # set param_dict=None to use default model
                               dataset_path=train_set_path,    # file or dir, dataset(s) will be automatically detected
                               model_path_to_save=save_path,   # set model_path_to_save=None to avoid save model
                               auto_evaluate=True,             # evaluate model while training if test set is available
                               auto_device=True                # Auto choose CUDA or CPU
                               )

train_set_path = 'atepc_datasets/Chinese/phone'
aspect_extractor = train_atepc(parameter_dict=param_dict,      # set param_dict=None to use default model
                               dataset_path=train_set_path,    # file or dir, dataset(s) will be automatically detected
                               model_path_to_save=save_path,   # set model_path_to_save=None to avoid save model
                               auto_evaluate=True,             # evaluate model while training if test set is available
                               auto_device=True                # Auto choose CUDA or CPU
                               )
