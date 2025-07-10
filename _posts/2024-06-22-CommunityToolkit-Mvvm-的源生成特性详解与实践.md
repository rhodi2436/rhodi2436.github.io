---
title: CommunityToolkit.Mvvm 的源生成特性详解与实践
date: 2024-06-22
tags: [CommunityToolkit.Mvvm, Source Generator, MVVM, WPF, .NET, ObservableProperty, RelayCommand, ObservableObject, ObservableValidator, ObservableRecipient]
categories: [前端开发, .NET]
---

# CommunityToolkit.Mvvm 的源生成特性详解与实践

在 .NET 生态中，MVVM（Model-View-ViewModel）架构极大地推动了前端与业务逻辑的解耦，增强了代码可维护性和可测试性。虽然 WPF 本身已具备 MVVM 架构的基础设施，但各种 MVVM 辅助包（如 CommunityToolkit.Mvvm）则进一步简化了开发流程，提升了代码的简洁性和可读性。本文将深入讲解 CommunityToolkit.Mvvm 的核心——**源生成（Source Generator）机制**，并介绍其主要特性及实践方法。

## 一、MVVM 跨平台原因简述

CommunityToolkit.Mvvm 能够在 Blazor、MAUI、WPF、WinUI 等多种 UI 框架下使用，主要原因是这些 UI 框架自设计之初，就保持了高度一致的 API 和数据绑定机制。这为 MVVM 库提供了在各平台统一运作的基础，也让相关 toolkit 可以专注于简化模块编写，而无需重复造轮子。

## 二、Source Generator 的优势与主要用途

随着 C# 和 .NET 的进化，“源生成器”（Source Generator）被引入来在编译时自动生成模板代码，从而减少样板代码的书写，提高开发效率。CommunityToolkit.Mvvm 正是利用这一特性实现了诸多 MVVM 开发中的痛点缓解，代表性功能包括：

- `[ObservableProperty]` —— 自动为字段生成 INotifyPropertyChanged 实现的属性，简化数据双向绑定。
- `[RelayCommand]` —— 自动生成 ICommand 实现，便于 ViewModel 提供命令绑定。

此外，由于 C# 本身不支持多重继承，因此此类特性极大地降低了 ViewModel 编写的复杂度。接下来，我们将介绍几个核心类及其用法。

## 三、核心类型及实现细节

### 1. ObservableObject

`ObservableObject` 是实现 INotifyPropertyChanged 的基类，是 MVVM 架构中数据绑定的底层实现。其典型用法有：

- 简单属性包装：

  ```csharp
  public class UserViewModel : ObservableObject
  {
      private string _name;
      public string Name
      {
          get => _name;
          set => SetProperty(ref _name, value);
      }
  }
  ```

- 复杂类型包装：

  ```csharp
  public class MyViewModel : ObservableObject
  {
      private User _user;
      public User User
      {
          get => _user;
          set => SetProperty(_user, value, ref _user, (u, n) => u.Name = n);
      }
  }
  ```

- 针对 `Task<T>` 属性的变更，则需使用 `SetPropertyAndNotifyOnCompletion`，通常配合私有字段加 TaskWrapper 或 TaskNotifier 使用，以便在异步任务完成后通知属性变化。

### 2. ObservableProperty

`ObservableProperty` 特性（Attribute）可以直接应用于字段上，源生成器会自动为其生成属性及变更通知，大量减少样板代码。例如：

```csharp
[ObservableProperty]
private string title;
```
会自动生成：
```csharp
public string Title
{
    get => title;
    set => SetProperty(ref title, value);
}
```

### 3. RelayCommand

通过 `[RelayCommand]` 特性，无需手动实现 ICommand，源生成会自动生成对应命令属性。适合绑定按钮等控件的Click事件。

```csharp
[RelayCommand]
private void DoSomething()
{
    // Command logic here
}
```

### 4. ObservableValidator

在表单校验场景下，`ObservableValidator` 是在 `ObservableObject` 基础上实现的扩展，实现了 `INotifyDataErrorInfo` 接口。它的特性及用法包含：

1. 属性验证：可通过 `SetProperty` 方法重载来启动验证。
2. 提供 `ValidateProperty`、`ValidateProperties`、`ClearAllErrors` 等方法进行更多定制。
3. 可自定义验证特性（如 `CustomValidator`），实现依赖于 IOC 的服务进行业务级校验，从而灵活拆分 VM 逻辑和验证逻辑。

```csharp
public class PersonViewModel : ObservableValidator
{
    [Required]
    [ObservableProperty]
    private string name;

    public PersonViewModel(IFancyService fancyService)
    {
        // 可利用注入的FancyService进行自定义验证
    }
}
```

### 5. ObservableRecipient

`ObservableRecipient` 在 `ObservableObject` 基础上，实现了消息通信的能力（通过 `IMessenger`），便于不同模块/页面之间传递信息。

- 自动生成带 `IMessenger` 参数的构造函数，公开 `Messenger` 属性，便于通过 IOC 容器自动注入消息服务。
- `IsActive` 属性用于自动管理消息注册和释放（监听者的激活/失活），可在 VM 注销、页面冻结/暂停时关闭，减少不必要的资源消耗。
- 注册消息有两种方式：
  1. 继承 `IRecipient<TMessage>`，激活（OnActivated）时自动注册；
  2. 手动重写 `OnActivated` 方法，通过 `Messager.Register` 注册特定消息。

## 四、实际开发建议

- 合理使用 `[ObservableProperty]` 和 `[RelayCommand]`，可显著优化 ViewModel 的可读性和可维护性。
- 表单/业务校验首选 `ObservableValidator`，复杂校验可自定义验证逻辑并结合依赖注入。
- 多模块消息通信推荐 `ObservableRecipient`，提升页面之间的解耦性与扩展能力。

## 五、示例代码片段

一个典型 ViewModel 示例如下：

```csharp
public partial class MainViewModel : ObservableRecipient
{
    [ObservableProperty]
    private string searchText;

    [RelayCommand]
    private void Search()
    {
        // 搜索逻辑
    }
}
```

这样就自动拥有了 INotifyPropertyChanged 实现、SearchCommand 属性、以及模块间消息收发能力等功能。

## 六、总结

CommunityToolkit.Mvvm 优雅地利用 .NET 源生成提高 MVVM 代码编写体验，并且通过高度抽象的组件帮助开发者快速实现跨平台 MVVM 功能。推荐在 .NET 新项目中优先采纳，以获得高效、专业的界面开发体验。

---

**AI润色**