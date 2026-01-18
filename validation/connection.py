import requests

CONNECTION_CODES = [200, 201, 301, 302, 400, 404] #Status codes the model may reasonably encounter during get requests

def verify_connection_codes():
    for code in CONNECTION_CODES:
        #httpbin.org/status/[code] will return corresponding status code during get request. Verify system can obtain each relevant status code.
        r = requests.get(f"https://httpbin.org/status/{code}", allow_redirects = False) #3xx codes (redirects) will actively redirect to the 200 page. Disable redirects during get calls to access these status codes.
        if r.status_code != code:
            raise ConnectionError(f"\033[91mStatus code {code} unreachable. Please check connection.\033[0m")
    print("\033[92mCONNECTION CHECK: PASS - System is able to fetch web content.\033[0m")