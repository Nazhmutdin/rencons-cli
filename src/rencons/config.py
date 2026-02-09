from os import environ

from dotenv import load_dotenv

load_dotenv()

class CliConfig:
    @classmethod
    def API_ID(cls): 
        return int(environ["API_ID"])
    
    @classmethod
    def API_HASH(cls): 
        return environ["API_HASH"]
