from requests import get
from .Settings import Settings

HeadersToAuth = {
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': f'Basic {Settings.ApiKeyBase64}'
    }

class GetRootFolder: 

    def GetSubscriptionId() -> str:
        GetSubscriptionIdLink = "https://fastreport.cloud/api/manage/v1/Subscriptions"
        SubscriptionsResponse = get(url=GetSubscriptionIdLink,
                                    headers = HeadersToAuth)
        if SubscriptionsResponse.status_code == 200:
            SubscriptionsResponseJson = SubscriptionsResponse.json()
            SubscriptionId = SubscriptionsResponseJson['subscriptions'][0]['id']
            return SubscriptionId
        else: return "False"

    def GetFolderId(Link: str) -> str:
        FolderResponse = get(url=Link,
                             headers=HeadersToAuth)
        if FolderResponse.status_code == 200:
            return FolderResponse.json()['id']
        else:
            return "False"
        
    # Folder Id in FileSystem
    SubscriptionId = GetSubscriptionId()
    TemplatesRootFolderId = GetFolderId(
        f"https://fastreport.cloud/api/rp/v1/Templates/Root?subscriptionId={SubscriptionId}")
    ReportRootId = GetFolderId("https://fastreport.cloud/api/rp/v1/Templates/Root")
    ReportsRootFolderId = GetFolderId("https://fastreport.cloud/api/rp/v1/Reports/Root")
    ReportHeaders = {
        'accept': 'text/plain',
        'Content-Type': 'application/json-patch+json',
        'Authorization': f'Basic {Settings.ApiKeyBase64}'
        }