import json
import MeCab
import exchangeSlackToJson
import unidic
# C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\lib\site-packages\MeCab\
# if your environment can not import MeCab, you should copy and paste libmecab.dll ↑ to ↓
# C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages\MeCab\

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

# separare word of massage array
wakati = MeCab.Tagger('-Owakati')
for massage in massage_array:
    result = wakati.parse(massage)
