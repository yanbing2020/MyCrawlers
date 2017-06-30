# -*- coding: utf-8 -*-
# 爬取代理ip

import requests
from scrapy.selector import Selector
import MySQLdb


conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="12345678", db="spider", charset="utf8")
cursor = conn.cursor()

def crawler_ips():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    for i in range(1, 1568):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        headers
        url = "http://www.xicidaili.com/nn/{0}".format(i)
        url_re = requests.get(url)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))
        for ip_info in ip_list:
            cursor.execute(
                "insert ignore proxy_ips(ip, port, speed, proxy_type) VALUES ('{0}', '{1}',{2}, 'HTTP')".format(
                    ip_info[0], ip_info[1], ip_info[3]
                )
            )
        conn.commit()


class GetIP(object):
    def delete_ip(self,ip):
        delete_sql = """
            delete from proxy_ips where ip = '{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return  True

    def judge_ip(self, ip, port):
        # 是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "https://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http":proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=3)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code <300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # from db 随机取ip
        random_sql ="""
              SELECT ip, port FROM proxy_ips
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()



if __name__ == '__main__':
    # crawler_ips()
    getip = GetIP()
    getip.get_random_ip()
