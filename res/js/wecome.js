// 页面类
class Wecome {
    // 构造函数
    constructor() {
        // 调试占位div
        this.placeholder = $("#placeholder");

        // 调整窗口布局
        this.Layout();

        // 进行语法演练
        $("#training").click(this.Training);
    }

    // Layout
    Layout() {
        // 取得窗口高度
        let wHeight = $(window).height();

        this.placeholder.css("height", wHeight - 720 + "px");
    }

    // 语法演练
    Training() {
        window.location.href = "training.html";
    }
}

$(document).ready(function () {
   new Wecome();
});