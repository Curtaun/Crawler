import sys
import json
import re
from Lib.Epub import Epub

if len(sys.argv) != 2:
    print("缺失json文件")
else:
    file = sys.argv[1]

    with open(file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    e = Epub(describe={
        "name": raw["bookname"],
        "author": raw["author"],
        "update_time": raw["book_uptime"],
        "coverurl": raw["cover"],
        "describe": raw["details"].split("\n")
    })
    for i in raw["chapterList"]:
        Chaptername = i["name"]
        for j in i["lists"]:
            content = j["content"].split("\n")
            text = [{
                "Uid": j["href"].split("/")[-1],
                "title": f'{Chaptername}-{j["name"]}',
                "lines": []
            }]
            for k in content:
                k = k.replace('\u3000', " ")
                if "<img" not in k:
                    text[0]['lines'].append({
                        "type": "p",
                        "item": k
                    })
                else:
                    text[0]['lines'].append(
                        {
                            "type": "img",
                            "item": re.findall(r'''<img src="([\s\S]+?)" ''', k)[0]
                        }
                    )
            e.add_text(text)

    e.finish()