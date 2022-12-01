from boto.s3.connection import S3Connection

region_name = 'sa-east-1'
aws_access_key_id = 'AKIAZUYHWTZ2MDHCZHO6'
aws_secret_access_key = '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'



if __name__ == '__main__':
    conn = S3Connection(aws_access_key_id, aws_secret_access_key)
    print(conn.get_bucket('grupo3-prisma').get_key('datasets'))