---
title: Vben Admin 源码解读
date: 2024-3-1 13:20:11 +0800
categories: [Vue3]
tags: [vue, web, source, vben]     # TAG names should always be lowercase
---

# Vben Admin 源码解读

> 长期更新……
>
> 为了提高编码能力和设计能力，并提高对Vue的理解，选择广受好评的 Vben Admin 项目进行学习。文章将 Vben 源码中涉及的Vue高级功能进行标注和解释，并对一些Vue组件设计思想进行解读。
> 本文不会涉及Vue基础内容



## 登陆

登陆动作有以下重点行为：

1. 表单验证 - 组件行为，使用响应性完成 Form:rule
2. 网络请求 - 状态更改，使用 Pinia.Action
3. 路由响应 - 状态更改，使用 Pinia.Action 修改更新路由表，并调用 router.replace 来重定向
4. 界面提醒 - 组件行为，根据 Action 返回值响应

### LoginForm 组件

### UserState  Pinia

Login 行为调用 Pinia.Action 



## 菜单和路由

菜单通常和路由有对应关系。同时还要考虑菜单的访问权限。权限则是与用户有关。

因此 用户登陆-构建路由表-渲染菜单组件 就成了一个固定的流程。

### PermissionState Pinia



## 搜索框和实时结果

下面描述实时搜索组件的行为：

1. 点击搜索图标，展开全屏模态框
2. 搜索框为空时，结果列表为空
3. 当键入搜索内容时，结果列表显示搜索结果
4. 更改搜索框内容，结果列表改变
5. 点击搜索结果，跳转到指定路由

本功能思路

1. 使用 teleport 将全局模态框**发送**到body元素中
2. 为了动态设定搜索结果每个 item 的行为，我们需要使用 函数引用模版 items
3. 搜索框的每次改变（重新渲染）之前，则清空结果并重新搜索
4. 使用 shallowRefs 来提高性能。我们只需要跟踪 模版的变化，无须跟踪模版对象成员。
5. 将 搜索功能 单独写成 Use 函数方便引用。

### UseRefs 钩子

该钩子函数将 shallowRef 功能进行了整合。创建了一个 Ref[] 的列表来存储列表元素的引用。方便组件根据 index 访问元素。

并使用 onBeforeUpdate 钩子在组件重新渲染前清空引用。

### UseMenuSearch 功能集合

vben 将搜索相关的功能单独放在该组合式函数中，使得代码更佳整洁。



# Vue 进阶功能

## v-bind

v-bind 用来绑定组件的 prop 与 响应式数据。通常单个 prop 的绑定可以用 `:` 代替。

**v-bind 支持批量的绑定**

## 组合式函数

组合式函数用来**复用响应式逻辑**

当不同的组件中有相同的响应行为，可以将其行为相关的响应式变量、方法、状态等单独分装成一个函数 `useXXX()`。

## 异步加载组件

`defineAsyncComponent` 可以异步加载组件。它不仅可以从服务端获取组件本身，也可以使用异步导入Import来延迟加载。

https://cn.vuejs.org/guide/components/async.html#async-components

## toRefs()

可以解构响应式对象

`const { foo } = toRefs(fref)` 

`fref` 是一个响应式对象，包含一个 foo 成员。

上述代码的 foo 也是一个响应式变量。

## 属性透传

在一个父组件中使用 `provider('key', refval)` 来暴露一个响应式 Props

然后在子组件中使用 `const x = inject('key')` 来获取响应式 Props

Vue 会自动搜索上层组件暴露的属性

## 函数模版引用

普通的模版应用很简单，只需在组件模版中使用 `ref` 属性，并在 setup 中声明一个同名引用即可。

此外，还可以使用函数动态绑定模版引用：

`<input :ref="(el)=>{ ... }"`

vben 中使用这个功能对搜索框的结果列表的 `<li>` 进行了绑定

























