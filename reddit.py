from recon.core.module import BaseModule
from urllib.parse import urlparse
import json

class Module(BaseModule):
  meta = {
      'name': 'Reddit link finder',
      'author': 'Max Harley (@Max_68)',
      'description': 'Finds domains that are linked in a reddit post',
      'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL'
      }
  def module_run(self, hosts):
    total_domains = 0

    for host in hosts:
      self.verbose('Trying domain: {}'.format(host))
      self.output("-------")
      url = 'http://reddit.com/domain/%s.json' % (host)

      try:
        resp = self.request(url)
        code = resp.status_code
        if code == 200 or code == 301:
          if resp.json == None:
            self.alert("No data was found for the url")
            return
          parsed = json.loads(resp.text)
          for child in parsed["data"]["children"]:
            total_domains += 1
            permalink = child['data']['permalink']
            reddit_url = child['data']['url']
            h = urlparse(reddit_url).hostname
            self.add_domains(h)
            self.alert('Permalink: http://reddit.com{}'.format(permalink))
        else:
          self.error('Error for domain {}'.format(url))
      except KeyboardInterrupt:
        raise KeyboardInterrupt

    self.alert('Added {} domains'.format(total_domains))
