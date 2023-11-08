import re
import sys
import os

regx = [
    r"(.*(implementation|api)[\s]*)(['|\"]io\.agora\.rtc:iris-rtc(-beta)?:[0-9a-zA-Z\.-]+['|\"])",
    r"(.*(implementation|api)[\s]*)(['|\"]io\.agora\.rtc:(agora-)?(special-)?(full|voice)(-(preview|sdk))?:[0-9a-zA-Z\.-]+['|\"])",
    r"(.*(implementation|api)[\s]*)(['|\"]io\.agora\.rtc:full-screen-sharing(-special)?:[0-9a-zA-Z\.-]+['|\"])",
    r"(.*(pod|dependency)[\s]*)(['|\"]AgoraIrisRTC_iOS(_Beta)?['|\"],[\s]*['|\"][0-9a-zA-Z\.-]+['|\"])",
    r"(.*(pod|dependency)[\s]*)(['|\"]Agora(RtcEngine|Audio)(_Special)?_iOS(_Preview)?['|\"],[\s]*['|\"][0-9a-zA-Z\.-]+['|\"])",
    r"(.*(CDN:)?[\s]*)(https://download\.agora\.io/sdk/release/iris_[0-9a-zA-Z\.-]+_DCG_Windows_(Video|Audio)_([0-9]+)_([0-9]+)\.zip)",
    r"(.*(CDN:)?[\s]*)(https://download\.agora\.io/sdk/release/iris_[0-9a-zA-Z\.-]+_DCG_Mac_(Video|Audio)_([0-9]+)_([0-9]+)\.zip)",
    r"(.*(pod|dependency)[\s]*)(['|\"]AgoraIrisRTC_macOS(_Beta)?['|\"],[\s]*['|\"][0-9a-zA-Z\.-]+['|\"])",
    r"(.*(pod|dependency)[\s]*)(['|\"]Agora(RtcEngine|Audio)(_Special)?_macOS(_Preview)?['|\"],[\s]*['|\"][0-9a-zA-Z\.-]+['|\"])",
]
matches = []


def match(content: str):
    matches.clear()
    for r in regx:
        flag = False
        for line in content.splitlines():
            m = re.match(r, line)
            if m is not None and m.group(3) not in matches:
                matches.append(m.group(3))
                flag = True
                break
        if not flag:
            matches.append(None)

    for m in matches:
        print(m, end = "\r\n")


def replace(path: str):
    with open(path, 'r') as f:
        content = f.read()

    for i in range(len(matches)):
        if matches[i] is not None:
            content = re.sub(regx[i], r'\1' + matches[i], content)

    with open(path, 'w') as f:
        f.write(content)


match(sys.argv[1])

for path in sys.argv[3].splitlines():
    replace(os.path.join(sys.argv[2], path))
