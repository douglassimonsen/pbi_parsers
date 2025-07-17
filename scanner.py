from .token import Token


class Scanner:
    source: str
    start_position: int
    current_position: int
    tokens: list[Token]

    def match(self, char: str) -> bool:
        pass

    def peek(self) -> str | None:
        return (
            self.source[self.current_position]
            if self.current_position < len(self.source)
            else None
        )
    
    def scan(self) -> None:
        while not self.at_end():
            

    def at_end(self) -> bool:
        return self.current_position >= len(self.source)
