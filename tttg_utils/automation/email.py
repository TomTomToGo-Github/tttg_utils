from tttg_utils.automation.selenium import setup_driver

def send_email(sender, receiver, msg, provider_url=None, sender_pwd=None, subject=None, cc=None, bc=None, browser_name=None, browser_driver_path=None, headless=False):
    """NOT IMPLEMENTED YET

    Args:
        sender (_type_): _description_
        receiver (_type_): _description_
        msg (_type_): _description_
        provider_url (_type_, optional): _description_. Defaults to None.
        sender_pwd (_type_, optional): _description_. Defaults to None.
        subject (_type_, optional): _description_. Defaults to None.
        cc (_type_, optional): _description_. Defaults to None.
        bc (_type_, optional): _description_. Defaults to None.
        browser_name (_type_, optional): _description_. Defaults to None.
        browser_driver_path (_type_, optional): _description_. Defaults to None.
        headless (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    print("NOT IMPLEMENTED YET")
    # if not browser_name:
    #     browser_name = "edge"  # 'edge' or 'chrome'
    # driver = setup_driver(browser_name, browser_driver_path, headless, url=provider_url)
    # if not sender_pwd:
    #     sender_pwd = input("Sending email - Type your password and press enter: ")
    # return driver