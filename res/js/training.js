// 页面类
class Training {
    // 构造函数
    constructor() {
        // 编辑器DIV
        this.editorDiv = $("#editor_div");

        // 编辑器对象
        this.editor = editormd("editor_div", {
            width: "99%",
            height: this.GetEditorHeight(),
            path: "../lib/",
            tex: true,
            taskList: true,
            flowChart: true,
            sequenceDiagram : true,
            toolbarIcons: ["undo", "redo", "|",
                "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                "h1", "h2", "h3", "h4", "h5", "h6", "|",
                "list-ul", "list-ol", "hr", "|",
                "link", "reference-link", "image_", "code", "code-block", "table", "|",
                "goto-line", "watch", "preview", "fullscreen", "clear", "search"],
            toolbarIconsClass : {
                image_ : "fa-image"     // 自定义图片功能的图标
            },
            lang: {
                toolbar: {
                    image_: "添加图片"
                }
            },
            toolbarHandlers: {
                image_: (cm, icon, cursor, selection) => {
                    window.parent.mdbox.AddImageForTraining((imgPath)=>{
                        // 替换选中文本，如果没有选中文本，则直接插入
                        cm.replaceSelection(`![](${imgPath})`);

                        // 如果当前没有选中的文本，将光标移到要输入的位置
                        if(selection === "") {
                            cm.setCursor(cursor.line, cursor.ch + 1);
                        }
                    });
                }
            }


        });

        // 加载tex公式用的js和css，editormd中有bug下面的路径不能带扩展名
        editormd.katexURL = {
            js: "../js/katex.min",
            css: "../css/katex.min"
        };
    }

    // 计算编辑器的高度
    GetEditorHeight() {
        // 取得窗口高度
        let wHeight = $(window).height();

        // 取得编辑器的offset高度
        let oTop = this.editorDiv.offset().top;

        return wHeight - oTop - 15;
    }
}

// 页面全局变量
let page = new(Training);