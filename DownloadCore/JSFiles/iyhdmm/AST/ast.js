const fs = require('fs');
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;

// 读取文件
readPath = 'DownloadCore\\JSFiles\\iyhdmm\\AST\\iyhdmm.js'
writePath = 'DownloadCore\\JSFiles\\iyhdmm\\AST\\iyhdmm_decoded.js'
let input_code = fs.readFileSync(readPath, { encoding: "utf-8" });

// 转换为ast树
let ast = parser.parse(input_code);

/*-----------------------------------------------------------------------------------------------------------------------------------------------------------*/

let new_array = parser.parse('');
new_array.program.body.push(ast.program.body[0].declarations[2]);// 大数组声明语句
new_array.program.body.push(ast.program.body[3]); // 解密函数声明语句
let decrypt_func = new_array.program.body[1].id.name; // 解密函数名
// 将2部分代码转换成js,并且执行加载到内存
eval(generator(new_array, { compact: true }).code);

// 遍历ast树,找到并调用解密函数
traverse(ast, {
    CallExpression(path) {
        node = path.node
        if (node.callee.name != decrypt_func) return;
        // 找到解密函数的调用参数
        let args = node.arguments
        // 解密函数参数个数为2
        if (args.length != 2) return;
        // 解密函数参数类型为字符串 字符串
        if (args[0].type != 'StringLiteral' || args[1].type != 'StringLiteral') return;
        let binding = path.scope.getBinding(decrypt_func)
        if (!binding) return;
        
    }
})

// 删除多余空行
traverse(ast, {
    EmptyStatement(path) {
        path.remove()
    }
})
console.log('finish--> 删除多余空行');

// 规范语句,给语句加{}
traverse(ast, {
    // if语句
    IfStatement: {
        exit(path) {
            let { test, consequent, alternate } = path.node;
            if (!t.isBlockStatement(consequent)) {
                path.node.consequent = t.blockStatement([consequent])
            }
            if (alternate !== null && !t.isBlockStatement(alternate)) {
                path.node.alternate = t.blockStatement([alternate])
            }
        }
    },
    // for 和 while
    "ForStatement|WhileStatement": {
        exit(path) {
            let { body } = path.node;
            if (!t.isBlockStatement(body)) {
                path.node.body = t.blockStatement([body])
            }
        }
    },
})
console.log('finish--> 规范语句,给语句加{}');

// 逗号表达式还原
traverse(ast, {
    // var 赋值语句的逗号表达式情况
    VariableDeclaration: {
        exit(path) {
            let { node } = path;
            // 排除var只有一个初始化的节点情况
            if (node.declarations.length == 1) return;
            // 排除for循环中的逗号表达式情况
            if (path.parentPath.isForStatement()) return;
            // 获取节点在容器冲的索引
            let index = path.key
            // 获取容器名字
            let container = path.listKey
            // 节点替换操作start
            let new_array = [];  // 创建用来存放node节点的数组
            // 取出原本在列表中的node节点(splice会默认删除取出的内容)
            let new_var = node.declarations.splice(1)
            new_var.map(v => {
                // 创建节点
                let create_node = t.variableDeclaration('var', [v])
                // 将节点添加到数组中去
                new_array.push(create_node)
            })
            // 将取出来的节点添加到指定位置
            new_array.reverse().map(q => {
                path.parent[container].splice(index + 1, 0, q)
            })
        }
    },
    // return语句逗号还原
    ReturnStatement: {
        exit(path) {
            let { node } = path;
            if (node.argument.expressions instanceof Array && node.argument.expressions.length > 1) {
                // 获取节点在容器冲的索引
                let index = path.key
                // 获取容器名字
                let container = path.listKey
                // 保留数组中的最后一个值
                let return_body = node.argument.expressions

                // 如果return中含有自执行函数,则不便利此次逗号表达式(情况可能有很多种,需要维护!!!!!!!!!!!!!!!!!!!!!!!!!)
                let flag;
                return_body.map(v => {
                    if (v.type == 'CallExpression' && v.callee && v.callee.type == 'FunctionExpression' && v.arguments) {
                        // console.log(generator(v).code)
                        flag = true;
                    }
                })
                if (flag) return;

                // 替换操作
                let new_return = return_body.splice(0, return_body.length - 1)
                new_return.reverse().map(v => {
                    // 特殊(不全)的自执行函数需要特殊处理
                    if (v.type == 'CallExpression' && v.callee && v.callee.type == 'FunctionExpression' && v.arguments) {
                        v = t.expressionStatement(v) // 给自执行函数头尾添加()
                        path.parent[container].splice(index + 1, 0, v);
                        return;
                    }
                    path.parent[container].splice(index + 1, 0, v);
                })
                // 构造最后一个return语句,并添加到父级容器中
                let last_node = t.returnStatement(return_body[0])
                path.parent[container].push(last_node)
                // 删除原来的整个return节点
                path.remove()
            }
        }
    },
    // 序列表达式
    ExpressionStatement: {
        exit(path) {
            let { node } = path;
            if (node.expression.expressions instanceof Array && node.expression.expressions.length > 1) {
                // 获取节点在容器中的索引
                let index = path.key
                // 获取容器名字
                let container = path.listKey
                // 替换操作
                node.expression.expressions.reverse().map(v => {
                    path.parent[container].splice(index + 1, 0, v);
                })
                // 直接path.remove()删除原节点
                path.remove();
            }
        }
    },
})
console.log('finish--> 逗号表达式还原');



/*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/
// 生成新的js code，并保存到文件中输出
let output_code = generator(ast, {
    comments: false, // false为删除所有注释
    retainLines: false, // 是否保留多余空行: true为保留  false为不保留
    // compact: true, // 压缩代码
}).code;
fs.writeFile(writePath, output_code, (err) => { });