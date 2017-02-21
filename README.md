# ADS

#Part 2: Dockerize this pipeline 

* Checking Version
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

#Pushing Image to DockerHub
taj@taj-pc MINGW64 /c/adsrepo/notebooks_docker (master)
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: pptaj
Password:
Login Succeeded

#Listing Images
taj@taj-pc MINGW64 /c/adsrepo/notebooks_docker (master)
$ docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
part                          latest              fcf47e0746e7        22 minutes ago      816.7 MB
pptaj/ads                     latest              fcf47e0746e7        22 minutes ago      816.7 MB
ads                           latest              90c953ab3985        54 minutes ago      690.3 MB
<none>                        <none>              b54f3186162b        About an hour ago   726.6 MB
<none>                        <none>              cece5bb77ad0        4 hours ago         3.984 MB
python                        3                   3984f3aafbc9        11 days ago         690.3 MB
nginx                         latest              cc1b61406712        3 weeks ago         181.8 MB
ubuntu                        latest              f49eec89601e        4 weeks ago         129.5 MB
hello-world                   latest              48b5124b2768        5 weeks ago         1.84 kB
alpine                        latest              88e169ea8f46        7 weeks ago         3.984 MB
ipython/ipython               3.x                 2c1c04a96877        11 months ago       816.7 MB
dataquestio/python3-starter   latest              3cccab0c85e2        14 months ago       1.796 GB

taj@taj-pc MINGW64 /c/adsrepo/notebooks_docker (master)
$ docker push pptaj/ads:latest
The push refers to a repository [docker.io/pptaj/ads]
75ce99ae9ea6: Pushing [==============================================>    ] 29.01 MB/31.28 MB
9953fb688ad8: Pushing [=================>                                 ] 14.02 MB/40.15 MB
89781da60c2a: Pushed
06cd93119a0b: Pushed
82ecd3afe058: Pushed


