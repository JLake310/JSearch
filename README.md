# JSearch
 
_문장 색인 및 토큰 역색인을 활용한 특정 텍스트 포함 데이터셋 구성 툴_

_토크나이저 : monologg/koelectra-base-v3-discriminator_

### 0. Requirements
```
transformers==4.8.2
```

### 1. Mapping 
Usage
```
python JS_map_build --data_dir {dir}
```
Result => _두 개의 맵을 생성합니다._

_텍스트_
```
[
    소나무가 있다,
    소나무가 없다
]
```

_텍스트 맵_
```
인덱스를 key로, 텍스트를 value로 저장
sentences_dict = {
    0 : "소나무가 있다",
    1 : "소나무가 없다"
}
```

_토큰 맵_
```
토큰 번호를 key로, 그 토큰이 포함된 텍스트 인덱스 리스트를 value로 저장
"소나무가 있다"는 토큰 인덱스로 [13876, 4070, 3249, 4176],
"소나무가 없다"는 [13876, 4070, 3123, 4176] 이므로
tokens_dict = {
    13876: [0, 1],
    4070: [0, 1],
    3249: [0],
    3123: [1],
    4176: [0, 1]
}
```

### 2. Querying

> 2023.01.19</br>
> and/or 옵션이 추가되었습니다.</br>
> option</br>
> and : 모든 query 토큰들이 포함된 텍스트로 구성된 데이터셋을 반환하며,</br>
> or : 텍스트에 토큰들 중 하나라도 포함되어 있다면 데이터셋에 포함됩니다.

Usage
```
python JSearch.py --query {keywords} --option {and/or} # keywords ex) "사랑" "사랑 행복"
```
Result => {dataset/{keywords}_{option}.txt}에 추출된 데이터셋이 저장됩니다.

980만개 가량의 문장으로 실행했을 때, 5초 가량 소요됩니다.
