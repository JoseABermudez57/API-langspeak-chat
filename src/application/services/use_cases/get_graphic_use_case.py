from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import boto3
# from config.database import conn
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from src.application.dtos.responses.base_response import BaseResponse

load_dotenv()
bucket_name = os.getenv("AWS_BUCKET_NAME")
access_key = os.getenv("AWS_ACCESS_KEY")
secret_key = os.getenv("AWS_SECRET_KEY")
region = os.getenv("AWS_REGION")


class GetGraphicUseCase:
    def __init__(self, db):
        self.db = db
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def execute(self, user_uuid: str):
        # Query para obtener los datos desde la base de datos
        query = f"SELECT id, start_time, end_time FROM time_ia WHERE user_id = '{user_uuid}';"
        df = pd.read_sql(query, self.db.bind)

        # Convertir start_time y end_time a datetime
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])

        # Calcular la diferencia entre start_time y end_time en minutos
        df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60

        # Agrupar por fecha y sumar las duraciones
        df['date'] = df['start_time'].dt.date
        df_grouped = df.groupby('date')['duration'].sum().reset_index()

        # Crear una serie de tiempo
        df_grouped['date'] = pd.to_datetime(df_grouped['date'])
        df_grouped.set_index('date', inplace=True)
        df_grouped.sort_index(inplace=True)

        # Aplicar un modelo predictivo a la serie de tiempo
        model = ExponentialSmoothing(df_grouped['duration'], seasonal='add', seasonal_periods=7).fit()
        forecast = model.forecast(steps=7)

        # Guardar la serie de tiempo y las predicciones como una imagen
        plt.figure(figsize=(10, 5))
        plt.plot(df_grouped.index, df_grouped['duration'], label='Actual')

        # Crear un índice para los valores de forecast
        forecast_index = pd.date_range(start=df_grouped.index[-1], periods=7, freq='D')
        plt.plot(forecast_index, forecast, label='Forecast', linestyle='--')

        plt.title('Time Series of Chat Duration')
        plt.xlabel('Date')
        plt.ylabel('Duration (minutes)')
        plt.legend()

        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        image_path = f"{current_time}_timeseries.png"

        plt.savefig(image_path)

        # Subir la imagen a S3
        s3_key = f"timeseries/{image_path}"

        self.s3_client.upload_file(image_path, bucket_name, s3_key,
                              ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'})

        # Generar la URL pública de la imagen
        url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_key}"

        # Eliminar la imagen local después de subirla a S3
        os.remove(image_path)

        return BaseResponse(data={"url": url},
                            status_code=200,
                            message="Get graphic successfully",
                            success=True,
                            http_status="OK")
