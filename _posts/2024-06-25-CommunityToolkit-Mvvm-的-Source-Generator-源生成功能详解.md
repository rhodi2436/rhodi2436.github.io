---
title: CommunityToolkit.Mvvm 的 Source Generator 源生成功能详解
date: 2025-07-11
tags: [CommunityToolkit.Mvvm, Source Generator, MVVM, WPF, .NET, Blazor, MAUI, WinUI, 数据验证, 消息通信]
categories: [开发框架, WPF, .NET]
---

## CommunityToolkit.Mvvm 的 Source Generator 源生成功能详解

### 引言

随着 .NET 平台的发展，MVVM 架构日渐成为主流的 UI 开发范式。WPF、Blazor、MAUI 和 WinUI 等现代 UI 框架都原生支持 MVVM 所需的基础设施。然而，实现标准的 MVVM 模式仍需编写大量样板代码。为此，CommunityToolkit.Mvvm（原 MVVM Toolkit）利用了 C# Source Generator 特性，极大简化了 MVVM 相关代码的编写，提升开发效率。

本文将详细介绍 CommunityToolkit.Mvvm 源生成的主要功能组件，并结合实际应用场景做详细说明。

---

### 一、为什么需要 Mvvm 包的 Source Generator？

尽管 WPF 和其它 UI 框架完备支持 MVVM 的运行机制（如数据绑定、命令、通知等），但传统实现方式需开发者手动实现 `INotifyPropertyChanged`、命令、数据校验等接口，大量重复的样板代码降低了开发效率。CommunityToolkit.Mvvm 的 Source Generator 通过自动生成属性、命令、验证逻辑等，大大简化了 ViewModel 的实现。

CommunityToolkit.Mvvm 能够跨 Blazor、MAUI、WPF、WinUI 等平台，源于这些框架 API 设计时就保持了高度一致性，使得一套 MVVM 基础设施可以无缝适配多种 .NET UI 框架。

---

### 二、主要 Source Generator 特性及用法

#### 1. `ObservableProperty` —— 一键生成可观察属性

通过在字段上加 `[ObservableProperty]` 特性，Source Generator 会自动生成绑定所需的属性和通知逻辑。开发者不再需要手动实现 `INotifyPropertyChanged`：

```csharp
[ObservableProperty]
private string name;
```

编译后，会自动生成对应的 public 属性，并带有属性更改通知，这简化了 ViewModel 的属性定义。

#### 2. `RelayCommand` —— 快速生成命令

同理，[RelayCommand] 特性可以帮助开发者一行代码定义命令，无需手动实现 `ICommand` 相关逻辑。例如：

```csharp
[RelayCommand]
private void SaveData() { ... }
```

会生成对应的命令属性，方便 XAML 绑定。

#### 3. ObservableObject 提供的数据通知基础

`ObservableObject` 是所有支持数据通知 ViewModel 的基类。通过其自带的 `SetProperty` 方法，可以优雅地实现属性变更通知。

- 简单属性更新可用：
  
  ```csharp
  SetProperty(ref yourProp, value)
  ```
  
- 复杂属性更新（如封装类内部字段）可用重载形式：

  ```csharp
  SetProperty(user.Name, value, user, (u, n) => u.name = n)
  ```

##### 针对 `Task<T>` 属性变更通知

如果属性类型为 `Task<T>`，可用 `TaskNotifier<T>` 私有属性，配合 `SetPropertyAndNotifyOnCompletion(ref, value)` 来在任务完成后触发通知。这对于异步数据加载尤为重要。

#### 4. ObservableValidator —— 集成数据验证

`ObservableValidator` 为 ViewModel 增加了属性级别的数据验证：

- 实现了 `INotifyDataErrorInfo` 接口
- 提供了带验证的 `SetProperty` 方法重载
- 支持 `TrySetProperty` 用于尝试设置属性并捕获验证错误
- 额外提供了 `ValidateProperty`、`ValidateProperties`、`ClearAllErrors` 等辅助方法
- 支持使用 `ValidateAttribute` 以及自定义验证逻辑

例如，给属性加 `[ValidateAttribute]`，调用 `SetProperty(ref, value, true)` 即可自动启用验证。

##### 进阶：自定义验证逻辑

可以通过 `CustomValidator` 特性，将验证逻辑与 ViewModel 分离（例如从 IOC 注入 Service 做验证）。同时也可继承 `ValidatorAttribute` 实现高级自定义。

#### 5. ObservableRecipient —— 集成消息通信

为了支持 ViewModel 之间或模块间解耦通信，`ObservableRecipient` 在 `ObservableObject` 基础上增加了消息通信功能：

- 实现了 `IMessenger` 接口
- 自动生成带 `IMessenger` 参数的构造函数，可从 IOC 容器注入消息服务
- 公开 Message 属性用于消息订阅与分发
- 提供 `IsActive` 属性，用于自动注册/注销消息监听（如 VM 注销或页面冻结时释放资源）
- `OnActivated`/`OnDeactivated` 在激活或失活时自动执行相关逻辑

注册消息有两种方式：

- 继承 `IRecipient<TMessage>`，自动注册消息
- 手动重写 `OnActivated` 并用 `Messenger.Register` 进行自定义注册

---

### 三、总结与最佳实践

CommunityToolkit.Mvvm Source Generator 极大减少了 MVVM 开发样板代码，让开发者能更加专注于业务逻辑的实现而不是琐碎的属性和命令实现。同时，它在 Blazor、WPF、MAUI、WinUI 等多个平台都能无缝适配，是 .NET MVVM 开发值得推荐的实践方案。

**常用实践建议：**

- 强制新项目采用 Source Generator，最大限度减少手写重复代码
- 合理利用数据验证与消息通信，增强 ViewModel 的健壮性和模块解耦能力
- 利用 IOC 和自定义验证特性，将业务验证与 ViewModel 解耦

---

**AI润色**
