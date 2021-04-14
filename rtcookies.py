from selenium import webdriver

headers = {
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': ' gzip, deflate, br',
    'Accept-Language': ' zh-CN,zh;q=0.9',
    'Cache-Control': ' max-age=0',
    'Connection': ' keep-alive',
    'Cookie': 'JSESSIONID=8976F5A6EEA889AE78AD0FA6A70689E0; zg_did=%7B%22did%22%3A%20%22178685f48124b-0dea03d8ab43ec-6252732d-144000-178685f481317%22%7D; _ga=GA1.3.1611319239.1616915533; _gid=GA1.3.2133340482.1616915533; aliyungf_tc=c2b072d974d07cc08fe94573cf37abacea5668a5244ae39fed6bce6b4653cef1; acw_tc=781bad4416169309103896129e3d223caf46b7f1556778705da66864e262db; CHSICC_CLIENTFLAGZSML=1f7c0048e2a49f1501a5e6658c46b4ea; zg_adfb574f9c54457db21741353c3b0aa7=%7B%22sid%22%3A%201616930910716%2C%22updated%22%3A%201616930910720%2C%22info%22%3A%201616658778142%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fyz.chsi.com.cn%2F%22%7D',
    'DNT': ' 1',
    'Host': ' yz.chsi.com.cn',
    'sec-ch-ua': ' " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': ' ?0',
    'Sec-Fetch-Dest': ' document',
    'Sec-Fetch-Mode': ' navigate',
    'Sec-Fetch-Site': ' none',
    'Sec-Fetch-User': ' ?1',
    'Upgrade-Insecure-Requests': ' 1',
    'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4449.6 Safari/537.36'
}


def getcookie(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option
    driver = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器

    # driver = webdriver.Chrome(executable_path='chromedriver.exe')  # chrome插件路径
    driver.get(url)  # 榜单地址
    got_cookies = driver.get_cookies()
    format_cookies = ''.join([f'{i["name"]}={i["value"]}; ' for i in got_cookies])[:-2]
    headers['Cookie'] = format_cookies
    driver.quit()  # 退出，关闭窗口
    return headers
