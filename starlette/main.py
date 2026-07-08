async def read_body(receive) -> bytes:
    body_chunks = []
    while True:
        message = await receive()
        if message.get("type") == "http.request":
            body_chunks.append(message.get("body", "b"))
            if not message.get("more_body", False):
                break
    return b"".join(body_chunks)


async def app(scope, receive, send):
    if scope["type"] != "http":
        return
    
    print("\n--- [DEBUG] Current Scope ---")
    import pprint

    printable_scope = {
        k: (v.decode() if isinstance(v, bytes) else v) for k, v in scope.items()
    }

    printable_scope["headers"] = scope["headers"]
    pprint.pprint(printable_scope)
    print("-----------------------------\n")

    path = scope["path"]
    method = scope["method"]

    if method == "GET" and path == "/":
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"text/plain")],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": b"hello world",
            }
        )

    elif method == "POST" and path == "/echo":
        req_body = await read_body(receive)

        content_type = b"text/plain"
        for k, v in scope["headers"]:
            if k == b"content-type":
                content_type = v
                break
        
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", content_type)],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": req_body,
            }
        )
        