import re
import json
import argparse

# useage
# python dep.py "input_string" --output "output.json"


android_cdnRegex = [
    r"https://download.(?:agora|shengwang)[^\s]*iris[^\s]*_Android[^\s]*\.zip",
    r"https://download.(?:agora|shengwang)[^\s]*Native_SDK_for_Android[^\s]*\.zip",
]

mavenRegex = [
    r"\b(?:implementation|api)\s+['|\"](?:cn|io)\.(?:agora|shengwang)\.rtc:?(?:agora-)?(?:special-)?(?:full|voice)?(?:-preview|-sdk)?:[a-zA-Z0-9_.-]+['|\"]",
    r"\b(?:implementation|api)\s+['|\"](?:cn|io)\.(?:agora|shengwang)\.rtc:full-screen-sharing(?:-special)?:[a-zA-Z0-9_.-]+['|\"]",
    r"\b(?:implementation|api)\s+['|\"](?:cn|io)\.(?:agora|shengwang)\:agora-rtm:[a-zA-Z0-9_.-]+['|\"]",
    r"\b(?:implementation|api)\s+['|\"](?:cn|io)\.(?:agora|shengwang)\.rtc:iris-rtc(?:agora-)?(?:special-)?(?:full|voice)?(?:-preview|-sdk)?:[a-zA-Z0-9_.-]+['|\"]",
    r"\b(?:implementation|api)\s+['|\"](?:cn|io)\.(?:agora|shengwang)\.rtm:iris-rtm(?:agora-)?(?:special-)?(?:full|voice)?(?:-preview|-sdk)?:[a-zA-Z0-9_.-]+['|\"]",
]

iOS_cdnRegex = [
    r"https://download.(?:agora|shengwang)[^\s]*iris[^\s]*_iOS[^\s]*\.zip",
    r"https://download.(?:agora|shengwang)[^\s]*Native_SDK_for_iOS[^\s]*\.zip",
]

windows_cdnRegex = [
    r"https://download.(?:agora|shengwang)[^\s]*iris[^\s]*_Windows[^\s]*\.zip",
    r"https://download.(?:agora|shengwang)[^\s]*Native_SDK_for_Windows[^\s]*\.zip",
    r"https://download.(?:agora|shengwang)[^\s]*windows_Preview[^\s]*\.zip",
]

mac_cdnRegex = [
    r"https://download.(?:agora|shengwang)[^\s]*iris[^\s]*_Mac[^\s]*\.zip",
    r"https://download.(?:agora|shengwang)[^\s]*Native_SDK_for_Mac[^\s]*\.zip",
    r"https://download.(?:agora|shengwang)[^\s]*macOS_Preview[^\s]*\.zip",
]

cocoapodsRegex = [
    r"pod\s*'(?:Shengwang|Agora)(?:IrisRTC|IrisRTM)?(?:_iOS|_macOS)(?:_Preview)?'\s*,\s*'[0-9a-zA-Z.-]+'(?!\s*,\s*:subspecs)",
    r"pod\s*'(?:Shengwang|Agora)(?:RtcEngine|Audio|Rtm)(?:_Special)?(?:_iOS|_macOS)(?:_Preview)?'\s*,\s*'[0-9a-zA-Z.-]+'(?!\s*,\s*:subspecs)",
    r"pod\s*'(?:ShengwangRtm|AgoraRtm)(?:_Preview)?'\s*,\s*'[0-9a-zA-Z.-]+'(?!\s*,\s*:subspecs)",
]

linux_cdnRegex = [
    r"https://download.(?:agora|shengwang)[^\s]*iris[^\s]*_Linux[^\s]*\.zip",
    r"https://download.(?:agora|shengwang)[^\s]*Native_SDK_for_Linux[^\s]*\.zip",
]

web_cdnRegex = [
    r"https://download.(?:agora|shengwang)[^\s]*iris-web[^\s]*\.js",
]

cdn_versionRegex = r'(\d+\.\d+\.\d+(?:\.\d+)?(?:-build\.\d+)?(?:-meeting\.\d+)?(?:-preview)?)'


def parse_content(input_string):
    platforms = ['iOS', 'macOS', 'Android', 'Windows', 'Linux', 'Web']
    result = []

    # Extract Cocoapods dependencies
    ios_dependencies = []
    iris_ios_dependencies = []
    macos_dependencies = []
    iris_macos_dependencies = []
    for pattern in cocoapodsRegex:
        found = re.findall(pattern, input_string)
        for match in found:
            if 'ios' in match.lower():
                if 'iris' in match.lower():
                    iris_ios_dependencies.append(match)
                else:
                    ios_dependencies.append(match)
            elif 'macos' in match.lower():
                if 'iris' in match.lower():
                    iris_macos_dependencies.append(match)
                else:
                    macos_dependencies.append(match)
            else:
                ios_dependencies.append(match)
                macos_dependencies.append(match)

    # Extract Maven dependencies
    maven_dependencies = []
    iris_maven_dependencies = []
    for pattern in mavenRegex:
        found = re.findall(pattern, input_string)
        for match in found:
            if 'iris' in match.lower():
                iris_maven_dependencies.append(match)
            else:
                maven_dependencies.append(match)

    # Extract CDN URLs
    cdn_urls = []
    for pattern in android_cdnRegex:
        found = re.findall(pattern, input_string)
        cdn_urls.append(found)

    for platform in platforms:
        platform_data = {
            'platform': platform,
            'cdn': [],
            'cocoapods': [],
            'maven': [],
            'iris_cocoapods': [],
            'iris_maven': [],
            'iris_cdn': [],
            'version': ''
        }

        if platform == 'Android':
            for pattern in android_cdnRegex:
                found = re.findall(pattern, input_string)
                for match in found:
                    if 'iris' in match.lower():
                        platform_data['iris_cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
                    else:
                        platform_data['cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
            platform_data['maven'] = maven_dependencies
            platform_data['iris_maven'] = iris_maven_dependencies

        if platform == 'iOS':
            for pattern in iOS_cdnRegex:
                found = re.findall(pattern, input_string)
                for match in found:
                    if 'iris' in match.lower():
                        platform_data['iris_cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
                    else:
                        platform_data['cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
            platform_data['cocoapods'] = ios_dependencies
            platform_data['iris_cocoapods'] = iris_ios_dependencies

        if platform == 'Windows':
            for pattern in windows_cdnRegex:
                found = re.findall(pattern, input_string)
                for match in found:
                    if 'iris' in match.lower():
                        platform_data['iris_cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
                    else:
                        platform_data['cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''

        if platform == 'macOS':
            for pattern in mac_cdnRegex:
                found = re.findall(pattern, input_string)
                for match in found:
                    if 'iris' in match.lower():
                        platform_data['iris_cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
                    else:
                        platform_data['cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
            platform_data['cocoapods'] = macos_dependencies
            platform_data['iris_cocoapods'] = iris_macos_dependencies

        if platform == 'Linux':
            for pattern in linux_cdnRegex:
                found = re.findall(pattern, input_string)
                for match in found:
                    if 'iris' in match.lower():
                        platform_data['iris_cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
                    else:
                        platform_data['cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''

        if platform == 'Web':
            for pattern in web_cdnRegex:
                found = re.findall(pattern, input_string)
                for match in found:
                    if 'iris' in match.lower():
                        platform_data['iris_cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
                    else:
                        platform_data['cdn'].append(match)
                        platform_data['version'] = re.search(cdn_versionRegex, match).group(0) or ''
        result.append(platform_data)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse input string for dependencies and CDN URLs.')
    parser.add_argument('input_string', type=str,
                        help='The input string to parse')

    args = parser.parse_args()

    parsed_data = parse_content(args.input_string)

    # Print the results to stdout
    print(json.dumps(parsed_data, indent=4))


# Example input string
# input_string = """
# # CDN
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_Android_rel.v4.1.2.139_68515_FULL_20250113_1950_524795.zip

# # IRIS
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Android_Video_20250122_0421_727.zip
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Android_Video_Standalone_20250122_0421_727.zip
# implementation 'io.agora.rtc:iris-rtc:4.3.2.11-meeting.1'
# https://download.agora.io/sdk/release/iris_2.2.2.1-build.1_RTM_Android_Video_Standalone_16K_20250116_0449_724.zip
# https://download.agora.io/sdk/release/iris_2.2.2.1-build.1_RTM_Android_Video_16K_20250116_0449_724.zip
# implementation 'io.agora.rtm:iris-rtm:2.2.2.1-build.1'

# # Maven
# api 'io.agora.rtc:full-sdk:4.5.0'
# api 'io.agora.rtc:voice-sdk:4.2.6'
# implementation 'io.agora.rtc:agora-full-preview:4.3.2.11'
# implementation 'io.agora.rtc:agora-special-voice:4.3.2.11'
# implementation 'io.agora.rtc:agora-special-full:4.3.2.11'
# implementation 'io.agora.rtc:full-screen-sharing:4.1.2.139'
# implementation 'io.agora.rtc:full-screen-sharing-special:4.3.2.11-meeting.1'
# implementation 'io.agora:agora-rtm:2.1.12'
# """

# input_string = """
# # CDN
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_Windows_v4.5.0_FULL.zip
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_Windows_rel.v4.2.6.153_27683_FULL_20241230_2024_503327.zip

# # IRIS
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Windows_Video_20250122_0421_597.zip
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Windows_Video_Standalone_20250122_0421_597.zip
# """

# input_string = """
# # CDN
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_Mac_rel.v4.2.6.154_23292_FULL_20250108_1705_516982.zip
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_Mac_v4.5.0_FULL.zip

# # IRIS
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Mac_Video_Standalone_20250122_0424_558.zip
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Mac_Video_20250122_0424_558.zip
# pod 'AgoraIrisRTC_macOS', '4.3.2.11-meeting.1'

# # Cocoapods
# pod 'AgoraRtcEngine_macOS_Preview', '4.3.2.11-meeting.1'
# pod 'AgoraRtcEngine_macOS', '4.3.2.11-meeting.1'
# pod 'AgoraRtcEngine_Special_macOS', '4.3.2.11-meeting.1'
# pod 'ShengwangRtcEngine_Special_macOS', '4.3.2.11-meeting.1'

# """

# input_string = """
# # CDN
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_iOS_v4.5.0_FULL.zip
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_iOS_v4.5.0_VOICE.zip
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_iOS_v4.5.0_LITE.zip

# # IRIS
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Mac_Video_Standalone_20250122_0424_558.zip
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Mac_Video_20250122_0424_558.zip
# pod 'AgoraIrisRTC_iOS', '4.3.2.11-meeting.1'
# pod 'AgoraIrisRTM_iOS', '4.3.2.11-meeting.1'
# # Cocoapods
# pod 'AgoraRtcEngine_iOS_Preview', '4.3.2.11-meeting.1'
# pod 'AgoraRtcEngine_iOS', '4.3.2.11-meeting.1'
# pod 'AgoraRtcEngine_Special_iOS', '4.3.2.11-meeting.1'
# pod 'AgoraAudio_Special_iOS', '4.3.2.11-meeting.1'
# pod 'AgoraAudio_iOS', '4.3.2.11-meeting.1'
# pod 'AgoraRtm_iOS', '4.3.2.11-meeting.1'
# """

# input_string = """
# # CDN
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_Linux_rel.v4.2.6.153_27683_FULL_20241230_2024_503327.zip
# https://download.agora.io/sdk/release/Agora_Native_SDK_for_Linux_v4.5.0_FULL.zip

# # IRIS
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Linux_Video_20250122_0421_597.zip
# https://download.agora.io/sdk/release/iris_4.3.2.11-meeting.1_DCG_Linux_Video_Standalone_20250122_0421_597.zip
# """
