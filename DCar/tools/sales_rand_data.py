import asyncio
from typing import Any
import requests

URL = 'https://www.dongchedi.com/motor/pc/car/rank_data'
AID = 1839
RANK_DATA_TYPE = 11

async def download(url: str, params: dict[str, Any]):
    try:
      response = requests.get(url, params=params)
      if response.status_code == 200:
        data = response.json()
        print('page_info', data['data']['paging'])
        print('page_list', data['data']['list'])
      else:
          print('异常', response)
    except Exception as e:
        print('exception. ：', e)



if __name__ == '__main__':
    async def main():
      params = {'aid': AID, 'rank_data_type': RANK_DATA_TYPE}
      # 页面参数 count=10&offset=70
      params.update({'count': 10})
      params.update({'offset': 0})
      await download(URL, params)

    asyncio.run(main())