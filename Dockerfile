FROM python:3.12

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt


# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONPATH=/code/src

# 
COPY ./src  /code/src

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]