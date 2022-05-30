import base64
import os
class Anonymization(object):
    def __init__(self):
        '''
        生成转义 ascii 码映射表
        前 32 个 非常规字符
        37  ==> %
        47  ==> /
        61  ==> =
        92  ==> \
        127 ==> DEL
        '''
        self.key_char = '&'
        self.map = dict()
        special = [idx for idx in range(0, 32)] + [37, 47, 61, 92, 127, ord(self.key_char)]
        for ascii in special:
            val = hex(ascii).replace('0x','')
            # 保证 & 后面是两位数字字符
            self.map[ascii] = self.key_char + (val if 2==len(val) else '0'+val)

    # 加密
    def encrypt(self, filename):
        plaintext = bytes(filename, encoding = "utf8")
        ciphertext = base64.b64encode(plaintext)

        ciphertext = str(ciphertext, encoding = "utf8")
        return self.__encode(ciphertext)

    # 解密
    def decrypt(self, filename):
        ciphertext = self.__decode(filename)
        ciphertext = bytes(ciphertext, encoding = "utf8")
        plaintext = base64.b64decode(ciphertext)

        return str(plaintext, encoding = "utf8")

    # 编码
    def __encode(self, filename):
        ascii = list(bytearray(filename, encoding='utf-8'))
        character = [self.map[value] if value in self.map.keys() else chr(value) for value in ascii]
        return ''.join(character)

    # 解码
    def __decode(self, filename):
        character = []
        position = 0
        while (position < len(filename)):
            if filename[position] != self.key_char:
                character.append(filename[position])
                position = position+1
            else:
                character.append(filename[position:position+3])
                position = position+3
        rev_map = dict(zip(self.map.values(), self.map.keys()))
        character = [chr(rev_map[value]) if value in rev_map.keys() else value for value in character]
        return ''.join(character)
