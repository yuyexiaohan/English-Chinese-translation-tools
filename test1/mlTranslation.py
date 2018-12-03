SecretId = "AKIDkLoCSYPchcMvMhL01ylNo7I5Jk7JLCxY"
SecretKey = "c5FzaDqRs8ECzbaTGFSXXM3jHj3Cg2GJ"

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import json
try:

    while True:
        inputData = input("请输入要翻译的内容：") # str

        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile ()
        httpProfile.endpoint = "tmt.ap-shanghai.tencentcloudapi.com"
        # client = tmt_client.TmtClient(cred, "ap-shanghai")
        clientProfile = ClientProfile ()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient (cred, "ap-shanghai", clientProfile)

        # 进行语种识别
        req = models.LanguageDetectRequest() # 初始化一个语言识别类型实例
        '''
            Text	是	String	待识别的文本
            ProjectId	是	Integer	项目id
        '''
        params = """{
            "Text": "%s",
            "ProjectId": "%s"
        }"""%(inputData, 1)
        # print('......' ,params, '......')
        req.from_json_string (params)

        resp = client.LanguageDetect (req)
        # print('......' ,resp, type(resp), '......')
        # resp： {"Lang": "en", "RequestId": "138f27c7-0aa9-4361-815e-f64d626077a7"}
        # type(resp)：<class 'tencentcloud.tmt.v20180321.models.LanguageDetectResponse'>

        # 进行英汉互译
        fromLang = json.loads(resp.to_json_string())["Lang"] # en
        # print ('......', json.loads(resp.to_json_string()), '......', fromLang, '......')
        # {'Lang': 'en', 'RequestId': 'aeaaf5da-955f-4bd7-a8ea-04797e5e7a11'}

        toLang = None
        if fromLang == "en":
            toLang = "zh"
        elif fromLang == "zh":
            toLang = "en"
        else:
            print("请输入英文或者中文，本软件暂不支持其他语言的翻译！")

        if toLang:
            req = models.TextTranslateRequest() # 初始化一个文本翻译类型实例

            '''
                SourceText	是	String	待翻译的文本
                Source	是	String	源语言，参照Target支持语言列表
                Target	是	String
                ProjectId	是	Integer	项目id
            '''
            params1 = """{
                "SourceText": "%s",
                "Source": "%s",
                "Target": "%s",
                "ProjectId": 1
            }"""%(inputData, fromLang, toLang)

            req.from_json_string(params1)

            resp = client.TextTranslate(req)

            print(json.loads(resp.to_json_string())["TargetText"])

except TencentCloudSDKException as e:
    print(e)