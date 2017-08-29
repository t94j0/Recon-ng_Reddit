from recon.core.module import BaseModule
import urlparse
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
      url = 'http://reddit.com/domain/{}.json'.format(host)

      resp = self.request(url)
      code = resp.status_code
      if code == 200 or code == 301:
        if resp.json == None:
          self.alert('No data was found for the url')
          return

        for child in resp.json['data']['children']:
          total_domains += 1
          permalink = child['data']['permalink']
          reddit_url = child['data']['url']
          h = urlparse.urlparse(reddit_url).hostname
          self.add_hosts(h)
          self.alert('Permalink: http://reddit.com{}'.format(permalink))
      else:
        self.error('Error for domain {}'.format(url))
