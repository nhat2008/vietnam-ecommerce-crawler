from scrapy import log
from proxy import PROXIES
from agents import AGENTS

import random
from selenium import webdriver

"""
Custom proxy provider. 
"""
class CustomHttpProxyMiddleware(object):
    
    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.use_proxy(request):
            p = random.choice(PROXIES)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
            except Exception, e:
                log.msg("Exception %s" % e, _level=log.CRITICAL)
                
    
    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        if "depth" in request.meta and int(request.meta['depth']) <= 2:
            return False
        i = random.randint(1, 10)
        return i <= 2
    
    
"""
change request header nealy every time
"""
class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent


class JSMiddleware(object):
    def process_request(self, request, spider):
        print '>>>>>>>>>>>>>>'
        print request.meta

        # if request.meta.get('js'): # you probably want a conditional trigger
        driver = webdriver.PhantomJS()
        driver.get(request.url)
        body = driver.page_source
        f = open('data','w')
        print body
        f.write(body)
        f.closed

        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        # return
