import orjson
from typing import Any
from blacksheep import Content, Response


def json(data: Any, status: int = 200) -> Response:
    """
    Returns a response with application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status,
        None,
        Content(
            b"application/json",
            orjson.dumps(data),
        ),
    )


def pretty_json(
    data: Any,
    status: int = 200,
    indent: int = 4,
) -> Response:
    """
    Returns a response with indented application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status,
        None,
        Content(
            b"application/json",
            orjson.dumps(data, option=orjson.OPT_INDENT_2),
        ),
    )
