# PythonBceAPIAuth

[![forthebadge](http://forthebadge.com/images/badges/built-by-codebabes.svg)](http://forthebadge.com)  

> [More detail...](https://cloud.baidu.com/doc/Reference/AuthenticationMechanism.html#.B3.EE.B6.D3.25.F4.2B.A9.8E.EC.89.EC.17.BD.8C.DD)

This program can generat a `API Auth Token` follow bce auth rule

# Getting Started

## Example

```python
from PythonBceAPIAuth.bceauth import SignTokenGenerator
# build object
token_obj = SignTokenGenerator(
        'AK',  # access key id
        'SK',  # secret access key
        'POST',  # method
        '/v2/document',  # uri
        {'source':'bos'},  # get params
        'doc.bj.baidubce.com'  # endpoint
        )
# get token
print(token_obj.Token)
```

## Depends
- urllib
- datetime
- hashlib
- hmac
- time
