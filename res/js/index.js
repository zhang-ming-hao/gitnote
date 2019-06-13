// 页面类
class Index {
    // 构造函数
    constructor() {
        // 导航DIV
        this.nav = $("#nav");

        // 树DIV
        this.tree = $("#tree");

        // 确认对话框
        this.cdialog = $("#dialog-confirm");

        // 确认对话框中的类型
        this.ftype = $("#ftype");

        // 确认对话框中的名称
        this.fname = $("#fname");

        // 树节点个数：只增不减
        this.nodeCount = 1;

        // 编辑区
        this.editor = $("#editor");

        // 是否显示目录树
        this.showtree = GetQueryString("showtree");

        // 布局
        this.Layout();

        $(window).resize(() => {
            this.Layout();
        });

        if (this.showtree == 1) {
            this.InitTree();
            this.GetList("");
        }
        else {
            this.LoadEditor()
        }
    }

    // 布局
    Layout() {
        // 取得窗口大小
        let w = $(window).width();
        let h = $(window).height();

        // 计算控件大小
        this.editor.css("height",  h - 2 + "px");
        if (this.showtree == 1) {
            this.nav.css("height",  h - 2 + "px");
            this.editor.css("width", w - 303 + "px");
        }
        else {
            this.editor.css("width",  w + "px");
            this.nav.css("width", 0);
        }
    }

    // 初始化树控件
    InitTree() {
        let setting = {
            view: {
				showIcon: true,
				selectedMulti: false,
				addHoverDom: (treeId, treeNode) => this.AddHoverDom(treeId, treeNode),
                removeHoverDom: this.RemoveHoverDom
            },
            data: {
                simpleData: {
                    enable: true
                }
            },
            edit: {
                enable: true,
                removeTitle: "删除",
                renameTitle: "重命名",
                showRemoveBtn: this.ShowRemoveBtn,
                showRenameBtn: this.ShowRenameBtn
            },
			callback: {
				beforeExpand: (treeId, treeNode) => this.OnBeforeTreeExpand(treeNode),
                onClick: (event, treeId, treeNode, clickFlag) => this.OnTreeClick(treeNode),
                beforeRename: (treeId, treeNode, newName, isCancel) => this.OnBeforeRename(treeId, treeNode, newName, isCancel),
                beforeRemove: (treeId, treeNode) => this.OnBeforeRemove(treeId, treeNode)
			}
		};

        let zRoot = [
			{ id: this.nodeCount++, pId: null, name: "我的笔记", open: true, isParent: true}
		];

        let zTree = $.fn.zTree.init(this.tree, setting, zRoot);

        zTree.selectNode(zTree.getNodeByTId("1"));
    }

    // 控制树上是否显示删除按钮
    ShowRemoveBtn(treeId, treeNode) {
        return treeNode.id != 1;
    }

    // 控制树上是否显示编辑按钮
    ShowRenameBtn(treeId, treeNode) {
        return treeNode.id != 1;
    }

    // 当Hover时向zTree添加自定义控件
    AddHoverDom(treeId, treeNode) {
        // 只在目录节点显示
        if (!treeNode.isParent || $("#addFolderBtn_"+treeNode.tId).length>0) return;

        let sObj = $("#" + treeNode.tId + "_span");
        let addStr = "<span class='button add_folder' id='addFolderBtn_" + treeNode.tId + "' title='新建文件夹' onfocus='this.blur();'></span>";
        addStr += "<span class='button add_file' id='addFileBtn_" + treeNode.tId + "' title='新建笔记' onfocus='this.blur();'></span>";
        sObj.after(addStr);

        let btn = $("#addFolderBtn_"+treeNode.tId);
        if (btn) btn.bind("click", () => this.AddFolder(treeNode));

        btn = $("#addFileBtn_"+treeNode.tId);
        if (btn) btn.bind("click", () => this.AddNote(treeNode));
    }

    // 新建文件夹
    AddFolder(treeNode) {
        this.curNode = treeNode;
        if (!treeNode.open) {
            let zTree = $.fn.zTree.getZTreeObj("tree");
            zTree.expandNode(treeNode, true, false, false, true);
        }

        mdbox.AddFolder(this.GetPath(treeNode), (name) => this.AddFolderCallBack(name));
    }

    // 新建文件夹成功的回调函数
    AddFolderCallBack(name) {
        let zTree = $.fn.zTree.getZTreeObj("tree");
        zTree.addNodes(this.curNode, 0, {id:this.nodeCount++, pId:this.curNode.id, name:name, isParent:true});
    }

    // 新建笔记
    AddNote(treeNode) {
        this.curNode = treeNode;
        mdbox.AddNote(this.GetPath(treeNode), (name) => this.AddFileCallBack(name));
    }

    // 新建笔记成功的回调函数
    AddFileCallBack(name) {
        let zTree = $.fn.zTree.getZTreeObj("tree");
        let tn = zTree.addNodes(this.curNode, 0, {id:this.nodeCount++, pId:this.curNode.id, name:name});
        zTree.selectNode(tn[0]);

        // 设置后台选中的文件
        mdbox.SetCurrent(this.GetPath(tn[0]));

        // 加载编辑器
        this.LoadEditor();
    }

    // 删除自定义控件
    RemoveHoverDom(treeId, treeNode) {
        $("#addFolderBtn_"+treeNode.tId).unbind().remove();
        $("#addFileBtn_"+treeNode.tId).unbind().remove();
    };

    // zTree节点展开事件处理
    OnBeforeTreeExpand(treenote) {
        // 取得zTree对象
        let zTree = $.fn.zTree.getZTreeObj("tree");

        // 设置要展开的节点为选中节点
        zTree.selectNode(treenote);

        // 删除子节点
        zTree.removeChildNodes(treenote);

        // 添加子节点
        this.GetList(this.GetPath(treenote));

        return true;
    }

    // zTree节点点击事件处理
    OnTreeClick(treenote) {
        if (!treenote.isParent) {
            // 设置后台选中的文件
            mdbox.SetCurrent(this.GetPath(treenote));

            // 加载编辑器
            this.LoadEditor();
        }
    }

    // 重命名前的事件处理
    OnBeforeRename(treeId, treeNode, newName, isCancel) {
        if (isCancel) return true;

        this.curNode = treeNode;
        if (treeNode.isParent) {
            mdbox.RenameFolder(this.GetPath(treeNode), newName,
                (treeNode, newName, newPath, isSuccess) => this.RenameCallback(treeNode, newName, newPath, isSuccess)
            );
        }
        else {
            mdbox.RenameNote(this.GetPath(treeNode), newName,
                (newName, isSuccess) => this.RenameCallback(newName, isSuccess)
            );
        }

        return false;
    }

    // 重命名回调函数
    RenameCallback(newName, isSuccess) {
        let zTree = $.fn.zTree.getZTreeObj("tree");

         if (isSuccess) {
             zTree.cancelEditName(newName);
         }
         else {
             zTree.cancelEditName();
         }
    }

    // 删除前的事件处理
    OnBeforeRemove(treeId, treeNode) {
        this.curNode = treeNode;
        if (treeNode.isParent) {
            this.ftype.text("文件夹");
        }
        else {
            this.ftype.text("笔记");
        }

        this.fname.text(treeNode.name);

        this.cdialog.dialog({
            resizable: false,
            height: "auto",
            width: 400,
            modal: true,
            buttons: {
                "删除": () => {
                    this.cdialog.dialog("close");

                    if (treeNode.isParent) {
                        mdbox.RemoveFolder(this.GetPath(treeNode), () => this.RemoveFolderCallback());
                    }
                    else {
                        mdbox.RemoveNote(this.GetPath(treeNode), () => this.RemoveNoteCallback());
                    }
                },
                "取消": () => this.cdialog.dialog("close")
            }
        });

        return false;
    }

    // 删除文件夹回调函数
    RemoveFolderCallback() {
        let zTree = $.fn.zTree.getZTreeObj("tree");
        zTree.removeChildNodes(this.curNode);
        zTree.removeNode(this.curNode);
    }

    // 删除笔记回调函数
    RemoveNoteCallback() {
        let zTree = $.fn.zTree.getZTreeObj("tree");
        zTree.removeNode(this.curNode);
    }

    // 加载编辑器
    LoadEditor() {
        this.editor.attr("src", "./editor.html");
    }

    // 取得目录中的文件和文件夹列表
    GetList(path) {
        mdbox.GetList(path, (folders, notes) => {
            let zTree = $.fn.zTree.getZTreeObj("tree");
            let pNode = zTree.getSelectedNodes()[0];

            let treenodes = [];
            for (let folder of folders) {
                treenodes.push({ id: this.nodeCount++, pId: pNode.id, name: folder, isParent: true})
            }
            for (let note of notes) {
                treenodes.push({ id: this.nodeCount++, pId: pNode.id, name: note})
            }

            zTree.addNodes(pNode, treenodes);
        })
    }

    // 取得树节点的路径
    GetPath(treeNode) {
        if (treeNode.id == 1) return "";

        let zTree = $.fn.zTree.getZTreeObj("tree");
        let pId = treeNode.pId;
        let paths = [treeNode.name];
        while (pId != 1) {
            let pNode = zTree.getNodeByTId(pId.toString());
            paths.unshift(pNode.name);

            pId = pNode.pId;
        }

        return paths.join("/");
    }
}

$(document).ready(function () {
   new Index();
});
