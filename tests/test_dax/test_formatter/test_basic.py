import pytest

from pbi_parsers.dax.main import format_expression


@pytest.mark.parametrize(
    ("input_str", "output"),
    [
        (
            "12.3e10",
            "12.3e10",
        ),
        (
            "func.name(arg1 + 1 + 2  + 3, func(), func(10000000000000), arg2)",
            """
func.name(
    arg1 + 1 + 2 + 3,
    func(),
    func(10000000000000),
    arg2
)""".lstrip(),
        ),
        (
            "1+  2 ",
            "1 + 2",
        ),
    ],
)
def test_add_sub(input_str: str, output: str) -> None:
    formatted_str = format_expression(input_str)
    assert formatted_str == output, f"Expected: {output}, but got: {formatted_str}"
