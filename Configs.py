import configparser
config_file = configparser.ConfigParser()
config_file["access_token"] = {
        "token": 'vk1.a.FOPeogRotD8mxzUyIs1li1ENNH19zPZRy1nWnJHcR8Bj6nHOQSyraeCCtgNEJbZc4a1ZZVaAQVq7TYIM37R-VIKGMJ59PBLMbodtOhflLfv_r7iPM8R0DZukNT6fe6fCqu_oBnUXz0v_v25EgT9z_ofRhJfBq1Oeub81djXC0cs6dINYLX3OJ5OSUDCXQTCv'
        }
with open("person.ini", "w") as file_object:
    config_file.write(file_object)
print("Config file 'person.ini' created")
read_file = open("person.ini", "r")
content = read_file.read()
print("content of the config file is:")
print(content)