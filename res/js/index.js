// 页面类
class Index {
    // 构造函数
    constructor() {
        // 导航DIV
        this.nav = $("#nav");

        // 树DIV
        this.tree = $("#tree");

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
            this.editor.css("width", w - 203 + "px");
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
				showLine: false,
				showIcon: true,
				selectedMulti: false,
				dblClickExpand: true,
				addDiyDom: this.AddDiyDom
			},
			data: {
				simpleData: {
					enable: true
				}
			},
			callback: {
				onExpand: (event, treeId, treeNode) => {this.OnTreeExpand(treeNode);},
                onClick: (event, treeId, treeNode, clickFlag) => {this.OnTreeClick(treeNode);}
			}
		};

        let zRoot = [
			{ id: "1", pId: null, name: "我的笔记", open: true, isParent: true, path: ""}
		];

        let zTree = $.fn.zTree.init(this.tree, setting, zRoot);

        this.tree.addClass("showIcon");
        zTree.selectNode(zTree.getNodeByTId("1"));
    }

    // zTree内部用函数
    AddDiyDom(treeId, treeNode) {
        let spaceWidth = 5;
        let switchObj = $("#" + treeNode.tId + "_switch");
        let icoObj = $("#" + treeNode.tId + "_ico");
        switchObj.remove();
        icoObj.before(switchObj);

        if (treeNode.level > 1) {
            let spaceStr = "<span style='display: inline-block;width:" + (spaceWidth * treeNode.level)+ "px'></span>";
            switchObj.before(spaceStr);
        }
    }

    // zTree节点展开事件处理
    OnTreeExpand(treenote) {
        let zTree = $.fn.zTree.getZTreeObj("tree");
        zTree.selectNode(treenote);
        this.GetList(treenote.path);
    }

    // zTree节点点击事件处理
    OnTreeClick(treenote) {
        mdbox.SetCurrent(treenote.path);
        this.LoadEditor();
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
                treenodes.push({ id: folder.name, pId: pNode.id, name: folder.name, isParent: true, path: folder.path})
            }
            for (let note of notes) {
                treenodes.push({ id: note.name, pId: pNode.id, name: note.name, path: note.path})
            }

            zTree.addNodes(pNode, treenodes);
        })
    }
}

$(document).ready(function () {
   new Index();
});