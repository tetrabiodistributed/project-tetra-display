from behave import fixture
from selenium import webdriver


@fixture
def browser_chrome(context, timeout=30, **kwargs):
    opts = webdriver.ChromeOptions()
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--headless')
    context.browser = webdriver.Chrome(options=opts)
    yield context.browser
    context.browser.close()


def use_fixture_by_tag(tag, context, fixture_registery):
    fixture_data = fixture_registry.get(tag, None)
    if fixture_data is None:
        raise LookupError(f"Unknow fixture tag: {tag}")
    return use_fixture(fixture_data, context)
