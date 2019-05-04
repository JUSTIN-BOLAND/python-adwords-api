#https://developers.google.com/adwords/api/docs/samples/python/optimization#get-keywords-related-to-a-seed-keyword

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example retrieves keywords that are related to a given keyword.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

from googleads import adwords
from time import sleep
import sys
import datetime

# Optional AdGroup ID used to set a SearchAdGroupIdSearchParameter.
AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'
PAGE_SIZE = 10


def main(client, item, ad_group_id=None):
  # Initialize appropriate service.
  targeting_idea_service = client.GetService(
      'TargetingIdeaService', version='v201809')

  # Construct selector object and retrieve related keywords.
  selector = {
      'ideaType': 'KEYWORD',
      'requestType': 'STATS'
  }

  selector['requestedAttributeTypes'] = [
      'KEYWORD_TEXT', 'SEARCH_VOLUME']

  offset = 0
  selector['paging'] = {
      'startIndex': str(offset),
      'numberResults': str(PAGE_SIZE)
  }

  selector['searchParameters'] = [{
      'xsi_type': 'RelatedToQuerySearchParameter',
      'queries': item
  }]

  # Language setting (optional).
  selector['searchParameters'].append({
      # The ID can be found in the documentation:
      # https://developers.google.com/adwords/api/docs/appendix/languagecodes
      'xsi_type': 'LanguageSearchParameter',
      'languages': [{'id': '1004'}]
  })

  # Location setting (optional).
  selector['searchParameters'].append({
      # The ID can be found in the documentation:
      # https://developers.google.com/adwords/api/docs/appendix/geotargeting
      'xsi_type': 'LocationSearchParameter',
      'locations': [{'id': '2380'}]
  })

  # Network search parameter (optional)
  selector['searchParameters'].append({
      'xsi_type': 'NetworkSearchParameter',
      'networkSetting': {
          'targetGoogleSearch': True,
          'targetSearchNetwork': False,
          'targetContentNetwork': False,
          'targetPartnerSearchNetwork': False
      }
  })

  # Use an existing ad group to generate ideas (optional)
  if ad_group_id is not None:
    selector['searchParameters'].append({
        'xsi_type': 'SeedAdGroupIdSearchParameter',
        'adGroupId': ad_group_id
    })

  more_pages = True
  while more_pages:
    page = targeting_idea_service.get(selector)

    # Display results.
    if 'entries' in page:
      for result in page['entries']:
        attributes = {}
        for attribute in result['data']:
          attributes[attribute['key']] = getattr(attribute['value'], 'value', '0')
        results_file.write('%s|%s|%s\n' % (item, attributes['KEYWORD_TEXT'], attributes['SEARCH_VOLUME']))
        print ('%s|%s|%s' % (item, attributes['KEYWORD_TEXT'], attributes['SEARCH_VOLUME']))
      print
    else:
      print ('No related keywords were found.')
    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])

if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage("ABSOLUTE-PATH-TO-googleads.yaml")
  adwords_client.SetClientCustomerId('ENTER-YOURS-HERE')

  kwds = open("_kwds.txt","r")
  reload(sys)
  sys.setdefaultencoding('utf-8')
  
  for line in kwds:
      item = line.strip()
      results_file = open("_results.txt", "a+")
      main(adwords_client, item, int(AD_GROUP_ID) if AD_GROUP_ID.isdigit() else None)
      print(datetime.datetime.now())
      results_file.close()
      sleep(2)
