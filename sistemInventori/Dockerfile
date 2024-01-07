FROM python:3.10

# where your code lives  
WORKDIR /app  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . ./

# run this command to install all dependencies  
RUN pip install -r requirements.txt  

# port where the Django app runs  
EXPOSE 8000  

# start server  
CMD python manage.py runserver 0.0.0.0:8000