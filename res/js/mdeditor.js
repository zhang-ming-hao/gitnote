// 页面类
class MdEditor {
    // 构造函数
    constructor() {
        // 标题DIV
        this._titleDiv = $("#title");

        // 编辑器DIV
        this.editorDiv = $("#editor_div");

        // 编辑器textarea
        this._content = $("#editor");

        // 编辑器对象
        this.editor = editormd("editor_div", {
            width: "99%",
            height: this.GetEditorHeight(),
            syncScrolling: "single",
            path: "../lib/",
            //tex: true,
            taskList: true,
            flowChart: true,
            sequenceDiagram : true,
            toolbarIcons: ["undo", "redo", "|",
                "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                "h1", "h2", "h3", "h4", "h5", "h6", "|",
                "list-ul", "list-ol", "hr", "|",
                "link", "reference-link", "image", "code", "code-block", "table", "|",
                "goto-line", "watch", "preview", "fullscreen", "clear", "search"],
            onchange : () => {this.SaveContent()}
        });

        // 加载文件标题
        this.GetTitle();

        // 加载文件内容
        this.GetContent();
    }

    // 设置文件标题
    set title(title) {
        this._titleDiv.text(title);
    }

    // 取得文件标题
    get title() {
        return this._titleDiv.text();
    }

    // 设置编辑内容
    set content(content) {
        this._content.val(content);
    }

    // 取得编辑内容
    get content() {
        return this._content.val();
    }

    // 计算编辑器的高度
    GetEditorHeight() {
        // 取得窗口高度
        let wHeight = $(window).height();

        // 取得编辑器的offset高度
        let oTop = this.editorDiv.offset().top;

        return wHeight - oTop - 80;
    }

    // 取得文件标题
    GetTitle() {
        window.parent.mdbox.GetTitle((title) =>{
            this.title = title;
        });
    }

    // 取得文件内容
    GetContent() {
        window.parent.mdbox.GetContent((content) =>{
            this.content = content;
        });
    }

    // 保存文件内容
    SaveContent() {
        window.parent.mdbox.SaveContent(this.content)
    }
}

// 页面全局变量
let page = new(MdEditor);