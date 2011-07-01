/*jslint maxerr: 50, indent: 4 */
/*globals $,document,console*/
if(typeof formdesigner === 'undefined'){
    var formdesigner = {};
}

formdesigner.ui = (function () {
    "use strict";
    var that = {}, question_list = [],
    controller = formdesigner.controller,
    questionTree;

    var appendErrorMessage = that.appendErrorMessage = function(msg){
        $('#notify').addClass("notice");
        $('#notify').text($('#notify').text() + msg);
    };
    
    function do_loading_bar(){
        var pbar = $("#progressbar"),
        content = $("#content"),
        loadingBar = $("#loadingBar"),
                doneController = false,
                doneUtil = false,
                doneModel = false,
                doneTree = true,
                allDone = false,
                tryComplete = function(){
                    allDone = doneUtil && doneController && doneModel;
                    if(allDone){
                        loadingBar.delay(500).fadeOut(500);
                    }
                };

        content.show();
        loadingBar.css("background-color", "white");
        loadingBar.fadeIn(100);

        pbar.progressbar({ value: 0 });

//        $("#loadingInfo").html("downloading jstree.js");
//        $.getScript("js/jquery.jstree.js", function(){
//            pbar.progressbar({ value: (pbar.progressbar( "option", "value" )+25)});
//            doneTree = true;
//            tryComplete();
//        });
//
//        $("#loadingInfo").html("downloading util.js");
//        $.getScript("js/util.js", function (){
//            pbar.progressbar({ value: (pbar.progressbar( "option", "value" )+25)});
//            doneUtil = true;
//            tryComplete();
//        });
//
//        $("#loadingInfo").html("downloading model.js");
//        $.getScript("js/model.js", function(){
//            pbar.progressbar({ value: (pbar.progressbar( "option", "value" )+25)});
//            doneModel = true;
//            tryComplete();
//        });
//
//        $("#loadingInfo").html("downloading controller.js");
//        $.getScript("js/controller.js", function(){
//            pbar.progressbar({ value: (pbar.progressbar( "option", "value" )+25)});
//            doneController = true;
//            tryComplete();
//        });
//
//        window.setTimeout(function(){
//            if(!allDone){
//                    allDone = doneUtil && doneController && doneModel && doneTree;
//                    if(allDone){
//                        loadingBar.delay(500).fadeOut(500);
//                    }else{
//                        var alertString = '';
//                        if(!doneUtil){ alertString += '[Util.js]'; }
//                        if(!doneController){ alertString += '[Controller.js]';}
//                        if(!doneModel){ alertString += '[Model.js]';}
//                        if(!doneTree){ alertString += '[jsTree]'; }
//
//                        alert("Problem loading FormDesigner Libraries! Libraries not loaded: "+alertString);
//                    }
//            }
//                },5000);

        loadingBar.fadeOut(200);

    }

    function do_nav_bar(){
        $(function() {
            var d=300;
            $('#navigation a').each(function(){
                $(this).stop().animate({
                    'marginTop':'-80px'
                },d+=150);
            });

            $('#navigation > li').hover(
                function () {
                    $('a',$(this)).stop().animate({
                        'marginTop':'-2px'
                    },200);
                },
                function () {
                    $('a',$(this)).stop().animate({
                        'marginTop':'-80px'
                    },200);
                }
            );
        });
    }

    function init_toolbar(){
        (function c_add_text_question(){ //c_ means 'create' here
            $("#add-question").button().click(function(){
                formdesigner.controller.createQuestion();
            });
            $("#add-question-button")
                    .addClass("ui-corner-all ui-icon ui-icon-plusthick")
                    .css("float", "left");
        })();

        (function c_add_group(){
            $("#add-group-but").button().click(function(){

            });
            $("#add-group-button")
                    .addClass("ui-corner-all ui-icon ui-icon-plusthick")
                    .css("float", "left");
        })();

    }



    /**
     * Private function (to the UI anyway) for handling node_select events.
     * @param e
     * @param data
     */
    function node_select(e,data){
        var curSelUfid = jQuery.data(data.rslt.obj[0],'ufid');
        formdesigner.controller.setCurrentlySelectedMug(curSelUfid);
    };

    /**
     * Creates the UI tree
     * TODO: set up DND plugin, attach event bindings for DND.
     */
    function create_tree(){
        $("#question-tree").jstree({
            "json_data" : {
                "data" : []
            },
            "crrm" : {
                "move": {
                    "always_copy": false
                }
            },
            "types": getJSTreeTypes(),
            "plugins" : [ "json_data", "ui", "crrm", "types", "themeroller" ]
	    }).bind("select_node.jstree", function (e, data) {
                   node_select(e,data);
        });
        questionTree = $("#question-tree");
    }

//    /**
//     * Create the root form node.
//     * @param Form - The model form object.
//     */
//    var treeCreateRootFormNode = function(){
//        var objectData = {};
//        objectData["data"] = "Form";
//        objectData["attr"] = {
//            'id' : 'RootFormNode'
//        }
//        objectData["metadata"] = {'type': "root"};
//
//        $('#question-tree').jstree("create",
//                null, //reference node, use null if using UI plugin for currently selected
//                "inside", //position relative to reference node
//                objectData,
//                null, //callback after creation, better to wait for event
//                true); //skip_rename
//        $('#question-tree').jstree("select_node","#RootFormNode");
//
//    };
//    that.treeCreateRootFormNode = treeCreateRootFormNode;

    function getJSTreeTypes(){
        var groupRepeatValidChildren = ["group","repeat","question","selectQuestion"];
       var types =  {
            "max_children" : 1,
			"valid_children" : groupRepeatValidChildren,
			"types" : {
                "group" : {
                    "valid_children" : groupRepeatValidChildren
                },
                "repeat" : {
                    "valid_children" : groupRepeatValidChildren
                },
                "question" : {
                    "valid_children" : "none"
                },
                "selectQuestion" : {
                    "valid_children": ["item"]
                },
                "item" : {
                    "valid_children" : "none"
                },
				"default" : {
					"valid_children" : groupRepeatValidChildren
				}
			}
		}

    }


    /**
     * Updates the properties view such that it reflects the
     * properties of the currently selected tree item.
     *
     * This means it will show only fields that are available for this
     * specific MugType and whatever properties are already set.
     *
     * TODO: Should use the MugType to figure out which fields to display
     * TODO: create bindings to verify validity on property changes
     * TODO: show marker (or something) for required fields.
     * TODO: PARAM SHOULD BE MUGTYPE NOT MUG!
     * @param mug
     */
    var displayMugProperties = function(mug){
        var that = {}, qTable, qTHeader,qTBody, questionHolder, localMug = mug;

        questionHolder = $("#question-table-body")

        that.qTable = qTable;
        that.qTHeader = qTHeader;
        that.qTBody = qTBody;

        /**
         * Creates the Properties Box on the UI
         */
        var create = function (mug, title){
            var i,
            qTable = $('<table id="question-table" class="'+title+'"></table>');
            $('#question-properties').append(qTable);
            qTHeader = $('<thead class="question-table-header"></thead>');
            qTHeader.append('<tr><td colspan=2><b><h1>Question Properties: '+mug.properties.dataElement.properties.nodeID+'</h1></b></td></tr>');
            qTHeader.append("<tr><td><b>Property Name</b></td><td><b>Property Value</b></td></tr>");
            qTable.append(qTHeader);
            qTBody = $("<tbody></tbody>");
            qTable.append(qTBody);

            i = 'ufid';
            var row, col1,col2,mugProps;

            row = $("<tr></tr>");
            qTBody.append(row);
            row.attr('id', i);
            row.attr('class', "question-property-row");
            col1 = $("<td></td>");
            col2 = $("<td></td>");
            row.append(col1);
            row.append(col2);

            col1.html(i);
            col2.html(mug[i]);
            mugProps = mug.properties;
            for(var p in mugProps){
                var block = mugProps[p].properties;
                if(!mugProps.hasOwnProperty(p)){
                    continue;
                }
                if(typeof block === 'function' || typeof block === 'string'){
                    continue;
                }

                qTBody.append("<hr />");
                qTBody.append('<tr><td colspan=2><h2 class="properties-block-header">'+p+' Properties:</h2></tr>')

                for(i in block){
                    var inputBox;
                    if(!block.hasOwnProperty(i) || typeof block[i] === 'function'){
                        continue;
                    }
                    row = $("<tr></tr>");
                    qTBody.append(row);
                    row.attr('id', i);
                    row.attr('class', "question-property-row");
                    col1 = $('<td>'+i+'</td>');
                    col2 = $('<td></td>');
                    inputBox = $('<input value="'+block[i]+'" name="'+i+'" class="'+p+'" />');
                    col2.append(inputBox);
                    inputBox.change(function(e){
                        var target = $(e.target);
                        mug.properties[target.attr("class")].properties[target.attr("name")] = target.val();
                        mug.fire('property-changed');
                    });
                    row.append(col1);
                    row.append(col2);

                }

            }

            mug.on('property-changed',function(){
                $('#monitor-window-'+mug.ufid).filter(":input").text(JSON.stringify(mug,null,'\t'));
            },null);




        }(localMug, localMug.ufid);


        function setPropertyValForUI(property, value){
            $(".question-property-row "+property+" td:nth-child(2)").html(value);
        }
        that.setPropertValForUI = setPropertyValForUI;

        /**
         *
         * @param element can be one of (string) 'bind','data','control'
         * @param property (string) property name
         * @param val new value the property should be set to.
         */
        function setPropertyValForModel(element,property, val){
            mug[element][property] = val;
            mug.fire('property-changed');
        }

        return that;
    };
    that.displayMugProperties = displayMugProperties;

    $(document).ready(function () {
        do_loading_bar();
        init_toolbar();
        create_tree();
        do_nav_bar();

        controller = formdesigner.controller;
        controller.initFormDesigner();


    });

    return that;
}());