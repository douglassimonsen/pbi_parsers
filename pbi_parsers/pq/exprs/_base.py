from collections.abc import Callable
from typing import TYPE_CHECKING, TypeVar

from pbi_parsers.pq.tokens import TokenType

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser
T = TypeVar("T", bound="Expression")


class Expression:
    def pprint(self) -> str:
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    @classmethod
    def match(cls, parser: "Parser") -> "Expression | None":
        """Attempt to match the current tokens to this expression type.

        Returns an instance of the expression if matched, otherwise None.
        """
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    @staticmethod
    def match_tokens(parser: "Parser", match_tokens: list[TokenType]) -> bool:
        return all(parser.peek(i).tok_type == token_type for i, token_type in enumerate(match_tokens))

    def __repr__(self) -> str:
        return self.pprint()

    def children(self) -> list["Expression"]:
        """Returns a list of child expressions."""
        msg = f"This method should be implemented by subclasses. This subclass is: {type(self)}."
        raise NotImplementedError(msg)

    def find(self, cls_type: type[T] | tuple[type[T], ...], attributes: Callable[[T], bool] | None = None) -> T:
        attributes = attributes or (lambda _x: True)

        if isinstance(self, cls_type) and attributes(self):
            return self

        for child in self.children():
            try:
                return child.find(cls_type, attributes)
            except ValueError:
                continue

        msg = f"Matching {cls_type} not found in expression tree."
        raise ValueError(msg)

    def find_all(
        self,
        cls_type: type[T] | tuple[type[T], ...],
        attributes: Callable[[T], bool] | None = None,
    ) -> list[T]:
        attributes = attributes or (lambda _x: True)
        results: list[T] = []

        if isinstance(self, cls_type) and attributes(self):
            results.append(self)

        for child in self.children():
            results.extend(child.find_all(cls_type, attributes))

        return results
