from config import AWS_FILES_BUCKET_NAME
from helpers import s3_connect

def check_user_folder(user_id):
    s3 = s3_connect()
    folder_prefix = f'{user_id}/'
    response = s3.list_objects_v2(Bucket=AWS_FILES_BUCKET_NAME, Prefix=folder_prefix)
    if "Contents" not in response:
        # Pasta não existe, então criar:
        s3.put_object(Bucket=AWS_FILES_BUCKET_NAME, Key=folder_prefix)


def upload_file(file_obj, bucket_name, path, file_name, user_id=None):
    if user_id:
        check_user_folder(user_id)
        s3 = s3_connect()
        try:
            s3.upload_fileobj(
                file_obj,
                bucket_name,
                user_id + path + file_name
            )

        except Exception as e:
            print("Aconteceu algo: ", e)
            return False, e

    else:
        s3 = s3_connect()
        try:
            s3.upload_fileobj(
                file_obj,
                bucket_name,
                path + file_name
            )

        except Exception as e:
            print("Aconteceu algo: ", e)
            return False, e

    return True, file_name


def delete_file(user_id, filename, path):
    s3 = s3_connect()
    try:
        s3.delete_object(Bucket=AWS_FILES_BUCKET_NAME, Key=f"{user_id}/{path}/{filename}")
    except Exception as e:
        print("Aconteceu algo: ", e)
        return False

    return True

def gen_s3_uri(bucket_name, filename, path):
    s3 = s3_connect()
    try:
        url = s3.generate_presigned_url("get_object", Params = {"Bucket": bucket_name, "Key": path+filename},
                                        ExpiresIn=3600)
    except Exception as e:
        print("Aconteceu algo: ", e)
        return None

    return url