"""All constants
所有常量
"""

CHINESE_DIGITS: str = "零一二三四五六七八九"
"""
Normal simplified/traditional Chinese charactors for 0123456789.

小写中文数字, 简体繁体一致
"""

"""Tranditional Capitalized Chinese charactors for 0123456789.
繁体大写中文数字
"""
CAPITAL_CHINESE_DIGITS_TRADITIONAL: str = "零壹貳參肆伍陸柒捌玖"

"""Simplified Capitalized Chinese charactors for 0123456789.
簡体大写中文数字
""" 
CAPITAL_CHINESE_DIGITS_SIMPLIFIED: str = "零壹贰叁肆伍陆柒捌玖"

SMALLER_CHINESE_NUMBERING_UNITS_SIMPLIFIED: str = "十百千万"
"""Simplified Chinese charactors for $10^1$, $10^2$, $10^3$, $10^4$.
Not like other numbering systems,
a Chinese number is grouped by four decimal digits.

简体小写小额数字单位
"""

SMALLER_CHINESE_NUMBERING_UNITS_TRADITIONAL: str = "拾佰仟萬"
"""Traditional Chinese charactors for $10^1$, $10^2$, $10^3$, $10^4$.
Also used as capitalized units for simplified Chinese.
Not like other numbering systems,
a Chinese number is grouped by four decimal digits.

繁体大写小额数字单位
"""

LARGER_CHINESE_NUMBERING_UNITS_SIMPLIFIED: str = "亿兆京垓秭穰沟涧正载"
r"""
Simplified Chinese charactors for larger units.

简体小写大额数字单位

$i \in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]$:

| numbering_type | value                |
|----------------|----------------------|
| `low`          | $10^{8 + i}$       |
| `mid`          | $10^{8 + i*4}$     |
| `high`         | $10^{8 + 2^{i+3}}$ |

|type|亿|兆|京|垓|秭|穰|沟|涧|正|载|
|---|---|---|---|---|---|---|---|---|---|---|
|`low` | $10^{8}$|$10^{9}$|$10^{10}$|$10^{11}$|$10^{12}$|$10^{13}$|$10^{14}$|$10^{15}$|$10^{16}$|$10^{17}$|
|`mid` | $10^{8}$|$10^{12}$|$10^{16}$|$10^{20}$|$10^{24}$|$10^{28}$|$10^{32}$|$10^{36}$|$10^{40}$|$10^{44}$|
|`high` | $10^{8}$|$10^{16}$|$10^{32}$|$10^{64}$|$10^{128}$|$10^{256}$|$10^{512}$|$10^{1024}$|$10^{2048}$|$10^{4096}$|

"""

LARGER_CHINESE_NUMBERING_UNITS_TRADITIONAL: str = "億兆京垓秭穰溝澗正載"
r"""
Traditional Chinese charactors for larger units.
Also used as capitalized units for simplified Chinese.

繁体/简体大写大额数字单位

$i \in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]$:

| numbering_type | value                |
|----------------|----------------------|
| `low`          | $10^{8 + i}$       |
| `mid`          | $10^{8 + i*4}$     |
| `high`         | $10^{8 + 2^{i+3}}$ |

|type|亿|兆|京|垓|秭|穰|沟|涧|正|载|
|---|---|---|---|---|---|---|---|---|---|---|
|`low` | $10^{8}$|$10^{9}$|$10^{10}$|$10^{11}$|$10^{12}$|$10^{13}$|$10^{14}$|$10^{15}$|$10^{16}$|$10^{17}$|
|`mid` | $10^{8}$|$10^{12}$|$10^{16}$|$10^{20}$|$10^{24}$|$10^{28}$|$10^{32}$|$10^{36}$|$10^{40}$|$10^{44}$|
|`high` | $10^{8}$|$10^{16}$|$10^{32}$|$10^{64}$|$10^{128}$|$10^{256}$|$10^{512}$|$10^{1024}$|$10^{2048}$|$10^{4096}$|

"""

ZERO_ALT: str = "〇〇"
"""
Another version of zero in simplified and traditional Chinese
简体和繁体另一种零的写法
"""

TWO_ALT: str = "两兩"
"""
Another version of two in simplified and traditional Chinese
简体和繁体另一种二的写法
"""

POSITIVE: str = "正正"
"""
Positive in simplified and traditional Chinese
简体和繁体正
"""

NEGATIVE: str = "负負"
"""
Negative in simplified and traditional Chinese
简体和繁体负
"""

POINT: str = "点點"
"""
Point in simplified and traditional Chinese
简体和繁体点
"""

NUMBERING_TYPES: tuple[str, str, str] = ("low", "mid", "high")
"""
Chinese numbering types:
大额进位方法

|type|亿|兆|京|垓|秭|穰|沟|涧|正|载|
|---|---|---|---|---|---|---|---|---|---|---|
|`'low'`|$10^{8}$|$10^{9}$|$10^{10}$|$10^{11}$|$10^{12}$|$10^{13}$|$10^{14}$|$10^{15}$|$10^{16}$|$10^{17}$|
|`'mid'`|$10^{8}$|$10^{12}$|$10^{16}$|$10^{20}$|$10^{24}$|$10^{28}$|$10^{32}$|$10^{36}$|$10^{40}$|$10^{44}$|
|`'high'`|$10^{8}$|$10^{16}$|$10^{32}$|$10^{64}$|$10^{128}$|$10^{256}$|$10^{512}$|$10^{1024}$|$10^{2048}$|$10^{4096}$|
"""
