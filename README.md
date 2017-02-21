# ADS

#Part 2: Dockerize this pipeline 

*Checking Version
taj@taj-pc MINGW64 /c/adsrepo/notebooks_docker (master)
$ docker version
Client:
 Version:      1.12.6
 API version:  1.24
 Go version:   go1.6.4
 Git commit:   78d1802
 Built:        Wed Jan 11 00:23:16 2017
 OS/Arch:      windows/amd64

Server:
 Version:      1.13.0
 API version:  1.25
 Go version:   go1.7.3
 Git commit:   49bf474
 Built:        Wed Jan 18 16:20:26 2017
 OS/Arch:      linux/amd64

#Editing Dockerfile
 taj@taj-pc MINGW64 /c/adsrepo/notebooks_docker (master)
$ vim Dockerfile
FROM python:3
ADD Part1Latest.ipynb /
CMD ["python", "./Part1Latest.ipynb"]

#Creating Docker Image
taj@taj-pc MINGW64 /c/adsrepo/notebooks_docker (master)
$ docker build -t ads .
Sending build context to Docker daemon 8.192 kB
Step 1/3 : FROM python:3
 ---> 3984f3aafbc9
Step 2/3 : ADD Part1Latest.ipynb /
 ---> fdfd7e8f4342
Removing intermediate container d6ab9a7a99cd
Step 3/3 : CMD python ./Part1Latest.ipynb
 ---> Running in a90c73f669a4
 ---> 90c953ab3985
Removing intermediate container a90c73f669a4
Successfully built 90c953ab3985
SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. All files and directories added to build context will have '-rwxr-xr-x' permissions. It is recommended to double check and reset permissions for sensitive files and directories.

#Image Created
taj@taj-pc MINGW64 /c/adsrepo/notebooks_docker (master)
$ docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED              SIZE
ads                           latest              90c953ab3985        About a minute ago   690.3 MB
