import unicodedata

ROMAN_NUMS = {
    1000000: "Ⅿ̄",
    900000: "Ⅽ̄Ⅿ̄",
    500000: "Ⅾ̄",
    400000: "Ⅽ̄Ⅾ̄",
    100000: "Ⅽ̄",
    90000: "Ⅹ̄Ⅽ̄",
    50000: "Ⅼ̄",
    40000: "Ⅹ̄Ⅼ̄",
    10000: "Ⅹ̄",
    9000: "Ⅸ̄",
    8000: "ⅤⅢ̄",
    7000: "ⅤⅡ̄",
    6000: "ⅤⅠ̄",
    5000: "Ⅴ̄",
    4000: "Ⅳ̄",
    1000: "Ⅿ",
    900: "ⅭⅯ",
    500: "Ⅾ",
    400: "ⅭⅮ",
    100: "Ⅽ",
    90: "ⅩⅭ",
    50: "Ⅼ",
    40: "ⅩⅬ",
    10: "Ⅹ",
    9: "Ⅸ",
    8: "Ⅷ",
    7: "Ⅶ",
    6: "Ⅵ",
    5: "Ⅴ",
    4: "Ⅳ",
    3: "Ⅲ",
    2: "Ⅱ",
    1: "Ⅰ",
}
MERGES = {"ⅩⅡ": "Ⅻ", "ⅩⅠ": "Ⅺ", "Ⅹ̄Ⅱ̄": "Ⅻ̄", "Ⅹ̄Ⅰ̄": "Ⅺ̄"}
ROMAN_FRACS = {6: "S", 1: "·"}  # *12之后的
ROMAN_ZERO = "N"

AROMAN_NUMS = {
    "M̄": 1000000,
    "C̄M̄": 900000,
    "D̄": 500000,
    "C̄D̄": 400000,
    "C̄": 100000,
    "X̄C̄": 90000,
    "L̄": 50000,
    "X̄L̄": 40000,
    "X̄": 10000,
    "ĪX̄": 9000,
    "IX̄": 9000,
    "V̄ĪĪĪ": 8000,
    "V̄IIĪ": 8000,
    "VIIĪ": 8000,
    "V̄ĪĪ": 7000,
    "V̄IĪ": 7000,
    "VIĪ": 7000,
    "V̄Ī": 6000,
    "VĪ": 6000,
    "V̄": 5000,
    "ĪV̄": 4000,
    "IV̄": 4000,
    "M": 1000,
    "CM": 900,
    "D": 500,
    "CD": 400,
    "C": 100,
    "XC": 90,
    "L": 50,
    "XL": 40,
    "X": 10,
    "IX": 9,
    "V": 5,
    "IV": 4,
    "III": 3,
    "II": 2,
    "I": 1,
    "N": 0,
    "S": 1 / 2,
    "·": 1 / 12,
}


def an2rn(num: float) -> str:
    if num >= 4_000_000:
        raise ValueError("现代罗马数字不适用于表示四百万及以上的数。")
    if num < 0:
        raise ValueError("罗马数字不能表示负数。")
    if num == 0:
        return ROMAN_ZERO
    inte = int(num)
    deci = int(num * 12 - inte * 12)
    remain = num - inte - deci / 12
    ret = []
    for val, char in ROMAN_NUMS.items():
        while True:
            if inte >= val:
                ret.append(char)
                inte -= val
            else:
                break
    for val, char in ROMAN_FRACS.items():
        while deci >= val:
            ret.append(char)
            deci -= val
    retstr = "".join(ret)
    for k, v in MERGES.items():
        retstr = retstr.replace(k, v)
    return retstr + "N" if remain else retstr  # 尾随0表示忽略了不足1/12的部分


def an2rnA(num: float) -> str:
    return unicodedata.normalize("NFKC", an2rn(num))


def rn2an(rn: str) -> float | int:
    rn = unicodedata.normalize("NFKD", rn).upper()
    ret = 0
    for char, val in AROMAN_NUMS.items():
        while rn.startswith(char):
            ret += val
            rn = rn[len(char) :]
    if rn:
        raise ValueError(f"无法解析罗马数字 {rn}")
    return ret if ret != int(ret) else int(ret)
