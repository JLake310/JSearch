from transformers import ElectraTokenizer
import json
import argparse
import time

def load_map(type):
    f = open('{}s_dict.json'.format(type), 'r', encoding='utf8')
    dict_from_json = json.load(f)
    return dict_from_json

if __name__=='__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, default='만남')
    args = parser.parse_args()

    tokenizer = ElectraTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")

    # 맵 불러오기
    sentences_dict_from_json = load_map("sentence")
    tokens_dict_from_json = load_map("token")

    # 쿼리 토크나이징
    input_word = args.query
    word_to_token = tokenizer.tokenize(input_word)
    token_to_ids = tokenizer.convert_tokens_to_ids(word_to_token)

    # 쿼리의 토큰이 포함된 문장 인덱스 추출: 복잡도 O(1) * (쿼리 토큰 갯수)
    sentences_ids = ()
    for token_to_id in token_to_ids:
        if len(sentences_ids) == 0: sentences_ids = set(tokens_dict_from_json[str(token_to_id)])
        else : sentences_ids &= set(tokens_dict_from_json[str(token_to_id)])
    
    # 위에서 추출한 id로 문장 맵 순회: 복잡도 O(1) * (id set 길이)
    result_sentences = []
    for _id in sentences_ids:
        result_sentences.append(sentences_dict_from_json[str(_id)])
    result_set = '. '.join(result_sentences)

    with open('./dataset/{}.txt'.format(input_word), 'w', encoding='UTF-8') as f:
        f.write(result_set)

    # 최대 O(n), n은 전체 문장 개수로 데이터셋 추출 가능
    # 문장 개수 980만개 가량에서 "사랑"이라는 키워드 추출 약 5초 소요
    # 키워드 개수 상관 없이 5초 이내로 일정하게 추출
    end = time.time()
    print(f"{end - start:.5f} sec")