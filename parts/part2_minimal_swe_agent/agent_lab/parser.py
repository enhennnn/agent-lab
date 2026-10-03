"""解析模型返回的 message。"""

import json
from dataclasses import dataclass, field


@dataclass
class ParsedToolCall:
    call_id: str
    name: str
    arguments: dict


@dataclass
class ParsedResponse:
    tool_calls: list[ParsedToolCall] = field(default_factory=list)
    final_text: str | None = None
    assistant_message: dict = field(default_factory=dict)


def parse_response(message) -> ParsedResponse:
    """把 OpenAI/DeepSeek 的 message 转成统一结构。"""
    assistant_message = {
        "role": "assistant",
        "content": message.content or "",
    }

    if not message.tool_calls:
        return ParsedResponse(
            tool_calls=[],
            final_text=message.content,
            assistant_message=assistant_message,
        )

    parsed_calls = []
    raw_calls = []

    for call in message.tool_calls:
        try:
            arguments = json.loads(call.function.arguments or "{}")
        except Exception:
            arguments = {}

        parsed_calls.append(
            ParsedToolCall(
                call_id=call.id,
                name=call.function.name,
                arguments=arguments,
            )
        )
        raw_calls.append(
            {
                "id": call.id,
                "type": "function",
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments,
                },
            }
        )

    assistant_message["tool_calls"] = raw_calls
    return ParsedResponse(
        tool_calls=parsed_calls,
        final_text=None,
        assistant_message=assistant_message,
    )