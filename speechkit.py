import requests
from os import system
import time
import json


class recognizeShortAudio:
    def __init__(self, key):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        data = {"yandexPassportOauthToken": key}
        answer = requests.post(url, json=data)

        # print(answer.json()['iamToken'])
        self.token = answer.json()['iamToken']


    def recognize(self, file, folder):
        url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?folderId={}".format(folder)
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }

        answer = requests.post(url, data=open(file, 'rb').read(), headers=headers)

        if answer.status_code != 200:
            raise Exception("It's error with recognizing: {}".format(response.json()))
        else:
            return answer.text


def recode (inputfile, outputfile):
    """Recodering file using ffmpeg

    :param inputfile: string, path to input file
    :param outputfile: string, path to output file
    """

    cmd = "ffmpeg -i '" + str(inputfile) + "' '" + str(outputfile) + "'"
    out = system(cmd)
    return out

def removefile(inputfile):
    """Removes file

    :param inputfile: string, path to input file
    """

    cmd = "rm '" + str(inputfile) + "'"
    out = system(cmd)
    return out

class objectStorage:
    def __init__ (self, aws_access_key_id, aws_secret_access_key):
        """Starting ssesion with boto3 to access objectStorage

        :param aws_access_key_id: string
        :param aws_secret_access_key: string
        """

        import boto3
        # system("cd ~")
        # system("mkdir .aws")
        # system("echo '[default] \nregion=ru-central1' > .aws/config")
        # system("echo '[default] \naws_access_key_id = {} \naws_secret_access_key = {}' > .aws/credentials".format(aws_access_key_id, aws_secret_access_key))
        session = boto3.session.Session()
        self.s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )

    def upload_file(self, inputfilepath, baketname, outputfilename):
        """Upload a file to object storage

        :param inputfilepath: string, path to input file
        :param baketname: string
        :param outputfilename: string, name of file in object storage
        """

        return self.s3.upload_file(inputfilepath, baketname, outputfilename)


    def listObjectsInBucket(self, bucketname):
        return self.s3.list_objects(Bucket=bucketname)


    def deleteObject(self, object_name, bucketname):
        return self.s3.delete_objects(Bucket=bucketname, Delete={'Objects': [{'Key': object_name}]})


    def create_presigned_url(self, bucket_name, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        try:
            response = self.s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response


class recognizeLongAudio:
    def __init__(self, apiKey):
        """Initialize apiKey for recognizing long audio

        :param apiKey: string
        """

        self.apiKey = apiKey
        self.header = {'Authorization': 'Api-Key {}'.format(self.apiKey)}


    def recognize_post(self, filelink):
        """POST request to recognize long audio

        :param filelink: string
        """

        POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"
        body ={
            "config": {
                "specification": {
                    "languageCode": "ru-RU"
                }
            },
            "audio": {
                "uri": filelink
            }
        }
        req = requests.post(POST, headers=self.header, json=body)
        data = req.json()
        print(data)

        self.id = data['id']


    def ready_request(self, u):
        GET = "https://operation.api.cloud.yandex.net/operations/{id}"
        req = requests.get(GET.format(id=self.id), headers=self.header)
        req = req.json()
        self.req = req
        return req['done']


    def return_json(self):
        return self.req


    def return_text(self):
        strr = ''
        for chunk in self.req['response']['chunks']:
            strr = strr + str(chunk['alternatives'][0]['text'])
        return strr