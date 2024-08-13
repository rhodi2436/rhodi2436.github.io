---
title: MAUI 中的 MVVM
date: 2024-8-13 14:20:11 +0800
categories: [maui]
tags: [maui, xaml, mvvm]     # TAG names should always be lowercase
---

# MAUI 中的 MVVM

之前几篇文章，总结了如何使用Mvvm社区包创建ViewModel，介绍了Maui中视图层的数据绑定，在实践的过程中，发现一个问题：

**如何管理ViewModel？**

**什么时候初始化ViewModel？**



## 视图层实例化视图模型

官方文档中的示例，大多使用这种方式。

```xaml
<ContentPage.BindingContext>
	<local:ApplicationViewModel Info="Information" />
</ContentPage.BindingContext>
```

```C#
public MyContentPage() {
  InitailizeComponent();
  
  this.BindingContext = new Application{Info="Information"};
}
```

上面两种方式是等效的。都是在视图创建时，进行了视图模型的初始化。

如果这个视图模型只是描述了该视图（组件）的功能模型，那么这样做是比较方便的。

但如果ViewModel有其他依赖项，那么View也会与这些项目产生依赖，整个结构就变得杂乱臃肿。



## 依赖注入容器实例化视图模型

在官方文档的[依赖关系注入](https://learn.microsoft.com/zh-cn/dotnet/maui/fundamentals/dependency-injection?view=net-maui-8.0)项中，介绍了一种解耦视图层与视图模型的方式。



### 自动依赖项解析

自动依赖项解析，需要使用Shell来管理页面路由。当Shell创建新的页面对象时，会检查页面对象的构造函数参数，并从DI容器中找到依赖项并注入页面。

```C#
// 在 MauiProgram.cs 中 注册ViewModel
builder.Services.AddSinglton<ApplicationViewModel>();
// HomePage 页面必须在Shell中注册路由 AppShell.xaml.cs
Routing.RegisterRoute("HomePage", typeof(HomePage));
// HomePage 构造函数注入
public partial HomePage:ContentPage{
  private readonly ApplicationViewModel _viewModel
  public HomePage(ApplicationViewModel viewModel){
    InitialComponent();
    _viewModel = viewModel;
    BindingContext = viewModel;
  }
}
```

以上代码就是Shell来管理页面时，自动依赖注入的流程。



### 手动访问DI容器

有一种情况，当Shell并未创建时，或者不使用Shell，就需要手动访问DI容器，来获取依赖项。

假设有一个LoginPage作为应用的初始页面，当登录成功后替换为Shell应用页面。

此时LoginPage无法通过自动解析来获取依赖项，可以通过：

` Handler.MauiContext.Services.GetService<MainPageViewModel>(); ` 

访问到以来容器。

```C#
// LoginPage
public partial LoginPage:ContentPage{
  public LoginPage(){
    InitialComponent();
    
    HandlerChanged += OnHandlerChanged;
  }
  
  private void OnHandlerChanged(object sender, EventArgs e)
  {
      BindingContext = Handler.MauiContext.Services.GetService<MainPageViewModel>();
  }
}
```



### 何时使用

应用中通常有一些全局状态需要管理，例如登录用户的基本信息，一些样式，权限等。这时候使用依赖注入的方式注册一个单例的ViewModel，可以让整个应用活动期间都得以保持，并在应用的任何地方都可以访问到。













