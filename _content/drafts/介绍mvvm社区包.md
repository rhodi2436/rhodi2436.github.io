介绍CommunityToolkit.Mvvm的源生成

# WPF 本身具有 Mvvm 架构的所有基础设施。Mvvm 包只是简化这一过程。

# Mvvm包之所以可以跨UI框架（Blazor Maui WPF winUI），原因是，这些UI框架在设计之初就保持了API的一致性。

# 正因为UI框架已经有了mvvm实现的所有基础设施，因此，Mvvm包的 Source Generator 特性，就是为了**简化**范式的编写。
	- ObservableProperty 用来生成可观察属性
	- RelayCommand 用来生成命令
INotifyPropertyChanged ObservableObject … 由于C#不支持多重继承，因此，这些特性可以让一些现有的子类添加可观察的组件。

	- ObservableObject
	
	1. 使用 SetProperty(ref yourprop, value)  包装简单属性
	2. 使用 SetProperty(user.Name, value, user, (u, n)=>u.name = n) 包装复杂类型
对于 Task<T> 的属性，他的值改变是不确定的，需要 await 任务完成。也就是需要任务完成后通知。这个写法稍微复杂，使用 TaskNotifier<T> 的私有属性 + Task<T> + SetPropertyAndNotifyOnCompletion(ref ,value) 

	- ObservableValidator

	1. 在ObservableObject 的基础上实现了 INotifyDataErrorInfo
	2. 提供了 SetProperty 方法的重载，来支持属性验证
	3. 提供了 TrySetProperty 
	4. 提供了 ValidateProperty ValidateProperties ClearAllErrors 等方法
	5. ObservableValidator - Community Toolkits for .NET | Microsoft Learn
	6. 简单属性上，使用 ValidateAttribute 以及重载的 SetProperty(ref, value, true) 启动验证
	7. 自定义验证逻辑。CustomValidator 特性需要两个参数，验证上下文的类型，以及验证方法名。验证的主体部分，可以来自其他组件，比如案例中，验证主体来自IOC注入的 FancyService
自定义验证特性。继承 ValidatorAttribute，通过反射来获取验证上下文。这样可以分离 VM 逻辑和验证逻辑。

	- ObservableRecipient

	1. 在ObservableObject的基础上，实现了 Imessager 接口，用来模块之间传递-接收消息。
	2. 他会自动生成带有 Imessager 参数的构造函数，并公开Message属性，从 IOC 中获取消息组件。因此要使用此功能，也需要注册消息服务。
	3. 还有 IsActive 属性用来自动管理消息监听的相关资源。通常我们在VM注销时，或者页面处于冻结状态，暂停状态时，关闭 ISActive，从而减少资源浪费。
	4. IsActive 的更改会自动执行 OnActived  OnDeactived ，也可以直接调用这两个方法，来实现注册和注销。
	5. 注册消息模型的两种方式：
		a. 继承 Irecipient<xxmessage>, 这样 OnActived 会自动注册
		b. 手动重写 OnActived，使用 Messager.Registe 来注册
