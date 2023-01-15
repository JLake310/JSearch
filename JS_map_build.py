from glob import glob
from tqdm import tqdm
from transformers import ElectraTokenizer
import json
import argparse
import time

if __name__=='__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='../data/finetune')
    args = parser.parse_args()

    tokenizer = ElectraTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")

    # 텍스트 파일 리스트 가져오기
    files = glob('{}/*.txt'.format(args.data_dir))

    # 리스트에 텍스트 저장
    texts = []
    for file in tqdm(files):
        with open(file, 'r', encoding='utf8') as f:
            text = f.read()
            if len(text)==0: continue
            texts.append(text)

    # 문장 단위로 파싱
    sentences = []
    for text in tqdm(texts):
        text_ = text.split(". ")
        for line in text_:
            if len(line) == 0: continue
            sentences.append(line)

    # 인덱스를 key로, 문장을 value로 저장
    # ex)
    # sentences_dict = {
    #   0 : "소나무가 있다",
    #   1 : "소나무가 없다"
    # }
    sentences_dict = {}
    for idx, sentence in enumerate(sentences):
        sentences_dict[idx] = sentence

    # 문장 맵 저장
    with open('./sentences_dict.json', 'w', encoding='UTF-8') as f:
        json.dump(sentences_dict, f, indent='\t', ensure_ascii=False)

    # 문장 맵의 문장을 순회하면서 토큰 역색인 맵 만들기
    # 토큰 번호를 key로, 그 토큰이 포함된 문장 인덱스 리스트를 value로 저장
    # ex)
    # 소나무가 있다는 토큰으로 [13876, 4070, 3249, 4176],
    # 소나무가 없다는 토큰으로 [13876, 4070, 3123, 4176] 이므로
    # tokens_dict = {
    #   13876: [0, 1],
    #   4070: [0, 1],
    #   3249: [0],
    #   3123: [1],
    #   4176: [0, 1]
    # }
    # 처럼 저장됨
    tokens_dict = {}
    for idx in tqdm(sentences_dict):
        sentence = sentences_dict[idx]
        tokens = tokenizer.tokenize(sentence)
        tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
        tokens_ids = set(tokens_ids)
        for token_id in tokens_ids:
            if token_id not in tokens_dict:
                tokens_dict[token_id] = [idx]
            else:
                tokens_dict[token_id].append(idx)

    # 토큰 맵 저장
    with open('./tokens_dict.json', 'w', encoding='UTF-8') as f:
        json.dump(tokens_dict, f, indent='\t', ensure_ascii=False)

    end = time.time()
    print(f"{end - start:.5f} sec")

    # 총 실행 서버 기준 1분 40초 가량 소요