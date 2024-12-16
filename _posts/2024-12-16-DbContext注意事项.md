---
title: DbContext注意事项
date: 2024-12-16 12:20:11 +0800
categories: [dotnet]
tags: [efcore, dotnet, c#]     # TAG names should always be lowercase
---

## DbContext说明
DbContext是ORM在本机内存中存储的数据库数据的部分复制. 

当我们通过DbContext对数据库进行更改时,它会跟踪数据的改变, 以便在提交更改时, 正确生成更新脚本.

## DbContext的生存周期

DbContext 设计上, 仅仅用于"单个工作单元"。 这意味着 DbContext 实例的生存期通常很短。

在 ASP.net 中, DbContext 与 单个用户请求相关联. 当用户请求映射到某个控制器方法, ASP.net 会创建控制器实例, 并从DI容器创建 DbContext 供当前请求使用, 在完成对数据的增改后, 返回用户数据, 控制器和 DbContext 均被释放. 这个过程相当短. 

不同的是, 在 Blazor 等应用框架中, 可能无意识的导致 DbContext 生存期变得很长. 比如DI注入DbContext, 会让其生命周期与页面的生命周期相同.

这时候, 推荐使用 DbContextFactory, 将工厂注入页面, 在页面根据工作单元, 手动创建 DbContext 实例(推荐使用 using 保证其释放).

使用工厂创建还需要注意的是, DbContext并不是线程安全的. __请勿在不同线程访问同一个 DbContext 实例__!

此外还要注意异步操作. 进行异步操作必须立刻 await 等待, 否则也会出现两个异步操作在不同线程同时访问, 从而出现问题!

另外的问题是数据同步. DbContext 虽然可以将本地更改提交到数据库, 但若数据库有所更改(或者另一个DbContext对数据库进行了更改), 他并不会收到更新通知. 因此若手动创建多个 DbContext, 很容易出现数据同步问题.
