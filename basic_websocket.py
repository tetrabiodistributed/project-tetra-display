import websocket


def ws_connect_retry(uri):
    for _ in range(10):
        try:
            ws = websocket.create_connection(uri)
            return ws
        except Exception as e:
            if not isinstance(e, KeyboardInterrupt):
                time.sleep(0.1)
            else:
                raise
    raise Exception("Could not connect")
