# IP address script

>Module that handles ip addresses, adding, deleting...


# IPHandler 

``` python 
 class IPHandler(file=default_path, with_port=True) 
```

Documentation to IPHandler.

This class handles ip address storing and retrieving them
from a txt file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     file | str |         (optional argument)        Text (.txt) file full path where the ip address must be stored. | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| set_path | Sets the path to the file. | 
| create_ipa_file | Creates an empty file for storing ip addresses. | 
| erase_ipa_file | Function for erasing the filestoring ip addresses. | 
| add_ip | Adds ip address to the given file. | 
| remove_ip | Removes ip address to the given file. | 
| ip_is_in_file | Looks up an ip address in the given file. | 
| valid_ipv4 | Looks up an ip address in the given file. | 
| get_ip_listdef | Gets the list of all the ip address in the file. | 
| add_ip_list | Adds list of ip address to the given file. | 
 
 

### set_path

``` python 
    set_path(path) 
```


Sets the path to the file.

### create_ipa_file

``` python 
    create_ipa_file() 
```


Creates an empty file for storing ip addresses.

If there is already an existing file then it just leaves it as
it is. It does not erase the content already existing. For that
is the erase file.

### erase_ipa_file

``` python 
    erase_ipa_file() 
```


Function for erasing the filestoring ip addresses.

### add_ip

``` python 
    add_ip(ip_address, with_port=True) 
```


Adds ip address to the given file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         ip_address | str |             string containing a valid ip address | 
|         with_port | bool |             boolean specifying if the ip address must include            port number to be valid or not | 


### remove_ip

``` python 
    remove_ip(ip_address) 
```


Removes ip address to the given file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         ip_address | str |             string containing a valid ip address | 


### ip_is_in_file

``` python 
    ip_is_in_file(ip_address) 
```


Looks up an ip address in the given file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         ip_address | str |             string containing a valid ip_address | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         is_in | bool |             True if the ip address is in the given file.            False otherwise | 


### valid_ipv4

``` python 
    valid_ipv4(ip_address, with_port=True) 
```


Looks up an ip address in the given file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         ip_address | str |             string to be check | 
|         with_port | bool |             boolean specifying if the ip address must include            port number to be valid or not | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         valid | bool |             True if the ip address is valid (4 numbers            separated by . between 0-255 and integer after colon            in case of with_port being true).            False otherwise | 


### get_ip_listdef

``` python 
    get_ip_listdef() 
```


Gets the list of all the ip address in the file.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         ips | list |             a list containing all ip addresses (str) | 


### add_ip_list

``` python 
    add_ip_list(ip_list) 
```


Adds list of ip address to the given file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         ip_list | str list |             list containing valid ip addresses | 
|         with_port | bool |             boolean specifying if the ip address must include port            number to be valid or not | 
