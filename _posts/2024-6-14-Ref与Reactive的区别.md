---
title: Ref与Reactive的区别
date: 2024-6-14 13:20:11 +0800
categories: [技术, 前端]
tags: [vue, ref, reactive]     # TAG names should always be lowercase
---

在Vue中可以使用两个API来创建响应式变量:
- ref()
- reactive()

其中, `reactive(a)` 会返回一个 a 的代理对象(a是非基础类型).
而 `ref(a)` 会返回一个 `RefImp<typeof a>` 对象, 其中的 value(其实是_value的访问器) 是 a 的代理对象.

当 a 是一个基本类型时, 不能使用 `reactive` 来创建响应式变量, 但可以使用 `ref`. 所以 `ref` 是更加通用的 API, 也是 Vue3 推荐使用的.

如果对一个 **代理对象** 或者 **已经拥有代理**的对象 进行 `ref` 和 `reactive` 操作, 只会返回 **同一个** 代理对象. 所以就有了以下的验证:

```js
const obj = {a: 1, b: 2}
const obj_ref = ref(obj)
const obj_rac = reactive(obj)

console.log(obj === obj_ref) // false
console.log(obj_ref.value === obj_rac) // true
```