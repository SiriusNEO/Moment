

class BrowserManager:
    
    """
        width
        height
        
        pw
        browser
        context
        page
    """

    def __init__(self, pw, width, height):
        self.width = width
        self.height = height
        self.pw = pw

    async def __aenter__(self):
        self.browser = await self.pw.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            viewport={'width': self.width, 'height': self.height}, 
            device_scale_factor=1.5
        )
        self.page = await self.context.new_page()
        return self.page

    async def __aexit__(self, type, value, trace):
        await self.page.close()
        await self.context.close()
        await self.browser.close()



