from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from dotenv import load_dotenv

load_dotenv('/home/rich/Code/01_Ifes/03_TCC/.env')

MODEL: BaseChatModel = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0) # type: ignore