---
title: About Webpack
date: 2023-12-28 15:51:11 +0800
categories: [build]
tags: [Webpack, Writing]     # TAG names should always be lowercase
---

> 从原初开始, 重走时代的路程.

webpack 是一个纯粹的 **静态模块打包工具** 

## 概念

webpack 会从 *一个* 或 *多个* 入口构建 **依赖图**, 并将项目中的模块打包成一个或多个 *bundles*.

1. **入口起点**: 用来指示 webpack 使用哪个模块, 作为构造 *依赖图* 的起点. 默认值是 `./src/index.js` , 可以在配置文件中配置 `entry` 属性, 指定多个入口点.

2. **输出**: 用来指示如何创建输出的 bundle, 包括如何命名, 如何划分. 默认值是 `./dist/main.js` , 可以在配置文件中配置 `output`.

3. **Loader**: 要进行有效的打包, 就必须让 webpack 理解所有的静态资源. webpack 本身可以理解 js 和 json 文件, 但对其他格式无法正确处理. 使用 *Loader* 可以让webpack 正确处理这些文件( 例如 .css .xml 等等 ).

   ```js
   model.exports={
     output: { /* ... */ }
     module: {
     	rules: [{ test: /\.txt$/, use: 'raw-loader'}],
   	}	// 此选项规定了模块加载规则,即规则匹配则使用某种Loader
   }
   ```

4. **插件**: 如果要干涉 webpack 的内部过程, 则需要插件. 插件需要在配置文件的 `plugins` 数组中添加插件对象.

5. **mode**: 配置不同的模式, 来指示运行环境(proc, dev)



### 插件

webpack **插件**是一个具有 [`apply`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/apply) 方法的 JavaScript 对象。`apply` 方法会被 webpack compiler 调用，并且在 **整个** 编译生命周期都可以访问 compiler 对象。

`Compiler` 模块是 webpack 的主要引擎，它通过 [CLI](https://www.webpackjs.com/api/cli) 或者 [Node API](https://www.webpackjs.com/api/node) 传递的所有选项创建出一个 compilation 实例。 它扩展（extends）自 `Tapable` 类，用来注册和调用插件。 大多数面向用户的插件会首先在 `Compiler` 上注册。

在为 webpack 开发插件时，你可能需要知道每个钩子函数是在哪里调用的。想要了解这些内容，请在 webpack 源码中搜索 `hooks.<hook name>.call`。

以下生命周期钩子函数，是由 `compiler` 暴露， 可以通过如下方式访问：

```js
compiler.hooks.someHook.tap('MyPlugin', (params) => {
  /* ... */
});
```

取决于不同的钩子类型，也可以在某些钩子上访问 `tapAsync` 和 `tapPromise`。



### 配置

1. webpack 配置遵循 CommonJS 规范!





# Rullup

> 一个更现代的打包工具

## 插件系统

Rollup 插件是一个**对象**，具有 [属性](https://cn.rollupjs.org/plugin-development/#properties)、[构建钩子](https://cn.rollupjs.org/plugin-development/#build-hooks) 和 [输出生成钩子](https://cn.rollupjs.org/plugin-development/#output-generation-hooks) 中的一个或多个，并遵循我们的 [约定](https://cn.rollupjs.org/plugin-development/#conventions)。插件应作为一个**导出一个函数**的包进行发布，该函数可以使用插件特定的选项进行调用并返回此类对象。

```ts
// rollup-plugin-my-example.js
export default function myExample () {
  return {
    name: 'my-example', // 此名称将出现在警告和错误中			// name 是一个 属性
    resolveId ( source ) {														// resolveId 是一个 构建钩子
      if (source === 'virtual-module') {
        // 这表示 rollup 不应询问其他插件或
        // 从文件系统检查以找到此 ID
        return source;
      }
      return null; // 其他ID应按通常方式处理
    },
    load ( id ) {																				// load 是一个 创建钩子
      if (id === 'virtual-module') {
        // "virtual-module"的源代码
        return 'export default "This is virtual!"';
      }
      return null; // 其他ID应按通常方式处理
    }
  };
}

// rollup.config.js
import myExample from './rollup-plugin-my-example.js';
export default ({
  input: 'virtual-module', // 由我们的插件解析
  plugins: [myExample()],
  output: [{
    file: 'bundle.js',
    format: 'es'
  }]
});
```

