
import pickle
import math
import pandas as pd
import csv
from tqdm import trange
from utils.define import logger, TRAIN_DATASET_PICKLE_PATH, VALID_DATASET_PICKLE_PATH, BASEPATH
from utils.save import save_pickle


def load_targets(label_paths):
    """
    Provides dictionary of filename and labels
    Inputs: label_paths
        - **label_paths**: set of label paths
    Outputs: target_dict
        - **target_dict**: dictionary of filename and labels
    """
    target_dict = dict()
    for idx in trange(len(label_paths)):
        label_txt = label_paths[idx]
        with open(file=label_txt, mode="r") as f:
            label = f.readline()
            file_num = label_txt.split('/')[-1].split('.')[0].split('_')[-1]
            target_dict['KaiSpeech_label_%s' % file_num] = label
    save_pickle(target_dict, BASEPATH + "/data/pickle/target_dict.bin", message="target_dict save complete !!")
    return target_dict

def load_data_list(data_list_path, dataset_path):
    """
    Provides set of audio path & label path
    Inputs: data_list_path
        - **data_list_path**: csv file with training or test data list
    Outputs: audio_paths, label_paths
        - **audio_paths**: set of audio path
        - **label_paths**: set of label path
    """
    data_list = pd.read_csv(data_list_path, "r", delimiter = ",", encoding="cp949")
    audio_paths = list(dataset_path + data_list["audio"])
    label_paths = list(dataset_path + data_list["label"])

    return audio_paths, label_paths

def load_label(label_path, encoding='utf-8'):
    """
    Provides char2index, index2char
    Inputs: label_path
        - **label_path**: csv file with character labels
    Outputs: char2index, index2char
        - **char2index**: char2index[ch] = id
        - **index2char**: index2char[id] = ch
    """
    char2index = dict()
    index2char = dict()
    with open(label_path, 'r', encoding=encoding) as f:
        labels = csv.reader(f, delimiter=',')
        next(labels)

        for row in labels:
            char2index[row[1]] = row[0]
            index2char[int(row[0])] = row[1]

    return char2index, index2char

def load_pickle(filepath, message=""):
    with open(filepath, "rb") as f:
        load_result = pickle.load(f)
        logger.info(message)
        return load_result

def load_dataset(hparams, audio_paths, valid_ratio=0.05):
    batch_num = math.ceil(len(audio_paths) / hparams.batch_size)
    valid_batch_num = math.ceil(batch_num * valid_ratio)
    train_batch_num = batch_num - valid_batch_num
    if hparams.use_augmentation: train_batch_num *= int(1 + hparams.augment_ratio)

    with open(TRAIN_DATASET_PICKLE_PATH, 'rb') as f:
        train_dataset = pickle.load(f)

    with open(VALID_DATASET_PICKLE_PATH, 'rb') as f:
        valid_dataset = pickle.load(f)

    return train_batch_num, train_dataset, valid_dataset