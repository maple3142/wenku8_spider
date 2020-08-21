from b2.api import B2Api
from wenku8_spider.credentials import *

api = B2Api()
api.authorize_account('production', B2_ACCOUNT_ID, B2_APPLICATION_KEY)

print(api.get_bucket_by_name('maple-scraping'))
