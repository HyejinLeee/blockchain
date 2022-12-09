### blockchain 해쉬 계산

각 블록의 식별자 역할을 하는 블록해쉬를 직접 계산해보았다.  
 
<br>
**블록해쉬를 구하는 과정을 요약** 하면 아래와 같다.  
---
 

1. 버전, 이전 블록 해쉬, 머클루트, 타임, bits, nonce 를 리틀엔디안 형식으로 변환한다.

2. 위의 정보들을 이어 붙인다. (이때 순서가 매우 중요!)

3. 위에서 이어 붙인 정보들을 바이너리 형태로 변환한다. 

4. SHA256 으로 변형 후 다시 SHA256 으로 변형한다.

5. 이렇게 얻은 결과값을 다시 역순으로 가지고 온다. 
---   

  
제일 시간이 많이 걸린건, [blockchain.info](https://www.blockchain.com/explorer) 에서 읽어온 블록의 구성 정보(버전, 시간, bits, nonce, 머클루트, 이전 블록 해쉬 )들을 리틀엔디안으로 변환하는 부분이다. (아마도 빠른 계산 속도 때문에 리틀엔디안으로 변환해야하지 않나(?) 추측해보지만 확실치는 않다. 이 부분을 알게되면 업데이트 해놓아야겠다.)

 

또 리틀엔디안을 변환하는 과정에서, 최근 블록들과 예전 블록들이 버전이 표시되는 길이가 달라 (예를 들어 125552 height 를 가진 블록의 버전은 2 로 읽어오지만, 508217 height 을 가진 블록의 버전은 536870912이다. ), 이부분을 좀 고민을 하다 최근 블록의 버전 표시로 통일하는 꼼수를 넣었다.

(블록 버전의 표시가 중간에 좀 바뀐듯 한데, 바뀐 이유는 아직 잘 모르겠다. )

 

508217 블록을 가지고 시작해보자. 

해쉬 값 : 
```
000000000000000000081759445e2a44cb808c2b5e144c41d5d24d8fe7149269
```   
을 구하면 된다.     
<br>

**블록 헤더**

```
 "result": {
        "hash": "000000000000000000081759445e2a44cb808c2b5e144c41d5d24d8fe7149269",
        "confirmations": 225833,
        "strippedsize": 984150,
        "size": 1040139,
        "weight": 3992589,
        "height": 508217,
        "version": 536870912,
        "versionHex": "20000000",
        "merkleroot": "98f0bb94fc154733f22ac54994e9637981900fcee8a0db7d5880b5b79ca3853d",
```

block_hash.py
```

import requests
import hashlib
from binascii import unhexlify, hexlify

def hex_lsb(number):
    try:
        hex_str = hex(number)[2:]
        
        if(len(hex_str)== 1): #버전이 한자리 숫자일 경우에 대한 처리
            hex_str =  "0000000" + hex_str
        
        hex_str_lsb = ''.join([hex_str[i-2:i] for i in range(len(hex_str), 0, -2)])
        
        return hex_str_lsb
        
    except ValueError:
        # 에러 처리!
        print('Conversion failed!')
        return ''
    
def str_lsb(sHash):
    try:       
        str_lsb = ''.join([sHash[i-2:i] for i in range(len(sHash), 0, -2)])
        
        return str_lsb
        
    except ValueError:
        # 에러 처리!
        print('Conversion failed!')
        return ''
        

#url = 'https://blockchain.info/block-height/' + '125552' + '?format=json'
url = 'https://blockchain.info/block-height/' + '508217' + '?format=json'

resp = requests.get(url=url)
data = resp.json()
block = data['blocks'][0]

#읽어온 블록 header 정보를 저장함
sVersion =  block['ver']
shashPrevBlock = block['prev_block']
shashMerkleRoot = block['mrkl_root']
stime = block['time']
sBits = block['bits']
sNonce = block['nonce']


#little endian 형식으로 변환 
cVersion = hex_lsb(sVersion)
ctime = hex_lsb(stime)
cBits = hex_lsb(sBits)
cNonce = hex_lsb(sNonce)

chashPrevBlock = str_lsb(shashPrevBlock)
chashMerkleRoot = str_lsb(shashMerkleRoot)

#위의 정보를 합산함. 순서 중요
header_hex = cVersion + chashPrevBlock + chashMerkleRoot + ctime + cBits + cNonce

# 바이너리 형태로 변환후 두번 SHA256 으로 변형
header_bin = unhexlify(header_hex)
hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()

print(hexlify(hash).decode("utf-8"))

#결과값을 역순으로 가지고 온다.
print(hexlify(hash[::-1]).decode("utf-8"))

```


실행결과 : 

두번째 줄의 값이 위에서 구하고자 한 값 000000000000000000081759445e2a44cb808c2b5e144c41d5d24d8fe7149269 과 일치함을 볼 수 있다. 