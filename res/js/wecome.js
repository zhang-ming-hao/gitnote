// 页面类
class Wecome {
    // 构造函数
    constructor() {
        // 调试占位div
        this.placeholder = $("#placeholder");

        // 克隆窗口
        this.cloneDlg = $("#clone_dlg");

        // 正在克隆窗口
        this.cloningDlg = $("#cloning_dlg");

        // 远程地址
        this.remote = $("#remote");

        // 调整窗口布局
        this.Layout();

        // 进行语法演练
        $("#training").click(() => this.Training());

        // 显示克隆对话框
        $("#clone").click(() => this.ShowCloneDlg());

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

    // 显示克隆对话框
    ShowCloneDlg() {
        this.cloneDlg.dialog({
            resizable: false,
            height: "auto",
            width: 400,
            modal: true,
            buttons: {
                "确定": () => {
                    let remote = this.remote.val();
                    if (remote.length > 0) {
                        // 关闭本窗口
                        this.cloneDlg.dialog("close");

                        // 显示正在克隆窗口
                        this.cloningDlg.dialog({
                            resizable: false,
                            height: "auto",
                            width: 400,
                            modal: true,
                            //隐藏默认的关闭按钮
                            open: function (event, ui) {
                                $(".ui-dialog-titlebar-close", $(this).parent()).hide();
                            }
                        });
                    }
                },
                "取消": () => this.cloneDlg.dialog("close")
            }
        });
    }
}

$(document).ready(function () {
   new Wecome();
});