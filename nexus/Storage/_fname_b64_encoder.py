import base64
    
def fname_b64_encode(text: str) -> str:
    encoded = base64.urlsafe_b64encode(
        text.encode("utf-8")
    ).decode("utf-8")
    return "b64_" + encoded

def fname_b64_decode(text: str) -> str:
    decoded = base64.urlsafe_b64decode(
        text[4:].encode("utf-8")
    ).decode("utf-8")
    return decoded