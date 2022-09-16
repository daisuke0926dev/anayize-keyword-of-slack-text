import json
import MeCab
import exchangeSlackToJson
import unidic
from yake import KeywordExtractor
# C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\lib\site-packages\MeCab\
# if your environment can not import MeCab, you should copy and paste libmecab.dll ↑ to ↓
# C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages\MeCab\

def separete():
    # get json string
    non_decode_js_array = exchangeSlackToJson.exchange()
    decoded_js_array = []
    for non_decode_js in non_decode_js_array:
        # decode json string
        decoded_js = json.loads(non_decode_js)
        decoded_js_array.append(decoded_js)

    # make only massage array
    massage_array = []
    for rec in decoded_js_array:
        rec = rec['value']
        post = rec['post']
        post = post['value']
        massage_array.append(post['massage'])

    wakati = MeCab.Tagger('-Owakati')
    separeted_massage_array = []
    # separare word of massage array
    for massage in massage_array:
        separeted_massage_array.append(wakati.parse(massage))
    return separeted_massage_array
