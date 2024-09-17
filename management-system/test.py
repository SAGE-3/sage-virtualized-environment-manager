import json

examples = [
    '{"urls":["about:home"]}',
    '{"urls":["about:home","null"]}',
    '{"urls":["about:home","https://www.youtube.com/"]}',
    '{"urls":["about:home","https://www.youtube.com/?themeRefresh=1"]}',
]


# test = json.loads('{"urls": ["about:home","https://www.youtube.com/watch?v=0XoT1z-gAQw","https://www.amazon.com/"]}')
test = json.loads(examples[3])

print(test)