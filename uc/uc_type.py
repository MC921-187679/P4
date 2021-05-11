from __future__ import annotations
from typing import Optional, Sequence, Set, Tuple


class uCType:
    """
    Class that represents a type in the uC language.  Basic
    Types are declared as singleton instances of this type.
    """

    __slots__ = "_typename", "binary_ops", "unary_ops", "rel_ops", "assign_ops"

    def __init__(
        self,
        name: Optional[str],
        binary_ops: Set[str] = set(),
        unary_ops: Set[str] = set(),
        rel_ops: Set[str] = set(),
        assign_ops: Set[str] = set(),
    ):
        """
        You must implement yourself and figure out what to store.
        """
        self._typename = name
        self.unary_ops = frozenset(unary_ops)
        self.binary_ops = frozenset(binary_ops)
        self.rel_ops = frozenset(rel_ops)
        self.assign_ops = frozenset(assign_ops)

    def __eq__(self, other: uCType) -> bool:
        """Primary types are only equal to themselves."""
        return self is other

    def typename(self) -> str:
        """The name of the uCType."""
        return self._typename or "<unnamed>"

    def __str__(self) -> str:
        """Standard type formatting."""
        return f"type({self.typename()})"

    def __format__(self, format_spec: str) -> str:
        """Special 't' format for types that only show the typename."""
        if format_spec == "t":
            return self.typename()

        return super().__format__(format_spec)


# # # # # # # # #
# Primary Types #

IntType = uCType(
    "int",
    unary_ops={"-", "+"},
    binary_ops={"+", "-", "*", "/", "%"},
    rel_ops={"==", "!=", "<", ">", "<=", ">="},
    assign_ops={"="},
)

CharType = uCType(
    "char",
    rel_ops={"==", "!=", "&&", "||"},
    assign_ops={"="},
)

BoolType = uCType(
    "bool",
    rel_ops={"==", "!=", "&&", "||"},
    assign_ops={"="},
)

VoidType = uCType("void")  # no valid operation


# # # # # # # # # #
# Compound Types  #


class ArrayType(uCType):
    __slots__ = "type", "size"

    def __init__(self, element_type: uCType, size: Optional[int] = None):
        """
        type: Any of the uCTypes can be used as the array's type. This
              means that there's support for nested types, like matrices.
        size: Integer with the length of the array.
        """
        super().__init__(None, unary_ops={"*", "&"}, rel_ops={"==", "!="})
        self.type = element_type
        self.size = size

    def __eq__(self, other: uCType) -> bool:
        return isinstance(other, ArrayType) and self.type == other.type and self.size == other.size

    def typename(self) -> str:
        return f"{self.type:t}[{self.size or ''}]"


class FunctionType(uCType):
    __slots__ = "function_name", "rettype", "params"

    def __init__(self, name: str, return_type: uCType, params: Sequence[Tuple[str, uCType]] = ()):
        """
        name: Function definition name.
        return_type: Any uCType can be used here.
        params: Sequence of 'name, type' for each of the function parameters.
        """
        super().__init__()  # only valid operation is call
        self.function_name = name
        self.rettype = return_type
        self.params = tuple(params)

    @property
    def param_types(self) -> Tuple[uCType, ...]:
        return tuple(t for _, t in self.params)

    def __eq__(self, other: uCType) -> bool:
        return (
            isinstance(other, FunctionType)
            and self.rettype == other.rettype
            and self.param_types == other.param_types
        )

    def typename(self, *, show_names: bool = False) -> str:
        if show_names:
            params = ", ".join(f"{n}: {t:t}" for n, t in self.params)
            return f"{self.rettype} {self.typename}({params})"
        else:
            # no space between parameters
            params = ",".join(f"{t:t}" for t in self.param_types)
            return f"{self.rettype}({params})"

    def __format__(self, format_spec: str) -> str:
        """Special 'tn' format that show parameter and function names."""
        if format_spec == "tn":
            return self.typename(show_names=True)

        return super().__format__(format_spec)
