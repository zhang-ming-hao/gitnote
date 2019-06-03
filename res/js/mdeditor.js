// 页面类
class MdEditor {
    // 构造函数
    constructor() {
        // 标题DIV
        this._titleDiv = $("#title");

        // 放置编辑器的DIV
        this.editorDiv = $("#editor_div");

        // 编辑器内容
        this._content = this.editorDiv.children("textarea");

        // 编辑器对象
        this.editor = editormd("editor_div", {
            width: "90%",
            height: this.GetEditorHeight(),
            syncScrolling: "single",
            path: "../lib/",
            flowChart: true
        });
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
        this.editor.getValue();
    }

    // 计算编辑器的高度
    GetEditorHeight() {
        // 取得窗口高度
        let wHeight = $(window).height();

        // 取得编辑器的offset高度
        let oTop = this.editorDiv.offset().top;

        return wHeight - oTop - 10;
    }
}

// 页面初始化
$(function () {
    let obj = new(MdEditor);
    console.log(obj.content);
});