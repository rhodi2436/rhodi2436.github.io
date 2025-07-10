```yaml
---
title: 探索 CommunityToolkit.Mvvm 的源生成特性及其在多平台 MVVM 开发中的应用
date: 2024-06-21
tags: [CommunityToolkit.Mvvm, 源生成, MVVM, WPF, 跨平台, ObservableProperty, RelayCommand, ObservableObject, ObservableValidator, ObservableRecipient]
categories: [开发框架, .NET]
---
```

# 探索 CommunityToolkit.Mvvm 的源生成特性及其在多平台 MVVM 开发中的应用

MVVM（Model-View-ViewModel）架构是现代 .NET UI 开发的重要模式，被广泛应用于 WPF、WinUI、MAUI 甚至 Blazor 等多种前端框架。虽然这些 UI 框架本身都内建了实现 MVVM 所需的基础设施，但实际开发中若手写代码，仍然存在不少模板化、繁琐和易错的环节。近期，Microsoft 的 CommunityToolkit.Mvvm 包凭借 Source Generator 技术，有效简化了 MVVM 相关代码的编写，大幅提高了开发效率和代码质量。

## 一、MVVM 基础设施与 CommunityToolkit.Mvvm 的意义

如 WPF 这类典型前端框架，已经实现了诸如 `INotifyPropertyChanged`、命令绑定、数据上下文等 MVVM 所需的所有核心机制。CommunityToolkit.Mvvm 并不是为了替代这些基础设施，而是进一步优化和简化了“规范化”的实现过程。例如，将一个普通属性完整实现为可通知的属性（Observable Property），传统上需要数十行重复代码，而现在 Source Generator 只需一行特性标记即可生成。

## 二、跨平台 MVVM 的统一基础

CommunityToolkit.Mvvm 能够无缝支持 WPF、Blazor、MAUI、WinUI 等多种 UI 框架，得益于这些框架自设计之初就约定了相似的 API 结构。这促进了 ViewModel 层的高度复用，令同一个 ViewModel 代码仅需极少调整就能在不同平台间迁移。

## 三、核心 Source Generator 特性

CommunityToolkit.Mvvm 的源生成特性是现代 MVVM 开发的“提效神器”。以下简要梳理包中的主要自动生成能力：

### 1. ObservableProperty —— 自动生成可观察属性

借助 `[ObservableProperty]` 特性修饰字段，Source Generator 可自动为你生成实现 `INotifyPropertyChanged` 的属性封装。

```csharp
[ObservableProperty]
private string name;
```

上述一行代码会自动生成带有 `get`、`set`、属性更改通知的 `Name` 属性。对于复杂或自定义需求，框架还提供了 `SetProperty` 方法来手动更细致地管理属性变更通知。

- 基本属性包装：
  ```csharp
  SetProperty(ref _yourProp, value);
  ```
- 复杂类型属性包装：
  ```csharp
  SetProperty(user.Name, value, user, (u, n) => u.Name = n);
  ```

对于异步任务（如 `Task<T>`），需要在任务完成后通知属性变更，可借助 `TaskNotifier<T>` + `SetPropertyAndNotifyOnCompletion` 方法实现。

### 2. RelayCommand —— 自动生成命令

借助 `[RelayCommand]`，你只需定义处理方法，源生成工具即自动生成绑定于 UI 的命令对象，极大减少了模板代码。

```csharp
[RelayCommand]
private void OnClick() { /* ... */ }
```

### 3. ObservableObject —— 可观察对象基类

`ObservableObject` 提供了 `INotifyPropertyChanged` 的标准实现，是绝大多数 ViewModel 的基类。由于 C# 不支持多重继承，开箱即用的特性可富集“添加可观察组件”能力。

### 4. ObservableValidator —— 集成属性验证

`ObservableValidator` 继承自 `ObservableObject` 并实现了 `INotifyDataErrorInfo`，极大方便了开发者的属性验证场景：

- 对应 `SetProperty`，支持属性验证的重载版
- 提供验证相关方法，如 `ValidateProperty`、`ClearAllErrors`
- 支持属性级别的验证（使用 `[ValidateAttribute]`）、方法级自定义验证（`CustomValidator` 特性指定方法与上下文）

通过继承 `ValidatorAttribute`，可以脱耦字段验证逻辑，实现更灵活的验证模块设计。例如，将验证逻辑抽取到独立服务（如 IOC 注入的 FancyService）中去执行。

### 5. ObservableRecipient —— 跨模块的消息收发

`ObservableRecipient` 增强了 ViewModel 的跨模块通讯能力：

- 基于 `IMessenger` 接口，实现模块间消息分发/接收
- 自动注入用于通讯的消息组件（需配合注册消息服务）
- 内置 `IsActive` 属性，可自动管理消息监听资源
  - 在 VM 注销/页面暂停时关闭消息监听，减少资源消耗
  - 支持 `OnActivated` / `OnDeactivated` 方法自定义注册流程
- 支持两种消息注册方式：
  1. 继承 `IRecipient<TMessage>` 接口，自动注册消息
  2. 手动重写 `OnActivated`，显式调用 `Messenger.Register` 注册

## 四、实战小结

通过对 CommunityToolkit.Mvvm 的合理利用，我们不仅能极大减少手写模板代码，更能集中精力关注业务逻辑本身。面向未来，随着 MAUI、Blazor 等多平台 UI 框架的发展，MVVM 与 Source Generator 的结合会成为主流 .NET 应用架构的不二选择。

---

**AI润色**