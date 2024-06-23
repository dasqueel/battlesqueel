'''
ever tuesday or wednesday or whenever the pff grades drop.  and get the new json and store it in a new json file?

where to store?
'''
import requests
import pprint

def getGame(gameId):
    url = f"https://premium.pff.com/api/v1/facet/offense/summary?game_id={gameId}"
    premiumCookie = "_premium_key=SFMyNTY.g3QAAAABbQAAABZndWFyZGlhbl9kZWZhdWx0X3Rva2VubQAAAlpleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpRY21WdGFYVnRJaXdpWlhod0lqb3hOamt5TmpReU5EZzFMQ0pwWVhRaU9qRTJPVEkyTkRBMk9EVXNJbWx6Y3lJNklsQnlaVzFwZFcwaUxDSnFkR2tpT2lKaFkyRTJNVEF5TUMxaE1qaGtMVFEzTURFdE9EWXdaQzA0WVdJMk5qWTNPVFF3WmpjaUxDSnVZbVlpT2pFMk9USTJOREEyT0RRc0luQmxiU0k2ZXlKaFlXWWlPakVzSW01allXRWlPakVzSW01bWJDSTZNU3dpZUdac0lqb3hmU3dpYzNWaUlqb2llMXdpWlcxaGFXeGNJanBjSW1SaGMzRjFaV1ZzUUhsaGFHOXZMbU52YlZ3aUxGd2labVZoZEhWeVpYTmNJanBiWFN4Y0ltWnBjbk4wWDI1aGJXVmNJanB1ZFd4c0xGd2liR0Z6ZEY5dVlXMWxYQ0k2Ym5Wc2JDeGNJblZwWkZ3aU9sd2laV1l5Wm1VeU5XTXRNbVpoT1MwME9XWm1MVGszTURjdE0yWmlPVGMzTldZeVlXSTRYQ0lzWENKMlpYSjBhV05oYkZ3aU9sd2lRMjl1YzNWdFpYSmNJbjBpTENKMGVYQWlPaUpoWTJObGMzTWlmUS4xUTk0NW5OanN2MThScFVCLUk3ZmpEOUxZZy16dFBmUjc4MVFtbEhaNmsxWGM0QmhrcEdkcEE1c3M0eXpNeld3NjlNejJEQ2FabEdVLUJvX2pRX2FyUQ.Do9MGbZkUf_3uFuN-oYT2qMKniBrxgK5408eWlOQ3Q8; c_groot_access_token=3arYn3bfruqelfFY2Mdin9Ak8vk9vrwW2-wYNhmUh-4-E65U9CCFHUB9mUjoyOgP; c_groot_access_ts=2023-08-21T17:32:29Z; c_groot_refresh_token=mHnOOBo011bRj32wBZitQr1-rpePDjFrEPKxvEedtmo7lPJDCtMVwFwxuAmSu3U9"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://premium.pff.com/ncaa/games/2022/9/missouri-tigers/offense',
        'Cookie': premiumCookie,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'DNT': '1',
        'TE': 'trailers'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response)

def getPosition(position):
    url = f"https://www.pff.com/api/nfl/grades?league=ncaa&position={position}&season=2023"
    url = f"https://www.pff.com/api/nfl/grades?league=ncaa&position=CB&season=2023"
    cookie = "_merlin_key=SFMyNTY.g3QAAAAFbQAAAAtfY3NyZl90b2tlbm0AAAAYWWFyaXpBa3BfVzdvWk9BRHJHWUJFZnV5bQAAABZndWFyZGlhbl9kZWZhdWx0X3Rva2VubQAAAjtleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpOWlhKc2FXNGlMQ0psZUhBaU9qRTNNVGt3T1RJek9ESXNJbWxoZENJNk1UY3hPVEE0T0RjNE1pd2lhWE56SWpvaVRXVnliR2x1SWl3aWFuUnBJam9pTUdKbU9EQm1Zell0Tm1FeU9TMDBPVEV6TFdKaFpqY3ROR1V5WVRSaE4yTTRNRFUwSWl3aWJtSm1Jam94TnpFNU1EZzROemd4TENKd1pXMGlPbnNpY0hKbGJXbDFiU0k2TVgwc0luTjFZaUk2SW50Y0ltVnRZV2xzWENJNlhDSmtZWE54ZFdWbGJFQjVZV2h2Ynk1amIyMWNJ…YB78AXGHxCEmPiCd1-835OJvcY; AWSALB=eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk; AWSALBCORS=eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk; c_groot_access_token=Mt9zaZszSoqUWdJR5H6iKRnXT7D5Qw4UdaGsQ4YPF8g0OD9X9I6FOpki3ZluNgv6; c_groot_access_ts=2024-06-22T20:39:42Z; c_groot_refresh_token=0r3rFTEZIvz6u4Hl2aNQ4U0jiNE1GNW17E8j-NNUVoqqSYLZflV9WR5n_5lLd5vy"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': f'https://www.pff.com/college/grades/position/{position}',
        'Cookie': '_merlin_key=SFMyNTY.g3QAAAAFbQAAAAtfY3NyZl90b2tlbm0AAAAYWWFyaXpBa3BfVzdvWk9BRHJHWUJFZnV5bQAAABZndWFyZGlhbl9kZWZhdWx0X3Rva2VubQAAAjtleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpOWlhKc2FXNGlMQ0psZUhBaU9qRTNNVGt3T1RJek9ESXNJbWxoZENJNk1UY3hPVEE0T0RjNE1pd2lhWE56SWpvaVRXVnliR2x1SWl3aWFuUnBJam9pTUdKbU9EQm1Zell0Tm1FeU9TMDBPVEV6TFdKaFpqY3ROR1V5WVRSaE4yTTRNRFUwSWl3aWJtSm1Jam94TnpFNU1EZzROemd4TENKd1pXMGlPbnNpY0hKbGJXbDFiU0k2TVgwc0luTjFZaUk2SW50Y0ltVnRZV2xzWENJNlhDSmtZWE54ZFdWbGJFQjVZV2h2Ynk1amIyMWNJ…YB78AXGHxCEmPiCd1-835OJvcY; AWSALB=eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk; AWSALBCORS=eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk; c_groot_access_token=Mt9zaZszSoqUWdJR5H6iKRnXT7D5Qw4UdaGsQ4YPF8g0OD9X9I6FOpki3ZluNgv6; c_groot_access_ts=2024-06-22T20:39:42Z; c_groot_refresh_token=0r3rFTEZIvz6u4Hl2aNQ4U0jiNE1GNW17E8j-NNUVoqqSYLZflV9WR5n_5lLd5vy',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'DNT': '1',
        'TE': 'trailers'
    }



    # response = requests.request("GET", url, headers=headers, data=payload)
    response = requests.request("GET", url, headers=headers)

    json = response.json()
    print(json)
    # players = json['players']

    # for player in players:
    #     print(player['name'])

def test():
    cookies = {
        '_merlin_key': 'SFMyNTY.g3QAAAAFbQAAAAtfY3NyZl90b2tlbm0AAAAYWWFyaXpBa3BfVzdvWk9BRHJHWUJFZnV5bQAAABZndWFyZGlhbl9kZWZhdWx0X3Rva2VubQAAAjtleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpOWlhKc2FXNGlMQ0psZUhBaU9qRTNNVGt3T1RJek9ESXNJbWxoZENJNk1UY3hPVEE0T0RjNE1pd2lhWE56SWpvaVRXVnliR2x1SWl3aWFuUnBJam9pTUdKbU9EQm1Zell0Tm1FeU9TMDBPVEV6TFdKaFpqY3ROR1V5WVRSaE4yTTRNRFUwSWl3aWJtSm1Jam94TnpFNU1EZzROemd4TENKd1pXMGlPbnNpY0hKbGJXbDFiU0k2TVgwc0luTjFZaUk2SW50Y0ltVnRZV2xzWENJNlhDSmtZWE54ZFdWbGJFQjVZV2h2Ynk1amIyMWNJaXhjSW1abFlYUjFjbVZ6WENJNlcxMHNYQ0ptYVhKemRGOXVZVzFsWENJNmJuVnNiQ3hjSW14aGMzUmZibUZ0WlZ3aU9tNTFiR3dzWENKMWFXUmNJanBjSW1WbU1tWmxNalZqTFRKbVlUa3RORGxtWmkwNU56QTNMVE5tWWprM056Vm1NbUZpT0Z3aUxGd2lkbVZ5ZEdsallXeGNJanBjSWtOdmJuTjFiV1Z5WENKOUlpd2lkSGx3SWpvaVlXTmpaWE56SW4wLjUxRmpEUldQeDRUY0FKYkZrYWJLbHRrcmlFVk9oNklFcU8xM1lCejF6UFh6bkhyQnh5WmRpaGl4RTF3eHRDVXFLZ0hJd2VjUUpTc2V0UXhkRVNNa25RbQAAABhsYXVuY2hfZGFya2x5X3Nlc3Npb25faWRtAAAAJGY4NWM0ZDNlLTAwOGQtNGUwZC1hMWQ3LTI5Zjg2MzQ2NWEzM20AAAAabGF1bmNoX2RhcmtseV91c2VyX2NvbnRleHR0AAAAA2QACmF0dHJpYnV0ZXN0AAAAB2QAAmlwbQAAACUyNjAzOjMwMGI6N2U1Ojk4MDA6M2NlMzplNTU0OmYyZGU6YTdmbQAAAAlhbm9ueW1vdXNkAAVmYWxzZW0AAAALcGZmSW50ZXJuYWxkAAVmYWxzZW0AAAAJcGZmVXNlcklkbQAAACRlZjJmZTI1Yy0yZmE5LTQ5ZmYtOTcwNy0zZmI5Nzc1ZjJhYjhtAAAAB3ByZW1pdW1kAAR0cnVlbQAAAAlzZXNzaW9uSWRtAAAAJGY4NWM0ZDNlLTAwOGQtNGUwZC1hMWQ3LTI5Zjg2MzQ2NWEzM20AAAAIc2lnbmVkSW5kAAR0cnVlZAADa2V5bQAAACRlZjJmZTI1Yy0yZmE5LTQ5ZmYtOTcwNy0zZmI5Nzc1ZjJhYjhkAARraW5kbQAAAAR1c2VybQAAAAlyZXR1cm5fdG9tAAAAGy9jb2xsZWdlL2dyYWRlcy9wb3NpdGlvbi9jYg.NcG2NCnFp1C57Lp7TYB78AXGHxCEmPiCd1-835OJvcY',
        'AWSALB': 'eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk',
        'AWSALBCORS': 'eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk',
        'c_groot_access_token': 'Mt9zaZszSoqUWdJR5H6iKRnXT7D5Qw4UdaGsQ4YPF8g0OD9X9I6FOpki3ZluNgv6',
        'c_groot_access_ts': '2024-06-22T20:39:42Z',
        'c_groot_refresh_token': '0r3rFTEZIvz6u4Hl2aNQ4U0jiNE1GNW17E8j-NNUVoqqSYLZflV9WR5n_5lLd5vy',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Sec-GPC': '1',
        'Alt-Used': 'www.pff.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.pff.com/college/grades/position/cb',
        # 'Cookie': '_merlin_key=SFMyNTY.g3QAAAAFbQAAAAtfY3NyZl90b2tlbm0AAAAYWWFyaXpBa3BfVzdvWk9BRHJHWUJFZnV5bQAAABZndWFyZGlhbl9kZWZhdWx0X3Rva2VubQAAAjtleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpOWlhKc2FXNGlMQ0psZUhBaU9qRTNNVGt3T1RJek9ESXNJbWxoZENJNk1UY3hPVEE0T0RjNE1pd2lhWE56SWpvaVRXVnliR2x1SWl3aWFuUnBJam9pTUdKbU9EQm1Zell0Tm1FeU9TMDBPVEV6TFdKaFpqY3ROR1V5WVRSaE4yTTRNRFUwSWl3aWJtSm1Jam94TnpFNU1EZzROemd4TENKd1pXMGlPbnNpY0hKbGJXbDFiU0k2TVgwc0luTjFZaUk2SW50Y0ltVnRZV2xzWENJNlhDSmtZWE54ZFdWbGJFQjVZV2h2Ynk1amIyMWNJaXhjSW1abFlYUjFjbVZ6WENJNlcxMHNYQ0ptYVhKemRGOXVZVzFsWENJNmJuVnNiQ3hjSW14aGMzUmZibUZ0WlZ3aU9tNTFiR3dzWENKMWFXUmNJanBjSW1WbU1tWmxNalZqTFRKbVlUa3RORGxtWmkwNU56QTNMVE5tWWprM056Vm1NbUZpT0Z3aUxGd2lkbVZ5ZEdsallXeGNJanBjSWtOdmJuTjFiV1Z5WENKOUlpd2lkSGx3SWpvaVlXTmpaWE56SW4wLjUxRmpEUldQeDRUY0FKYkZrYWJLbHRrcmlFVk9oNklFcU8xM1lCejF6UFh6bkhyQnh5WmRpaGl4RTF3eHRDVXFLZ0hJd2VjUUpTc2V0UXhkRVNNa25RbQAAABhsYXVuY2hfZGFya2x5X3Nlc3Npb25faWRtAAAAJGY4NWM0ZDNlLTAwOGQtNGUwZC1hMWQ3LTI5Zjg2MzQ2NWEzM20AAAAabGF1bmNoX2RhcmtseV91c2VyX2NvbnRleHR0AAAAA2QACmF0dHJpYnV0ZXN0AAAAB2QAAmlwbQAAACUyNjAzOjMwMGI6N2U1Ojk4MDA6M2NlMzplNTU0OmYyZGU6YTdmbQAAAAlhbm9ueW1vdXNkAAVmYWxzZW0AAAALcGZmSW50ZXJuYWxkAAVmYWxzZW0AAAAJcGZmVXNlcklkbQAAACRlZjJmZTI1Yy0yZmE5LTQ5ZmYtOTcwNy0zZmI5Nzc1ZjJhYjhtAAAAB3ByZW1pdW1kAAR0cnVlbQAAAAlzZXNzaW9uSWRtAAAAJGY4NWM0ZDNlLTAwOGQtNGUwZC1hMWQ3LTI5Zjg2MzQ2NWEzM20AAAAIc2lnbmVkSW5kAAR0cnVlZAADa2V5bQAAACRlZjJmZTI1Yy0yZmE5LTQ5ZmYtOTcwNy0zZmI5Nzc1ZjJhYjhkAARraW5kbQAAAAR1c2VybQAAAAlyZXR1cm5fdG9tAAAAGy9jb2xsZWdlL2dyYWRlcy9wb3NpdGlvbi9jYg.NcG2NCnFp1C57Lp7TYB78AXGHxCEmPiCd1-835OJvcY; AWSALB=eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk; AWSALBCORS=eksk7ykbas4QBOx9RYh/Ej7SUUW8l5yhDJI10AUmyJq//dJUwrK6rFsg3z+257aWTpLl9i69fl1g5M8ZjzZ8pL7Aw6GeFBLhn8fGagyWNu64ZHWHwCyJUACFENzk; c_groot_access_token=Mt9zaZszSoqUWdJR5H6iKRnXT7D5Qw4UdaGsQ4YPF8g0OD9X9I6FOpki3ZluNgv6; c_groot_access_ts=2024-06-22T20:39:42Z; c_groot_refresh_token=0r3rFTEZIvz6u4Hl2aNQ4U0jiNE1GNW17E8j-NNUVoqqSYLZflV9WR5n_5lLd5vy',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'league': 'ncaa',
        'position': 'CB',
        'season': '2023',
    }

    response = requests.get('https://www.pff.com/api/nfl/grades', params=params, cookies=cookies, headers=headers)
    json = response.json()

    players = json['players']
    cleanPlayerObjs = []

    for player in players:
        cleanPlayerObj = {k: v for k, v in player.items() if v is not None}
        cleanPlayerObjs.append(cleanPlayerObj)

    for player in cleanPlayerObjs:
        pprint.pprint(player)

if __name__ == "__main__":
    # getPosition("cb")
    test()