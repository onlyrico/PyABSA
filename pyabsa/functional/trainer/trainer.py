# -*- coding: utf-8 -*-
# file: trainer.py
# time: 2021/4/22 0022
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import os

from pyabsa import __version__
from pyabsa.functional.config.config_manager import ConfigManager
from pyabsa.utils.dataset_utils import detect_dataset
from pyabsa.core.apc.prediction.sentiment_classifier import SentimentClassifier
from pyabsa.core.apc.training.apc_trainer import train4apc
from pyabsa.core.atepc.prediction.aspect_extractor import AspectExtractor
from pyabsa.core.atepc.training.atepc_trainer import train4atepc
from pyabsa.core.tc.prediction.text_classifier import TextClassifier
from pyabsa.core.tc.training.classifier_trainer import train4classification

from pyabsa.functional.config.apc_config_manager import APCConfigManager
from pyabsa.functional.config.atepc_config_manager import ATEPCConfigManager
from pyabsa.functional.config.classification_config_manager import ClassificationConfigManager
from pyabsa.utils.logger import get_logger

from autocuda import auto_cuda, auto_cuda_name


def init_config(config, auto_device=True):
    if config:
        if auto_device:
            config.device = auto_cuda()
            config.device_name = auto_cuda_name()
        # reload hyper-parameter from parameter dict

    config.model_name = config.model.__name__.lower()
    config.Version = __version__

    if 'use_syntax_based_SRD' in config:
        print('-' * 130)
        print('Force to use syntax distance-based semantic-relative distance,'
              ' however Chinese is not supported to parse syntax distance yet!  ')
        print('-' * 130)
    return config


class Trainer:
    def __init__(self,
                 config: ConfigManager = None,
                 dataset: str = None,
                 from_checkpoint: str = None,
                 save_checkpoint: bool = True,
                 auto_device: bool = True):
        """

        :param config: PyABSA.config.ConfigManager
        :param dataset: Dataset name or path
        :param from_checkpoint: A checkpoint path to train based on
        :param save_checkpoint: Save trained model to checkpoint, otherwise return the checkpoint
        :param auto_device: Auto choose cuda device if any
        """
        if isinstance(config, APCConfigManager):
            self.train_func = train4apc
            self.model_class = SentimentClassifier
            self.task = 'apc'
        elif isinstance(config, ATEPCConfigManager):
            self.train_func = train4atepc
            self.model_class = AspectExtractor
            self.task = 'atepc'
        elif isinstance(config, ClassificationConfigManager):
            self.train_func = train4classification
            self.model_class = TextClassifier
            self.task = 'classification'

        self.config = config
        self.dataset_file = detect_dataset(dataset, task=self.task)
        self.config.dataset_file = self.dataset_file
        self.config = init_config(self.config, auto_device)
        self.config.dataset_path = dataset
        self.from_checkpoint = from_checkpoint
        self.save_checkpoint = save_checkpoint
        log_name = '_'.join([self.config.model_name if 'model_name' in self.config.args else '',
                             os.path.basename(self.config.dataset_path)])
        self.logger = get_logger(os.getcwd(), log_name=log_name, log_type='training')

        if save_checkpoint:
            config.model_path_to_save = os.path.join(os.getcwd(), 'checkpoints')
        else:
            config.model_path_to_save = None

        self.train()

    def train(self):
        if isinstance(self.config.seed, int):
            self.config.seed = [self.config.seed]

        model_path = []
        seeds = self.config.seed
        for _, s in enumerate(seeds):
            self.config.seed = s
            if self.save_checkpoint:
                model_path.append(self.train_func(self.config, self.from_checkpoint, self.logger))
            else:
                # always return the last trained model if dont save trained model
                model = self.model_class(model_arg=self.train_func(self.config, self.from_checkpoint, self.logger))
        while self.logger.handlers:
            self.logger.removeHandler(self.logger.handlers[0])

        if self.save_checkpoint:
            return self.model_class(max(model_path))
        else:
            return model


class APCTrainer(Trainer):
    pass


class ATEPCTrainer(Trainer):
    pass


class TextClassificationTrainer(Trainer):
    pass
