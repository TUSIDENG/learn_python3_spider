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
        if 'paging' in data['data']:
            print("paging键 存在")
        else:
            print("paging键 不存在")
        return data

      else:
          print('异常', response)
          res = {
              "code": response.status_code,
              "message": response.text,
              "data": None
          }
          return res
    except Exception as e:
        print('exception. ：', e)
        res = {
            "code": 500,
            "message": str(e),
            "data": None
        }
        return res



if __name__ == '__main__':
    async def main():
      params = {'aid': AID, 'rank_data_type': RANK_DATA_TYPE}
      # 页面参数 count=10&offset=70
      params.update({'count': 10})
      params.update({'offset': 0})
      await download(URL, params)

    asyncio.run(main())