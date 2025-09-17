import base64
import json
import zlib

from pbi_parsers.pq.exprs.array import ArrayExpression
from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.exprs.identifier import IdentifierExpression
from pbi_parsers.pq.exprs.literal_number import LiteralNumberExpression
from pbi_parsers.pq.exprs.literal_string import LiteralStringExpression
from pbi_parsers.pq.tokens import Token


def resolve_binary_decompress(node: FunctionExpression) -> FunctionExpression | LiteralStringExpression:
    assert node.name.name() == "Binary.Decompress"
    text_blob, compression = node.args[0], node.args[1]
    if not isinstance(text_blob, LiteralStringExpression):
        return node
    if not isinstance(compression, IdentifierExpression):
        return node
    if compression.name() == "Compression.Deflate":
        byte_array = bytes.fromhex(text_blob.value.text)
        decompressed = zlib.decompress(byte_array, -zlib.MAX_WBITS)
        new_text = "".join(f"{b:02x}" for b in decompressed)
        return LiteralStringExpression(value=Token.from_str(new_text))

    msg = f"Compression {compression.name()} not implemented"
    raise NotImplementedError(msg)


def resolve_binary_from_text(node: FunctionExpression) -> FunctionExpression | LiteralStringExpression:
    assert node.name.name() == "Binary.FromText"
    text_blob, encoding = node.args[0], node.args[1]
    if not isinstance(text_blob, LiteralStringExpression):
        return node
    if not isinstance(encoding, IdentifierExpression):
        return node
    if encoding.name() == "BinaryEncoding.Base64":
        decoded_bytes = base64.b64decode(text_blob.value.text.strip('"'))
        new_text = "".join(f"{b:02x}" for b in decoded_bytes)
        return LiteralStringExpression(value=Token.from_str(new_text))
    msg = f"Encoding {encoding.name()} not implemented"
    raise NotImplementedError(msg)


def resolve_json_document(node: FunctionExpression) -> FunctionExpression | ArrayExpression:
    assert node.name.name() == "Json.Document"
    text_blob = node.args[0]
    if not isinstance(text_blob, LiteralStringExpression):
        return node
    byte_array = bytes.fromhex(text_blob.value.text)
    json_entity = json.loads(byte_array.decode("utf-8"))
    ret = ArrayExpression(elements=[])
    for row in json_entity:
        row_ret = ArrayExpression(elements=[])
        ret.elements.append(row_ret)
        for e in row:
            if isinstance(e, str):
                row_ret.elements.append(LiteralStringExpression(value=Token.from_str(f'"{e}"')))
            elif isinstance(e, (int, float)):
                row_ret.elements.append(LiteralNumberExpression(value=Token.from_str(str(e))))
    return ret
