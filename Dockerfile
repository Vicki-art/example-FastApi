#The isntruction was taken from https://hub.docker.com/_/python.
# where "python" is a pictire name and 3.9.7 - is a version tag. 

FROM python:3.9.7 

WORKDIR /usr/src/app

COPY requirenments.txt ./

#Install all dependencies - the longest step 
RUN pip install --no-cache-dir -r requirenments.txt

COPY . . 

#This instructions are to be implemented step by step and cached.
#So if we will change the source code the 4 cached operations will be taken from the cache 
#And we only need to rerun the fifth operation. 
#This is one of the most impirtant features. 


#Mention the app launchong command 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


