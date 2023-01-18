from transformers import ElectraTokenizer
import json
import argparse
import time

def load_map(type):
    f = open('./{}s_dict.json'.format(type), 'r', encoding='utf8')
    dict_from_json = json.load(f)
    return dict_from_json

if __name__=='__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str)
    parser.add_argument('--option', type=str, default='or')
    args = parser.parse_args()

    input_word = args.query
    option = args.option
    if option != 'and' and option != 'or':
        print("option has to be 'and' or 'or'")
        exit(0)

    tokenizer = ElectraTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")

    # 맵 불러오기
    texts_dict_from_json = load_map("texts")
    tokens_dict_from_json = load_map("token")

    # 쿼리 토크나이징
    word_to_token = tokenizer.tokenize(input_word)
    token_to_ids = tokenizer.convert_tokens_to_ids(word_to_token)

    # 쿼리의 토큰이 포함된 텍스트 인덱스 추출: 복잡도 O(1) * (쿼리 토큰 갯수)
    texts_ids = ()
    for token_to_id in token_to_ids:
        if len(texts_ids) == 0: texts_ids = set(tokens_dict_from_json[str(token_to_id)])
        else :
            if option == 'and':
                texts_ids &= set(tokens_dict_from_json[str(token_to_id)])
            else:
                texts_ids |= set(tokens_dict_from_json[str(token_to_id)])
    
    # 위에서 추출한 id로 텍스트 맵 순회: 복잡도 O(1) * (id set 길이)
    result_sentences = []
    for _id in texts_ids:
        result_sentences.append(texts_dict_from_json[str(_id)])
    result_set = '. '.join(result_sentences)

    with open('./dataset/{}_{}.txt'.format(input_word, option), 'w', encoding='UTF-8') as f:
        f.write(result_set)

    end = time.time()
    print(f"{end - start:.5f} sec")