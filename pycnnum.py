""" Chinese number <=> int/float conversion methods """

from __future__ import annotations

from typing import Callable, Optional

from ._version import __version__
from .constants import *  # pylint: disable=wildcard-import


class ChineseChar:
    """Base Chinese char class.

    Each object has simplified and traditional strings.
    When converted to string, it will shows the simplified string or traditional string or space `' '`.

    Example:

    >>> negative = ChineseChar(simplified="负", traditional="負")
    >>> negative.simplified
    '负'
    >>> negative.traditional
    '負'
    >>> negative.__str__()
    '负'
    >>> negative.__repr__()
    '负'
    """

    simplified: str
    """Simplified Chinese char"""

    traditional: str
    """Traditional Chinese char"""

    def __init__(self, simplified: str, traditional: str) -> None:
        """
        Constructor

        Args:
            simplified (str): Simplified Chinese char
            traditional (str): Traditional Chinese char
        """
        self.simplified = simplified
        self.traditional = traditional

    def __str__(self) -> str:
        return self.simplified or self.traditional or " "

    def __repr__(self) -> str:
        return self.__str__()


class ChineseNumberUnit(ChineseChar):
    """Chinese number unit class

    Each of it is an `ChineseChar` with additional capitalize type strings.

    Example:

    >>> wan = ChineseNumberUnit(4, "万", "萬", "萬", "萬")
    >>> wan
    10^4
    """

    def __init__(
        self,
        power: int,
        simplified: str,
        traditional: str,
        capital_simplified: str,
        capital_traditional: str,
    ) -> None:
        """
        Constructor

        Args:
            power (int): The power of this unit, e.g. `power` = 4 for `'万'` ( $10^4$ )
            simplified (str): Charactor in simplified Chinese
            traditional (str): Charactor in traditional Chinese
            capital_simplified (str): Capitalized charactor in simplified Chinese
            capital_traditional (str): Capitalized charactor in traditional Chinese
        """
        super().__init__(simplified, traditional)
        self.power = power
        self.capital_simplified = capital_simplified
        self.capital_traditional = capital_traditional

    def __str__(self) -> str:
        return f"10^{self.power}"

    @classmethod
    def create(
        cls,
        index: int,
        chars: str,
        numbering_type: str = NUMBERING_TYPES[1],
        small_unit: bool = False,
    ) -> ChineseNumberUnit:
        """Create one unit charactor based on index in units in

        - `pycnnum.constants.SMALLER_CHINESE_NUMBERING_UNITS_SIMPLIFIED`
        - `pycnnum.constants.SMALLER_CHINESE_NUMBERING_UNITS_TRADITIONAL`
        - `pycnnum.constants.LARGER_CHINESE_NUMBERING_UNITS_SIMPLIFIED`
        - `pycnnum.constants.LARGER_CHINESE_NUMBERING_UNITS_TRADITIONAL`

        Args:
            index (int): Zero based index in larger units.
            chars (str): simplified and traditional charactors.
            numbering_type (str, optional): Numbering type. Defaults to `pycnnum.constants.NUMBERING_TYPES[1]`.
            small_unit (bool, optional): the unit is small unit (less than $10^5$ ). Defaults to False.

        Raises:
            ValueError: Raised when
                - invalid `index` is provided
                - invalid `numbering_type` is provided

        Returns:
            pycnnum.pycnnum.ChineseNumberUnit: Created unit object

        Example:

        >>> wan = ChineseNumberUnit.create(3, "万萬萬萬", small_unit=True)
        >>> wan
        10^4
        >>> wan = ChineseNumberUnit.create(9, "万萬萬萬", small_unit=True)
        Traceback (most recent call last):
        ValueError: 9 should be from 0 to 4.
        >>> wan = ChineseNumberUnit.create(12, "万萬萬萬", small_unit=False)
        Traceback (most recent call last):
        ValueError: 12 should be from 0 to 10.
        >>> wan = ChineseNumberUnit.create(3, "万萬萬萬", numbering_type="错")
        Traceback (most recent call last):
        ValueError: Numbering type should be in ('low', 'mid', 'high') but 错 is provided.
        """
        if small_unit:
            if index > len(SMALLER_CHINESE_NUMBERING_UNITS_SIMPLIFIED):
                raise ValueError(f"{index} should be from 0 to {len(SMALLER_CHINESE_NUMBERING_UNITS_SIMPLIFIED)}.")

            return ChineseNumberUnit(
                power=index + 1,
                simplified=chars[0],
                traditional=chars[1],
                capital_simplified=chars[1],
                capital_traditional=chars[1],
            )

        if index > len(LARGER_CHINESE_NUMBERING_UNITS_SIMPLIFIED):
            raise ValueError(f"{index} should be from 0 to {len(LARGER_CHINESE_NUMBERING_UNITS_SIMPLIFIED)}.")

        if numbering_type == NUMBERING_TYPES[0]:
            return ChineseNumberUnit(
                power=index + 8,
                simplified=chars[0],
                traditional=chars[1],
                capital_simplified=chars[0],
                capital_traditional=chars[1],
            )

        if numbering_type == NUMBERING_TYPES[1]:
            return ChineseNumberUnit(
                power=(index + 2) * 4,
                simplified=chars[0],
                traditional=chars[1],
                capital_simplified=chars[0],
                capital_traditional=chars[1],
            )

        if numbering_type == NUMBERING_TYPES[2]:
            return ChineseNumberUnit(
                power=pow(2, index + 3),
                simplified=chars[0],
                traditional=chars[1],
                capital_simplified=chars[0],
                capital_traditional=chars[1],
            )

        raise ValueError(f"Numbering type should be in {NUMBERING_TYPES} but {numbering_type} is provided.")


class ChineseNumberDigit(ChineseChar):
    """Chinese number digit class

    Example:

    >>> san = ChineseNumberDigit(3, *"三叁叁叁",)
    >>> san
    3
    """

    def __init__(
        self,
        int_value: int,
        simplified: str,
        traditional: str,
        capital_simplified: str,
        capital_traditional: str,
        alt_s: str = "",
        alt_t: str = "",
    ):
        """
        Constructor

        Args:
            int_value (int): int value of the digit, 0 to 9.
            simplified (str): Charactor in simplified Chinese.
            traditional (str): Charactor in traditional Chinese.
            capital_simplified (str): Capitalized charactor in simplified Chinese.
            capital_traditional (str): Capitalized charactor in traditional Chinese.
            alt_s (str, optional): Alternative simplified charactor. Defaults to "".
            alt_t (str, optional): Alternative traditional charactor. Defaults to "".
        """
        super().__init__(simplified, traditional)
        self.int_value = int_value
        self.capital_simplified = capital_simplified
        self.capital_traditional = capital_traditional
        self.alt_s = alt_s
        self.alt_t = alt_t

    def __str__(self):
        return str(self.int_value)


class ChineseMath(ChineseChar):
    """
    Chinese math operators

    Example:

    >>> positive = ChineseMath(*'正正+', lambda x: +x)
    >>> positive.symbol
    '+'
    """

    def __init__(
        self,
        simplified: str,
        traditional: str,
        symbol: str,
        expression: Optional[
            Callable[[int | float], int | float] | Callable[[int | float, int | float], int | float]
        ] = None,
    ):
        """
        Constructor

        Args:
            simplified (str): Simplified charactor.
            traditional (str): Traditional charactor.
            symbol (str): Mathematical symbol, e.g. '+'.
            expression (Callable[[int | float], int], optional): Callable for this math operator. Defaults to `None`.
        """
        super().__init__(simplified, traditional)
        self.symbol = symbol
        self.expression = expression
        self.capital_simplified = simplified
        self.capital_traditional = traditional


class MathSymbols:
    """Math symbols used in Chinese for both traditional and simplified Chinese

    - positive = ["正", "正"]
    - negative = ["负", "負"]
    - point = ["点", "點"]

    Used in `pycnnum.pycnnum.NumberingSystem`.
    """

    def __init__(self, positive: ChineseMath, negative: ChineseMath, point: ChineseMath):
        """
        Constructor

        Args:
            positive (ChineseMath): Positive
            negative (ChineseMath): Negative
            point (ChineseMath): Decimal point
        """
        self.positive = positive
        self.negative = negative
        self.point = point


class NumberingSystem:  # pylint: disable=too-few-public-methods
    """Numbering system class"""

    def __init__(self, numbering_type: str = NUMBERING_TYPES[1]) -> None:
        """
        Constructor

        Args:
            numbering_type (str, optional): Numbering type. Defaults to `pycnnum.constants.NUMBERING_TYPES[1]`.

        Example:

        >>> low = NumberingSystem("low")
        >>> low.digits
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> low.units
        [10^1, 10^2, 10^3, 10^4, 10^8, 10^9, 10^10, 10^11, 10^12, 10^13, 10^14, 10^15, 10^16, 10^17]
        >>> mid = NumberingSystem('mid')
        >>> mid.units
        [10^1, 10^2, 10^3, 10^4, 10^8, 10^12, 10^16, 10^20, 10^24, 10^28, 10^32, 10^36, 10^40, 10^44]
        >>> high = NumberingSystem('high')
        >>> high.units
        [10^1, 10^2, 10^3, 10^4, 10^8, 10^16, 10^32, 10^64, 10^128, 10^256, 10^512, 10^1024, 10^2048, 10^4096]
        """

        # region units of '亿' and larger
        all_larger_units = zip(
            LARGER_CHINESE_NUMBERING_UNITS_SIMPLIFIED,
            LARGER_CHINESE_NUMBERING_UNITS_TRADITIONAL,
        )
        larger_units = [
            ChineseNumberUnit.create(
                index=index,
                chars=simplified + traditional,
                numbering_type=numbering_type,
                small_unit=False,
            )
            for index, (simplified, traditional) in enumerate(all_larger_units)
        ]
        # endregion

        # region units of '十, 百, 千, 万'
        all_smaller_units = zip(
            SMALLER_CHINESE_NUMBERING_UNITS_SIMPLIFIED,
            SMALLER_CHINESE_NUMBERING_UNITS_TRADITIONAL,
        )
        smaller_units = [
            ChineseNumberUnit.create(
                index=index,
                chars=simplified + traditional,
                numbering_type=numbering_type,
                small_unit=True,
            )
            for index, (simplified, traditional) in enumerate(all_smaller_units)
        ]
        # endregion

        # region digits
        chinese_digits = zip(
            CHINESE_DIGITS,
            CHINESE_DIGITS,
            CAPITAL_CHINESE_DIGITS_SIMPLIFIED,
            CAPITAL_CHINESE_DIGITS_TRADITIONAL
        )
        digits = [ChineseNumberDigit(i, *v) for i, v in enumerate(chinese_digits)]
        digits[0].alt_s, digits[0].alt_t = ZERO_ALT[0], ZERO_ALT[1]
        digits[2].alt_s, digits[2].alt_t = TWO_ALT[0], TWO_ALT[1]
        # endregion

        # region math operators
        positive_cn = ChineseMath(
            simplified=POSITIVE[0],
            traditional=POSITIVE[1],
            symbol="+",
            expression=lambda x: x,
        )
        negative_cn = ChineseMath(
            simplified=NEGATIVE[0],
            traditional=NEGATIVE[1],
            symbol="-",
            expression=lambda x: -x,
        )
        point_cn = ChineseMath(
            simplified=POINT[0],
            traditional=POINT[1],
            symbol=".",
            expression=lambda integer, decimal: float(str(integer) + "." + str(decimal)),
        )
        # endregion

        self.units = smaller_units + larger_units
        self.digits = digits
        self.math = MathSymbols(positive_cn, negative_cn, point_cn)


from typing import Union

SymbolType = Union[ChineseNumberUnit , ChineseNumberDigit , ChineseMath]
# python 3.10
# SymbolType = ChineseNumberUnit | ChineseNumberDigit | ChineseMath
"""Type hint for symbols: unit, digit and math
"""


def get_symbol(char: str, system: NumberingSystem) -> SymbolType:
    """Get symbol based on charactor

    Args:
        char (str): One charactor
        system (NumberingSystem): Numbering system

    Raises:
        ValueError: a charactor is not in the numbering system, e.g. '你' is not a number nor a unit

    Returns:
        SymbolType: unit, digit or math operator
    """
    for u in system.units:
        if char in [
            u.traditional,
            u.simplified,
            u.capital_simplified,
            u.capital_traditional,
        ]:
            return u
    for d in system.digits:
        if char in [
            d.traditional,
            d.simplified,
            d.capital_simplified,
            d.capital_traditional,
            d.alt_s,
            d.alt_t,
        ]:
            return d
    for m in system.math.__dict__.values():
        if char in [m.traditional, m.simplified]:
            return m
    raise ValueError(f"{char} is not in system.")


def string2symbols(chinese_string: str, system: NumberingSystem) -> tuple[list[SymbolType], list[SymbolType]]:
    """String to symbols

    Args:
        chinese_string (str): Chinese number
        system (NumberingSystem): Numbering system

    Returns:
        tuple[list[SymbolType], list[SymbolType]]: Integer symbols, decimal symbols
    """
    int_string, dec_string = chinese_string, ""
    for p in [system.math.point.simplified, system.math.point.traditional]:
        if p not in chinese_string:
            continue
        int_string, dec_string = chinese_string.split(p)
        break
    integer_value = [get_symbol(c, system) for c in int_string]
    decimal_value = [get_symbol(c, system) for c in dec_string]
    return integer_value, decimal_value


# pylint: disable-next=too-many-branches
def refine_symbols(integer_symbols: list[SymbolType], system: NumberingSystem) -> list[SymbolType]:
    """Refine symbols

    Example:

    - `一百八` to `一百八十`
    - `一亿一千三百万` to `一亿 一千万 三百万`
    - `一万四` to `一万四千`
    - `两千万` to `两 10^7`

    Args:
        integer_symbols (list[SymbolType]): Raw integer symbols
        system (NumberingSystem): Numbering system

    Returns:
        list[SymbolType]: Refined symbols

    """
    # First symbol is unit, e.g. "十五"
    first_is_unit = isinstance(integer_symbols[0], ChineseNumberUnit) and integer_symbols[0].power == 1
    if first_is_unit:
        integer_symbols = [system.digits[1]] + integer_symbols  # type: ignore

    # Last symbol is digit and the second last symbol is unit, e.g. "一百一"
    if len(integer_symbols) > 2:
        if not isinstance(integer_symbols[-1], ChineseNumberDigit):
            pass
        elif not isinstance(integer_symbols[-2], ChineseNumberUnit):
            pass
        elif integer_symbols[-2].power < 2:  # do not add unit for ten, e.g. '十五'
            pass
        else:
            integer_symbols += [ChineseNumberUnit(integer_symbols[-2].power - 1, "", "", "", "")]

    result: list[SymbolType] = []
    unit_count = 0
    for s in integer_symbols:
        if isinstance(s, ChineseNumberDigit):
            result.append(s)
            unit_count = 0
            continue

        if not isinstance(s, ChineseNumberUnit):
            continue

        current_unit = ChineseNumberUnit(s.power, "", "", "", "")
        unit_count += 1

        # store the first met unit
        if unit_count == 1:
            result.append(current_unit)
            continue

        # if there are more than one units, e.g. "两千万"
        if unit_count > 1:
            for i in range(len(result)):
                if not isinstance(result[-i - 1], ChineseNumberUnit):
                    continue
                if result[-i - 1].power < current_unit.power:  # type: ignore
                    result[-i - 1] = ChineseNumberUnit(
                        result[-i - 1].power + current_unit.power, "", "", "", ""  # type: ignore
                    )
    return result


def compute_value(integer_symbols: list[SymbolType]) -> int:
    """Compute the value from symbol

    When current unit is larger than previous unit,
    current unit * all previous units will be used as all previous units.
    e.g. '两千万' = 2000 * 10000 not 2000 + 10000

    Args:
        integer_symbols (list[SymbolType]): Symbols, without point

    Returns:
        int: value
    """
    value = [0]
    last_power = 0
    for s in integer_symbols:
        if isinstance(s, ChineseNumberDigit):
            value[-1] = s.int_value
        elif isinstance(s, ChineseNumberUnit):
            value[-1] *= pow(10, s.power)
            if s.power > last_power:
                value[:-1] = list(map(lambda v, sym=s: v * pow(10, sym.power), value[:-1]))  # type: ignore
                last_power = s.power
            value.append(0)
    return sum(value)


def cn2num(chinese_string: str, numbering_type: str = NUMBERING_TYPES[1]) -> int | float:
    """Convert Chinese number to `int` or `float` value。

    Args:
        chinese_string (str): Chinese number
        numbering_type (str, optional): numbering type. Defaults to `pycnnum.pycnnum.NUMBERING_TYPES[1]`.

    Raises:
        ValueError: Raised when
            - a charactor is not in the numbering system, e.g. '你' is not a number nor a unit

    Returns:
        int | float: `int` or `float` value

    Example:

    >>> cn2num("一百八")
    180
    >>> cn2num("十五")
    15
    >>> cn2num("负十五")
    -15
    >>> cn2num("一百八十")
    180
    >>> cn2num("一百八点五六七")
    180.567
    >>> cn2num("两千万一百八十")
    20000180
    >>> cn2num("*两千万一百八十")
    Traceback (most recent call last):
    ValueError: * is not in system.
    """
    system = NumberingSystem(numbering_type)

    int_part, dec_part = string2symbols(chinese_string, system)
    sign = ChineseMath(*"正正+")
    if not int_part:
        int_part = [system.digits[0]]
    if isinstance(int_part[0], ChineseMath):
        sign = int_part[0]
        int_part = int_part[1:]
    int_part = refine_symbols(int_part, system)
    int_value = compute_value(int_part)
    if sign.symbol == "-":
        int_value = -int_value
    # skip unit in decimal value
    dec_str = "".join([str(d.int_value) for d in dec_part if isinstance(d, ChineseNumberDigit)])

    if dec_part:
        return float(f"{int_value}.{dec_str}")
    return int_value


def get_value(value_string: str, numbering_type: str = NUMBERING_TYPES[1]) -> list[SymbolType]:
    """Recursively get values of the number

    Args:
        value_string (str): Value string, e.g. "0.1", "34"
        numbering_type (str, optional): numbering type. Defaults to `pycnnum.pycnnum.NUMBERING_TYPES[1]`.

    Returns:
        list[SymbolType]: list of values
    """
    system = NumberingSystem(numbering_type)

    if value_string == "0":
        return [system.digits[0]]

    striped_string = value_string.lstrip("0")

    # record nothing if all zeros
    if not striped_string:
        return [system.digits[0]]

    # record one digits
    if len(striped_string) == 1:
        if len(value_string) != len(striped_string):
            all_len = len(value_string) - len(striped_string)
            return [system.digits[0] for _ in range(all_len)] + [system.digits[int(striped_string)]]  # type: ignore
        return [system.digits[int(striped_string)]]

    # recursively record multiple digits
    result_unit = next(u for u in reversed(system.units) if u.power < len(striped_string))
    result_string = value_string[: -result_unit.power]
    return (
        get_value(result_string)
        + [result_unit]
        + get_value(striped_string[-result_unit.power :])
    )


def num2cn(
    num: int | float | str,
    numbering_type: str = NUMBERING_TYPES[1],
    capitalize: bool = False,
    traditional: bool = False,
    alt_zero: bool = False,
    alt_two: bool = False
) -> str:
    """Integer or float value to Chinese string

    Args:
        num (int | float | str): `int`, `float` or `str` value
        numbering_type (str, optional): Numbering type. Defaults to `NUMBERING_TYPES[1]`.
        capitalize (bool, optional): Capitalized numbers. Defaults to `False`.
        traditional (bool, optional): Traditional Chinese. Defaults to `False`.
        alt_zero (bool, optional): Use alternative form of zero. Defaults to `False`.
        alt_two (bool, optional): Use alternative form of two. Defaults to `False`.
        keep_zeros (bool, optional): Keep Chinese zeros in `num`. Defaults to `True`.

    Example:

    >>> num2cn('023232.005184132423423423300', numbering_type="high", alt_two=True, capitalize=False, traditional=True)
    '兩萬三仟兩佰三拾二點零零五一八四一三二四二三四二三四二三三'
    >>> num2cn('023232.005184132423423423300', numbering_type="high", alt_two=False, capitalize=False, traditional=True)
    '二萬三仟二佰三拾二點零零五一八四一三二四二三四二三四二三三'
    >>> num2cn(111180000)
    '一亿一千一百一十八万'
    >>> num2cn(1821010)
    '一百八十二万一千零一十'
    >>> num2cn(182.1)
    '一百八十二点一'
    >>> num2cn('3.4')
    '三点四'
    >>> num2cn(16)
    '十六'
    >>> num2cn(10600)
    '一万零六百'
    >>> num2cn(110)
    '一百一'
    >>> num2cn(1600)
    '一千六'

    """
    system = NumberingSystem(numbering_type)

    num_str = str(num)
    int_string = num_str
    dec_string = ""

    if "." in num_str:
        int_string, dec_string = num_str.split(".", 1)
        dec_string = dec_string.rstrip("0")

    result_symbols = get_value(int_string)
    # Remove last 0 for number larger than 10
    if (len(result_symbols) > 1) and (getattr(result_symbols[-1], "int_value", None) == 0):
        result_symbols = result_symbols[:-1]

    # Remove leading 0 for non-zero numbers
    if (len(result_symbols) > 1) and (getattr(result_symbols[0], "int_value", None) == 0):
        result_symbols = result_symbols[1:]

    dec_symbols = [system.digits[int(c)] for c in dec_string]

    if "." in num_str:
        result_symbols += [system.math.point] + dec_symbols  # type: ignore

    if alt_two:
        liang = ChineseNumberDigit(
            2,
            system.digits[2].alt_s,
            system.digits[2].alt_t,
            system.digits[2].capital_simplified,
            system.digits[2].capital_traditional,
        )
        for i, v in enumerate(result_symbols):
            if not isinstance(v, ChineseNumberDigit):
                continue
            if v.int_value != 2:
                continue
            next_symbol = result_symbols[i + 1] if i < len(result_symbols) - 1 else None
            if not isinstance(next_symbol, ChineseNumberUnit):
                continue
            if next_symbol.power > 1:
                result_symbols[i] = liang

    # if capitalize is True, '两' will not be used and `alt_two` has no impact on output
    if traditional:
        attr_name = "traditional"
    else:
        attr_name = "simplified"

    if capitalize:
        attr_name = "capital_" + attr_name

    # remove leading '一' for '十', e.g. 一十六 to 十六
    if (getattr(result_symbols[0], "int_value", None) == 1) and (getattr(result_symbols[1], "power", None) == 1):
        result_symbols = result_symbols[1:]

    # remove trailing units, 1600 -> 一千六, 10600 -> 一萬零六百, 101600 -> 十萬一千六
    if len(result_symbols) > 3 and isinstance(result_symbols[-1], ChineseNumberUnit):
        if getattr(result_symbols[::-1][2], "power", None) == (result_symbols[-1].power + 1):
            result_symbols = result_symbols[:-1]

    result = "".join([getattr(s, attr_name) for s in result_symbols])

    for p in POINT:
        if not result.startswith(p):
            continue
        result = CHINESE_DIGITS[0] + result
        break

    if alt_zero:
        result = result.replace(getattr(system.digits[0], attr_name), system.digits[0].alt_s)

    return result
