---
title: Maui最佳实践之 Http请求
date: 2024-8-15 23:20:11 +0800
categories: [maui]
tags: [maui, xaml, c#]     # TAG names should always be lowercase
---



## 功能说明

1. 应用中应该对网络访问无感，即封装httpclient
2. 对请求根据业务进行分类，并封装配置过程



## HttpClient

httpClient 是 .net 系统库提供的网络访问类。

可以创建一个 httpClient 然后，使用 Get、Post 等方法访问 Uri

HttpClient还接受一个消息处理器 HttpMessageHandler，用来进行基本配置。

[HttpClient-官方文档](https://learn.microsoft.com/zh-cn/dotnet/api/system.net.http.httpclient?view=net-8.0)

[HttpMessageHandler-官方文档](https://learn.microsoft.com/zh-cn/dotnet/api/system.net.http.httpclienthandler?view=net-8.0)



## 封装提供网络请求的服务

这里使用“单例模式”对httpclient进行封装。虽然官方提供了工厂方法`HttpClientFactory`，但该方案只适用于无状态短期的http请求。对于客户端应用来说，这样做可能导致频繁创建httpclient，进而导致系统套接字资源耗尽。



### RequestProvider 请求构造器

以下构造器接口，支持Token验证和设备验证。以及自定义请求头等功能。

```c#
public interface IRequestProvider{
  Task<TResult> GetAsync<TResult>(string uri, string token="");
  Task<TResult> PostAsync<TResult, TResponse>(string ur, TRequest data, string token="", string header="");
  
  Task<bool> PostAsync<TRequest>(string uri, TRequest data, string token = "", string header = "");

  Task<TResult> PostAsync<TResult>(string uri, string data, string clientId, string clientSecret);

  Task<TResult> PutAsync<TResult>(string uri, TResult data, string token = "", string header = "");

  Task DeleteAsync(string uri, string token = "");
}
```

httpClient 使用懒加载单例模式

```c#
public class RequestProvider(HttpMessageHandler _messageHandler) : IRequestProvider{
  // 单例
  private readonly Lazy<HttpClient> _httpClient = 
    new(()=>{
      var httpClient = messageHander is not null ? new HttpClient(messageHanlder) : HttpClient();
      httpClient.DefaultRequestHanders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
      return httpClient;
    }, LazyThreadSafetyMode.ExecutionAndPublication);
  
  public async Task<TResult> GetAsync<TResult>(string uri, string token=""){
    var httpClient = GetOrCreateHttpClient(token);
    using var response = await httpClient.GetAsync(uri).ConfigureAwait(false);
		// 异步执行的最佳实践
    await HandleResponse(response).ConfigureAwait(false);
    var result = await response.Content.ReadFromJsonAsync<TResult>(_jsonSerializerContext).ConfigureAwait(false);

    return result;
  }
}
```



> `Lazy<T>` 延迟初始化类型
>
> 延迟初始化使得在类型初始化时，该成员不会立刻被创建，而是只有在需要时创建。
>
> 创建Lazy需要提供一个委托参数，即如何实例化该成员的委托。



## 对业务请求进行分割

在eShop项目中，对“商品目录”“购物车”“身份验证”等业务进行了分割

这里以商品目录为例

```c#
public interface ICatalogService
{
    Task<IEnumerable<CatalogBrand>> GetCatalogBrandAsync();
    Task<IEnumerable<CatalogItem>> FilterAsync(int catalogBrandId, int catalogTypeId);
    Task<IEnumerable<CatalogType>> GetCatalogTypeAsync();
    Task<IEnumerable<CatalogItem>> GetCatalogAsync();

    Task<CatalogItem> GetCatalogItemAsync(int catalogItemId);
}

// FilterAsync 的实现
public async Task<IEnumerable<CatalogItem>> FilterAsync(int catalogBrandId, int catalogTypeId)
{
    var uri = UriHelper.CombineUri(_settingsService.GatewayCatalogEndpointBase,
        $"{ApiUrlBase}/items/type/{catalogTypeId}/brand/{catalogBrandId}?PageSize=100&PageIndex=0&{ApiVersion}");

    var catalog = await _requestProvider.GetAsync<CatalogRoot>(uri).ConfigureAwait(false);

    return catalog?.Data ?? Enumerable.Empty<CatalogItem>();
}
```







