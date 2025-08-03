import asyncio
import os
import sys

from browser_use.llm.openai.chat import ChatOpenAI

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
	sys.path.insert(0, project_root)

import pytest
from dotenv import load_dotenv

# Third-party imports
from browser_use import ActionResult, Agent, Controller

# Local imports
from browser_use.browser import BrowserProfile, BrowserSession

# Load environment variables.
load_dotenv()

# Initialize language model and controller.
llm = ChatOpenAI(model='gpt-4.1')
controller = Controller()



from browser_use import Agent, BrowserSession
from playwright.async_api import async_playwright

async def test_check_pw_with_LLM(playwright: async_playwright):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    browser_session = BrowserSession()
    agent = Agent(
        task="Open website https://playwright.dev",
        llm=llm,
        browser=browser,
        browser_session=browser_session
    )

    await agent.run()
    print(await agent.AgentOutput)
    print(await agent.message_manager.get_messages())
    print(await agent.get_model_output())
    await browser.close()

@controller.action('Open website')
async def open_website(url: str, browser_session: BrowserSession) -> ActionResult:
    # find matching existing tab by looking through all pages in playwright browser_context
    all_tabs = await browser_session.browser_context.pages
    for tab in all_tabs:
        if tab.url == url:
            await tab.bring_to_foreground()
            return ActionResult(extracted_content=f'Switched to tab with url {url}')
    # otherwise, create a new tab
    new_tab = await browser_session.browser_context.new_page()
    await new_tab.goto(url)
    return ActionResult(extracted_content=f'Opened new tab with url {url}')


from playwright.sync_api import sync_playwright

def test_check_pw_with_LLM_sync(playwright: sync_playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    browser_session = BrowserSession()
    agent = Agent(
        task="Open website https://playwright.dev",
        llm=llm,
        browser=browser,
        browser_session=browser_session
    )

    agent.run()
    # print(agent.AgentOutput)
    print(agent.message_manager.get_messages())
    print(agent.get_model_output())
    browser.close()
    
