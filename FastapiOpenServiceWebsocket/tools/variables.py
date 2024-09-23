import datetime
import os
import sys
import oss2

CONF = {}
OSS = None


def set_conf(config_path):
    import configparser
    global CONF

    # 解析配置文件
    CONF = configparser.ConfigParser()
    CONF.read(config_path, encoding='utf-8')
    return CONF


def get_conf():
    global CONF  # 声明sessions为全局变量
    return CONF


def get_oss():
    global OSS
    return OSS


# 检查输入时间是否为%Y-%m-%d %H:%M:%S格式
def check_datetime(str_time):
    try:
        _ = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False


def set_oss():
    class AliOssControl:
        def __init__(self, access_key_id, access_key_secret, endpoint, region, bucket_name):
            # 使用获取的RAM用户的访问密钥配置访问凭证
            auth = oss2.AuthV4(access_key_id, access_key_secret)
            # 形成bucket对象
            self.bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)

        # 获取bucket相关数据信息
        def show_bucket(self):
            # 获取Bucket相关信息。
            bucket_info = self.bucket.get_bucket_info()
            # 获取Bucket名称。
            print('name: ' + bucket_info.name)
            # 获取Bucket存储类型。
            print('storage class: ' + bucket_info.storage_class)
            # 获取Bucket创建时间。
            print('creation date: ' + bucket_info.creation_date)
            # 获取Bucket内网Endpoint。
            print('intranet_endpoint: ' + bucket_info.intranet_endpoint)
            # 获取Bucket外网Endpoint。
            print('extranet_endpoint ' + bucket_info.extranet_endpoint)
            # 获取拥有者信息。
            print('owner: ' + bucket_info.owner.id)
            # 获取Bucket读写权限ACL。
            print('grant: ' + bucket_info.acl.grant)
            # 获取容灾类型。
            print('data_redundancy_type:' + bucket_info.data_redundancy_type)
            # 获取Bucket的访问跟踪状态。仅Python SDK 2.16.1及以上版本支持获取访问跟踪状态。
            print('access_monitor:' + bucket_info.access_monitor)
            # 获取存储空间的统计信息。
            result = self.bucket.get_bucket_stat()
            # 获取Bucket的总存储量，单位为GB。
            print('all_storage_size', round(result.storage_size_in_bytes / 1024 / 1024, 2), 'GB')
            # 获取Bucket中总的Object数量。
            print('all_object_num', result.object_count)

        # 创建目录
        def create_root(self, root_path):
            self.bucket.put_object(f'{root_path}/', '')

        # 清空并删除文件夹
        def delete_root(self, root_path):
            for obj in oss2.ObjectIterator(self.bucket, prefix=root_path):
                self.bucket.delete_object(obj.key)

        # 上传文件
        def upload_file(self, save_path, file_path=None):
            # 必须以二进制的方式打开文件。
            # 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
            with open(save_path, 'rb') as fileobj:
                content = fileobj.read()

                # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
                if file_path:
                    file_name = file_path
                else:
                    file_name = os.path.basename(save_path)

                # 不指定x-oss-forbid-overwrite时，默认覆盖同名Object。
                # 指定x-oss-forbid-overwrite为false时，表示允许覆盖同名Object。
                # 指定x-oss-forbid-overwrite为true时，表示禁止覆盖同名Object，如果同名Object已存在，程序将报错。
                headers = {'x-oss-forbid-overwrite': 'true'}
                try:
                    self.bucket.put_object(file_name, content, headers=headers)
                    return True
                except Exception as e:
                    print(e)
                    return False

        # 上传文件流
        def upload_file_seek(self, file_seek, file_path):
            # 不指定x-oss-forbid-overwrite时，默认覆盖同名Object。
            # 指定x-oss-forbid-overwrite为false时，表示允许覆盖同名Object。
            # 指定x-oss-forbid-overwrite为true时，表示禁止覆盖同名Object，如果同名Object已存在，程序将报错。
            headers = {'x-oss-forbid-overwrite': 'true'}
            try:
                self.bucket.put_object(file_path, file_seek, headers=headers)
                return True
            except Exception as e:
                print(e)
                return False

        # 展示目录文件列表
        def show_file_list(self, root_path=None):
            objs = []
            if root_path:
                for obj in oss2.ObjectIterator(self.bucket, prefix=root_path):
                    objs.append(obj.key)

            else:
                # 列举Bucket下的所有文件。
                for obj in oss2.ObjectIterator(self.bucket):
                    objs.append(obj.key)

            return objs

        # 文件存在检查
        def exist_file(self, file_path):
            exist = self.bucket.object_exists(file_path)
            # 返回值为true表示文件存在，false表示文件不存在。
            if exist:
                return True
            else:
                return False

        # 含进度条的文件本地下载功能
        def download_file(self, file_path, save_path):
            def percentage(consumed_bytes, total_bytes):
                if total_bytes:
                    rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
                    # rate表示下载进度。
                    print('\r{0}% '.format(rate), end='')

                    sys.stdout.flush()

            # progress_callback是可选参数，用于实现进度条功能。
            self.bucket.get_object_to_file(file_path, save_path, progress_callback=percentage)

        # 拉取文件stream流
        def pull_file_stream(self, file_path):
            object_stream = self.bucket.get_object(file_path)
            return object_stream

        # 删除文件
        def delete_file(self, file_path):
            self.bucket.delete_object(file_path)

    global OSS
    global CONF

    # 从配置文件中获取Access Key ID和Access Key Secret
    global_conf = CONF['oss']
    access_key_id = global_conf['alibaba_cloud_access_key_id']
    access_key_secret = global_conf['alibaba_cloud_access_key_secret']
    endpoint = global_conf['endpoint']
    region = global_conf['region']
    bucket_name = global_conf['bucket_name']

    OSS = AliOssControl(access_key_id, access_key_secret, endpoint, region, bucket_name)
