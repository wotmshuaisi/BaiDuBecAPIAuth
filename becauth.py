from urllib.request import quote
from datetime import datetime
import hashlib
import hmac
import time

class SignTokenGenerator(object):
    expire_time = 3600    

    def __init__(self, AK, SK, method, uri, params, host):
        """
        :AK : access key id
        :sk : secret access ke
        :method : method
        :uri : path
        :params : get params
        :host : endpoint
        """
        self.AK = AK
        self.SK = SK
        current_timestamp = datetime.utcnow().utctimetuple()
        self.time = time.strftime('%Y-%m-%dT%H:%M:%SZ', current_timestamp)
        
        self.method = method
        self.uri = self._standard_uri(uri)
        self.params = self._standard_queryset(params)
        self.headers = 'host:{}\nx-bce-date:{}'.format(host, quote(self.time))

    def _standard_uri(self, uri):
        """
        :return : urlencoded path
        """
        if not uri:
            return '/'
        return quote(uri)

    def _standard_queryset(self, queryset):
        """
        get params standard format
        :return : 'key=val&key=val'
        """
        result = []
        for k, v in queryset.items():
            if k == 'authorization':
                continue
            result.append('{}={}'.format(k, v))
        result.sort()
        return '&'.join(result)

    def _standard_request(self, ):
        """
        request standard format
        """
        request_list = [self.method, self.uri, self.params, self.headers]
        return '\n'.join(request_list)

    def _gen_signingkey(self,):
        """
        generate signingkey
        """
        signingkey = hmac.new(
            bytes(self.SK, 'utf-8'),
            bytes('bce-auth-v1/{}/{}/{}'.format(self.AK, self.time, self.expire_time), 'utf-8'),
            hashlib.sha256
        )
        return signingkey.hexdigest()
        
    def _gen_signature(self,):
        """
        generate signature
        """
        signingkey = self._gen_signingkey()
        signature = hmac.new(
            bytes(signingkey, 'utf-8'),
            bytes(self._standard_request(), 'utf-8'),
            hashlib.sha256
        )
        return signature.hexdigest()

    @property
    def Token(self, ):
        """
        generate token
        :return : token string, time string
        """
        tpl = 'bce-auth-v1/{}/{}/{}/host;x-bce-date/{}'
        tpl = tpl.format(self.AK, self.time, self.expire_time, self._gen_signature())
        return (tpl, self.time)
