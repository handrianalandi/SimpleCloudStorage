# Simple Cloud Storage<hr />

a simple cloud storage service that able to :<br>
upload a file (locally)<br>
download a file (locally)<br>
share file between user (locally)<br><br>
this project also implement session, user must logged in in order to use the service<br><br>
please kindly look at the documentation about how the service works :https://documenter.getpostman.com/view/13165507/UzBiRV5B


## login<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/login<br />  
> ### Request <br /> 
 ```
Request Body:
{
    "username":"han",
    "password":"han123"
}
``` 
<br />

> ### Response
**login**<br />``` Status Code: 200 OK```<br />
```
Response Body:
Welcome han
``` 
<hr /> 

## logout<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/logout<br />  

<br />

> ### Response
**logout**<br />``` Status Code: 200 OK```<br />
```
Response Body:
Successfully Logged out from han
``` 
<hr /> 

## register<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/register<br />  
> ### Request <br /> 
 ```
Request Body:
{
    "username":"han1",
    "password":"han123"
}
``` 
<br />

> ### Response
**register exist**<br />``` Status Code: 200 OK```<br />
```
Response Body:
Register Failed, Username already exist!
``` 
**register success**<br />``` Status Code: 200 OK```<br />
```
Response Body:
Register Success!, Welcome han1
``` 
<hr /> 

## upload<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/upload<br />  

<br />

> ### Response
**upload**<br />``` Status Code: 200 OK```<br />
```
Response Body:
Upload Success!
``` 
<hr /> 

## get file<br /> 
```GET```&nbsp;&nbsp;&nbsp;localhost:8000/files<br />  

<br />

> ### Response
**get file**<br />``` Status Code: 200 OK```<br />
```
Response Body:
{
    "your_files": [
        "Cat03.jpg"
    ],
    "shared_files": []
}
``` 
**get file with shared files**<br />``` Status Code: 200 OK```<br />
```
Response Body:
{
    "your_files": [
        "X-Jenis-Olahraga-Menyenangkan-untuk-Anjing-Peliharaan.jpg",
        "1545111808_contoh-pdf.pdf"
    ],
    "shared_files": [
        "Cat03.jpg"
    ]
}
``` 
<hr /> 

## share file<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/share<br />  
> ### Request <br /> 
 ```
Request Body:
{
    "file_id":"20",
    "user_destination_id":"2"
}
``` 
<br />

> ### Response
**share file**<br />``` Status Code: 200 OK```<br />
```
Response Body:
File share success
``` 
**share file (file not belong to you)**<br />``` Status Code: 200 OK```<br />
```
Response Body:
File not belong to user_origin
``` 
**share file (user destination not exist)**<br />``` Status Code: 200 OK```<br />
```
Response Body:
User_destination not exist
``` 
<hr /> 

## download<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/download<br />  
> ### Request <br /> 
 ```
Request Body:
{
    "file_id":"23"
}
``` 
<br />

> ### Response
**download**<br />``` Status Code: 200 OK```<br />
```
Response Body:
File not belong to user
``` 
<hr /> 


