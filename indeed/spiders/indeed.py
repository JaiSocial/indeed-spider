import os
import datetime
import scrapy
from jinja2 import Environment, FileSystemLoader

##
## Title to be written to the output HTML report file
##
TITLE = 'Search Results for Software Engineer Remote jobs'

## Absolute path of the templates directory relative to this spider class file
##
TEMPLATE_FILES_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../templates'

TEMPLATE_FILE = 'indeed_search_results_template.html'

OUTFILE = './indeed_search_results.html'

BASE_URL = 'https://www.indeed.com'

INITIAL_URL = 'https://www.indeed.com/jobs?q=Remote+Software+Engineer+-ts%2Fsci+-C%23+-.NET&jt=fulltime'

class IndeedSpider(scrapy.Spider):

	name = 'indeed'

	allowed_domains = [INITIAL_URL]

	start_urls = [INITIAL_URL]

	def parse(self, response):
		
		self.item_list = []

		links = response.xpath('//div[contains(@class, "row")]//a[contains(@data-tn-element, "jobTitle")]')

		for link in links:

			href = link.xpath('@href').extract_first()

			title = link.xpath('@title').extract_first()

			full_href = BASE_URL + href

			self.item_list.append({'href' : full_href, 'title' : title})


		self._generate_report()


	def _generate_report(self):


		now = datetime.datetime.now()

		j2_env = Environment(loader=FileSystemLoader(TEMPLATE_FILES_DIR),trim_blocks=True)
	    
		content = j2_env.get_template(TEMPLATE_FILE).render(date=now, title=TITLE, record_list = self.item_list, start_url=INITIAL_URL)

		f = open(OUTFILE, "w+")

		f.write(content)

		f.close()

		self.log("Wrote results to '%s'"  % OUTFILE)
