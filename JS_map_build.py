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

    # 인덱스를 key로, 텍스트를 value로 저장
    # ex)
    # sentences_dict = {
    #   0 : "소나무가 있다",
    #   1 : "소나무가 없다"
    # }

    texts_dict = {}
    for idx, text in enumerate(texts):
        texts_dict[idx] = text

    # 텍스트 맵 저장
    with open('./texts_dict.json', 'w', encoding='UTF-8') as f:
        json.dump(texts_dict, f, indent='\t', ensure_ascii=False)

    # 텍스트 맵의 텍스트을 순회하면서 토큰 역색인 맵 만들기
    # 토큰 번호를 key로, 그 토큰이 포함된 텍스트 인덱스 리스트를 value로 저장
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
    for idx in tqdm(texts_dict):
        sentence = texts_dict[idx]
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