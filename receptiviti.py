import boto3
import time

## the following textract APIs are used: start_document_text_detection, get_document_text_detection
def InvokeTextDetectJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract')
    response = client.start_document_text_detection(
            DocumentLocation={
                      'S3Object': {
                                    'Bucket': receptiviti/pdf/,
                                    'Name': sample.pdf
                                }
           })
    ## jobid from AWS
    return response["JobId"]

## check if job is complete, sleep or return
def CheckJobComplete(jobId):
    time.sleep(5)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return status

## take json and put in array, cycle through next page tokens
def JobResults(jobId):
    pages = []
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
 
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']
        while(nextToken):
            response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
            pages.append(response)
            print("Resultset page recieved: {}".format(len(pages)))
            nextToken = None
            if('NextToken' in response):
                nextToken = response['NextToken']
    return pages

# S3 bucket and document
s3BucketName = "receptiviti/pdf"
documentName = "sample.pdf"

# copied this to get output
jobId = InvokeTextDetectJob(s3BucketName, documentName)
print("Started job with id: {}".format(jobId))
if(CheckJobComplete(jobId)):
    response = JobResults(jobId)
    for resultPage in response:
        for item in resultPage["Blocks"]:
            if item["BlockType"] == "LINE":
                print ('\033[94m' + item["Text"] + '\033[0m')
