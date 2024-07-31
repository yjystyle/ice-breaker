from typing import Tuple
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import Summary, summary_parser

def ice_break_with(name:str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    print(f'linkedin_username: {linkedin_username}')
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url) 

    summary_template = """
        given the Linkedin information {information} about a person I want you to create:
        1. A short summary
        2. Two interesting facts about them

        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")

    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain = summary_prompt_template | llm | summary_parser
    # linkedin_data = scrape_linkedin_profile(
    #     linkedin_profile_url="https://www.linkedin.com/in/eden-marco/", mock=True
    # )
    res:Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name="강정현 ktds" )

   

    # async for chunk in chain.astream({'topic': 'colors'}):
    #     print('-')  # noqa: T201
    #     print(chunk, sep='', flush=True)  # noqa: T201
