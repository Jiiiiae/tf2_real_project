
#두 개의 사전에 특별한 기호 추가
_PAD = "_PAD"   #패딩 기호 (padding)
_GO = "_GO"     #두 문장을 나누는 기호 (시작 부분을 나타냄_)
_EOS = "_EOS"   #문장 끝을 가리키는 기호 (end of sentence)
_UNK = "_UNK"   #매우 드물게 등장하는 단어 (unknown)
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3
OP_DICT_IDS = [PAD_ID, GO_ID, EOS_ID, UNK_ID]