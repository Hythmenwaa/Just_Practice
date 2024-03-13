# 好兆头第一部 第1集
import requests
import re
import os

Good_Omens_1 = "Good_Omens_1/"

try:
    os.makedirs(Good_Omens_1)
    print(f"目录{Good_Omens_1}创建完毕。")
except FileExistsError:
    print(f"目录{Good_Omens_1}已存在，无需创建。")
except Exception as e:
    print("创建目录时出错:", e)
    exit(0)

url = "https://91mjw.tv/vplay/MTk0ODg3NS0xLTE=.html"
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
                  "/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

resp = requests.get(url=url, headers=head)
page_content = resp.text

obj = re.compile(r'<iframe src="(?P<video>.*?)" style="width: 100%; height: 100%;"></iframe>', re.S)
result = obj.finditer(page_content)

dic = {}
for i in result:
    dic = i.groupdict()
    dic['video'] = dic['video'].strip()

m3u8_url_piece = dic['video'].split('=')[-1]
m3u8_url = f"{m3u8_url_piece.rsplit('/', 1)[0]}/2000kb/hls/{m3u8_url_piece.rsplit('/', 1)[1]}"

resp.close()

# 下载m3u8文件
# https://vod4.bdzybf7.com/20220410/7Qum7cGk/index.m3u8
m3u8_resp = requests.get(url=m3u8_url, headers=head)
with open("Good_Omens.m3u8", mode="wb") as f:
    f.write(m3u8_resp.content)

m3u8_resp.close()

# 解析文件
# https://vod4.bdzybf7.com
header = m3u8_url_piece.rsplit("/", 3)[0]

n = 1
with open("Good_Omens.m3u8", mode="r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        child_url = header + line

        resp_child_url = requests.get(child_url)
        f = open("Good_Omens_1/" + f"{n}.ts", mode="wb")
        f.write(resp_child_url.content)
        f.close()
        resp_child_url.close()

        print(f"完成获取 {n}.ts")
        n += 1
