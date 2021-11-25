import pickle
import re
from collections import Counter
from nltk.corpus import comtrans
import data_utils

def retrieve_corpora(translated_sentences_l1_l2='alignment-de-en.txt'):
    """ 말뭉치를 검색하는 함수
    Args : NLTK Clomtrans 말뭉치의 정렬된 문장을 포함한 파일 하나
    Return : 원어와 번역어 두 개의 토큰 리스트
    """

    print("Retrieving corpora: {}".format(translated_sentences_l1_l2))
    als = comtrans.aligned_sents(translated_sentences_l1_l2)
    sentences_l1 = [sent.words for sent in als]
    sentences_l2 = [sent.mots for sent in als]
    return sentences_l1, sentences_l2

def clean_sentences(sentence):
    """ 토큰을 정리하는 함수.
    구두점을 토큰화하고 투큰을 소문자로 변환
    """
    regex_splitter = re.compile("([!?.,:;$\"')( ])")
    clean_words = [re.split(regex_splitter, word.lower()) for word in sentence]
    return [w for words in clean_words for w in words if words if w]

def filter_sentence_length(sentences_l1, sentences_l2, min_len=0, max_len=15):
    """토큰 개수가 max_len보다 크면 두 언어의 각 문장들이 삭제됨
    Args : sen_l1, sen_l2, min_len, max_len
    """
    filtered_sentences_l1 = []
    filtered_sentences_l2 = []
    for i in range(len(sentences_l1)):
        if min_len <= len(sentences_l1[i]) <= max_len and \
            min_len <= len(sentences_l2[i]) <= max_len:
            filtered_sentences_l1.append(sentences_l1[i])
            filtered_sentences_l2.append(sentences_l2[i])
    return filtered_sentences_l1, filtered_sentences_l2

def create_indexed_dictionary(sentences, dict_size=10000, storage_path=None):
    """사전은 알고리즘을 훈련하는 동안 생성됨.
    Args : 사전의 항목 개수, 사전을 저장할 경로
    Return : 빈도 수에 따른 id와 토큰을 연결한 사전
    """
    count_words = Counter() #Counter class : 데이터의 개수들을 반환
    dict_words = {}
    opt_dict_size = len(data_utils.OP_DICT_IDS)
    for sen in sentences:
        for word in sen:
            count_words[word] += 1

    dict_words[data_utils._PAD] = data_utils.PAD_ID
    dict_words[data_utils._GO] = data_utils.GO_ID
    dict_words[data_utils._EOS] = data_utils.EOS_ID
    dict_words[data_utils._UNK] = data_utils.UNK_ID

    for idx, item in enumerate(count_words.most_common(dict_size)): #개수가 많은 순서대로,받는 인수만큼 리턴 
        dict_words[item[0]] = idx + opt_dict_size

    if storage_path:
        pickle.dump(dict_words, open(storage_path, "wb"))
    return dict_words


def sentences_to_indexs(sentences, indexed_dictionary):
    """토큰을 id로 대체하는 함수
    """
    indexed_sentences = []
    not_found_counter = 0
    for sent in sentences:
        idx_sent = []
        for word in sent:
            try:
                idx_sent.append(indexed_dictionary[word])
            except KeyError:
                idx_sent.append(data_utils.UNK_ID)
                not_found_counter += 1
        indexed_sentences.append(idx_sent)

    print('[sentences_to_indexs] Did not find {} words'.format(not_found_counter))
    return indexed_sentences

def sentence_to_indexs(sentence, indexed_dictionary):
    """토큰을 id로 대체하는 함수
    """
    indexed_sentence = []
    not_found_counter = 0
   
    for word in sentence:
        try:
            indexed_sentence.append(indexed_dictionary[word])
        except KeyError:
            indexed_sentence.append(data_utils.UNK_ID)
            not_found_counter += 1


    print('[sentences_to_indexs] Did not find {} words'.format(not_found_counter))
    return indexed_sentence

def extract_max_length(corpora):
    """문장의 최대 길이를 추출하기 위한 함수
    앞서, 제한한 최대 길이와 동일한 값을 반환함
    """
    return max([len(sentence) for sentence in corpora])

def prepare_sentences(sentences_l1, sentences_l2, len_l1, len_l2):
    """sequece 길이를 통일, 없는 토큰은 패딩으로 채움, 두 번째 언어 처음과 끝에 해당 기호 추가
    Return : [l1, l2]
    """
    assert len(sentences_l1) == len(sentences_l2), "첫 번째 언어와 두 번째 언어의 최대 길이가 다름"
    data_set = []
    for i in range(len(sentences_l1)):
        padding_l1 = len_l1 - len(sentences_l1[i])
        pad_sentence_l1 = [data_utils.GO_ID] + sentences_l1[i] + [data_utils.EOS_ID] + ([data_utils.PAD_ID] * padding_l1)

        padding_l2 = len_l2 - len(sentences_l2[i])
        pad_sentence_l2 = [data_utils.GO_ID] + sentences_l2[i] + [data_utils.EOS_ID] + ([data_utils.PAD_ID] * padding_l2)
        data_set.append([pad_sentence_l1, pad_sentence_l2])

    return data_set
