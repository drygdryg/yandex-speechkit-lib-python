# Yandex SpeechKit Python SDK

![PyPI](https://img.shields.io/pypi/v/speechkit) ![GitHub](https://img.shields.io/github/license/tikhonp/yandex-speechkit-lib-python) ![PyPI - Format](https://img.shields.io/pypi/format/wheel) [![Build Status](https://travis-ci.com/TikhonP/yandex-speechkit-lib-python.svg?branch=master)](https://travis-ci.com/TikhonP/yandex-speechkit-lib-python) [![Updates](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/shield.svg)](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/) [![Python 3](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/python-3-shield.svg)](https://pyup.io/repos/github/TikhonP/yandex-speechkit-lib-python/) [![codecov](https://codecov.io/gh/tikhonp/yandex-speechkit-lib-python/branch/master/graph/badge.svg?token=NRNV9E36I4)](https://codecov.io/gh/tikhonp/yandex-speechkit-lib-python) [![Documentation Status](https://readthedocs.org/projects/yandex-speechkit-lib-python/badge/?version=latest)](https://yandex-speechkit-lib-python.readthedocs.io/en/latest/?badge=latest)

Python SDK for Yandex SpeechKit API.

This library supports absolutely all Yandex SpeechKit methods including “Streaming mode for short audio recognition”. For more information please visit [Yandex Speechkit API Docs](https://cloud.yandex.com/en/docs/speechkit/).

# Getting Started

Assuming that you have Python and `virtualenv` installed, set up your environment and install the required dependencies
like this, or you can install the library using `pip`:

```bash
$ git clone https://github.com/TikhonP/yandex-speechkit-lib-python.git
$ cd yandex-speechkit-lib-python
$ virtualenv venv
...
$ . venv/bin/activate
$ python -m pip install -r requirements.txt
$ python -m pip install .
```

```bash
python -m pip install speechkit
```

# SpeechKit documentation

See [speechkit readthedocs](https://yandex-speechkit-lib-python.readthedocs.io/en/latest/index.html) or [speechkit docs in PDF](https://yandex-speechkit-lib-python.readthedocs.io/_/downloads/en/latest/pdf/) for more info.

# Using speechkit

There are support of synthesis, recognizing long and short audio. For more information please read [Documentation](https://yandex-speechkit-lib-python.readthedocs.io/en/latest/index.html).

First you need create session for authorisation:

```python3
from speechkit import Session

oauth_token = str('<oauth_token>')
folder_id = str('<folder_id>')
api_key = str('<api-key>')
jwt_token = str('<jwt_token>')

oauth_session = Session.from_yandex_passport_oauth_token(oauth_token, folder_id)
api_key_session = Session.from_api_key(api_key)
jwt_session = Session.from_jwt(jwt_token)
```

Use created session to make other requests.

There are also functions for getting credentials (read [Documentation](https://yandex-speechkit-lib-python.readthedocs.io/en/latest/index.html) for more info):
`Speechkit.auth.generate_jwt`,  `speechkit.auth.get_iam_token`, `speechkit.auth.get_api_key`

### For audio recognition

Short audio:

```python3
from speechkit import ShortAudioRecognition

recognizeShortAudio = ShortAudioRecognition(session)
with open(str('/Users/tikhon/Desktop/out.wav'), str('rb')) as f:
    data = f.read()

print(recognizeShortAudio.recognize(data, format='lpcm', sampleRateHertz='48000'))

# Will be printed: 'text that need to be recognized'
```

See example with long
audio [long_audio_recognition.py](https://github.com/TikhonP/yandex-speechkit-lib-python/blob/master/examples/long_audio_recognition.py)
.

See example with streaming
audio [streaming_recognize.py](https://github.com/TikhonP/yandex-speechkit-lib-python/blob/master/examples/streaming_recognize.py)

### For synthesis

```python3
from speechkit import SpeechSynthesis

synthesizeAudio = SpeechSynthesis(session)
synthesizeAudio.synthesize(
    str('/Users/tikhon/Desktop/out.wav'), text='Текст который нужно синтезировать',
    voice='oksana', format='lpcm', sampleRateHertz='16000'
)
```

# TODO

- Provide wide range of exceptions (There is only `speechkit.exceptions.RequestError` right now)
- Add troubleshooting headers to `speechkit.Session`
- Add gRPC streaming synthesis

# License

MIT

Tikhon Petrishchev 2021
