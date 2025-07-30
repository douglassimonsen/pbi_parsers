from .exprs import Expression


class Formatter:
    expression: Expression

    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    def format(self) -> str:
        # Implement the formatting logic here
        msg = "Formatter.format method is not implemented."
        raise NotImplementedError(msg)
