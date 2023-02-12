from datetime import datetime
import json

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
import pendulum
import requests

from mgf_imoveis import crawler

@dag(
    schedule=None,
    dag_id='crawlers_real_estate',
    description="Raspagem de dados de sites de imobiliarias",
    catchup=False,
    start_date=pendulum.datetime(2023, 2, 7, tz="America/Sao_Paulo"),
    tags=['raw', '2_daily']
)
def get_data_real_estate():
    """
    ### Get data Real Estate
    Essa dag é responsável por raspar os dados de imovies e salva-los
    na camada raw do data lake.
    """
    # @task.virtualenv(
    #     task_id="virtualenv_python", requirements=["requests", "beautifulsoup4"], system_site_packages=False
    # )
    @task()
    def get_data_mgf_imoveis():
        """
        ### Get data MgfImoveis task 
        Recupera informações do site da MgfImoveis.
        """
        re_list = crawler()
        dt_now = pendulum.now("America/Sao_Paulo").strftime('%Y-%m-%d %H:%M:%S')
        if re_list != []:
            for real_estate in re_list:
                real_estate['created_date'] = dt_now
            return re_list
        else:
            return [None]
    
    @task.virtualenv(
        task_id="put_raw_minio", requirements=["minio", "pendulum"], system_site_packages=False
    )
    def put_raw_minio(re_list: list):
        """
        ### Put raw MinIo
        Salva informações do crawler na primeira camada do lake.
        """
        import io
        import json
        import os
        import uuid

        from minio import Minio
        import pendulum

        dt_now = pendulum.now("America/Sao_Paulo").strftime('%Y-%m-%d')
        file_path = f'mgf_crawler/{dt_now}/{uuid.uuid4()}.json'

        data_bytes = json.dumps(re_list).encode('utf-8')

        minio_client = Minio(os.environ["MINIO_URL_API"],
               access_key=os.environ["MINIO_ACCESS_KEY"],
               secret_key=os.environ["MINIO_SECRET_KEY"],
               secure=False
               )

        # Create destination bucket if it does not exist
        if not minio_client.bucket_exists(os.environ["MINIO_RAW_BUCKET"]):
            minio_client.make_bucket(os.environ["MINIO_RAW_BUCKET"])
            print("Destination Bucket '%s' has been created" % (os.environ["MINIO_RAW_BUCKET"]))
        else:
            print(f"Bucket {os.environ['MINIO_RAW_BUCKET']} already exists!")

        minio_client.put_object(
            bucket_name = os.environ["MINIO_RAW_BUCKET"],
            object_name = file_path,
            data=io.BytesIO(data_bytes),
            length=len(data_bytes),
            content_type='application/json')
        print("- Uploaded processed object '%s' to Destination Bucket '%s'" % (file_path, os.environ["MINIO_RAW_BUCKET"]))

    real_estates = get_data_mgf_imoveis()
    put_raw_minio(real_estates)
get_data_real_estate()