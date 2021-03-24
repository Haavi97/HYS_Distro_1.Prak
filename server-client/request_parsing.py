def parse_request(data):
    data = data.split('\r\n')
    processed = {}
    processed['http'] = data[0].split(' ')
    processed['method'] = processed['http'][0]
    processed['data'] = data[-1]
    for e in data[1:-1]:
        try:
            current = e.split(': ')
            processed[current[0]] = current[1]
        except:
            pass
    return processed


def get_request_data(data):
    return parse_request(data)['data']


def get_request_path(data):
    return parse_request(data)['http'][1]


def is_POST(data):
    return 'POST' in parse_request(data)['method']


def is_GET(data):
    return 'GET' in parse_request(data)['method']


def is_ok(data):
    return parse_request(data)['http'][1] == '200'
