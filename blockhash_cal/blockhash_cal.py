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
print(hexlify(hash[::-1]).decode("utf-8"))





