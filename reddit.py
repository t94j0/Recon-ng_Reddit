from recon.core.module import BaseModule
import json

class Module(BaseModule):
  meta = {
      'name': 'Reddit link finder',
      'author': 'Max Harley (@Max_68)',
      'description': 'Finds domains that are linked in a reddit post',
      'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL'
      }
  def module_run(self, hosts):
    for host in hosts:
      url = 'http://reddit.com/domain/%s.json' % (host)
      try:
        resp = self.request(url)
        code = resp.status_code
      except KeyboardInterrupt:
        raise KeyboardInterrupt
      except:
        code = 'Error'
      if code == 200 or code == 301:
        if resp.json == None:
          self.alert("No data was found for the url")
          return
        parsed = json.loads(resp.text)
        for child in parsed["data"]["children"]:
          permalink = child['data']['permalink']
          reddit_url = child['data']['url']
          self.add_domains(reddit_url)
          self.alert('Permalink: http://reddit.com%s' % (permalink))
          self.alert('Added new domain')
      else:
        self.error('Error for domain %s' % (url))
