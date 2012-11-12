(function(wysihtml5) {
  var NODE_NAME = "INLINE";
  
     wysihtml5.commands.insertInlineMedia = {
	 /**
	  * Inserts an <inline type="inline_media.model" id="object.id" class="css-class-selector" />
	  * If selection is already an inline element, it removes it
	  * 
	  * @example
	  *    wysihtml5.commands.insertInlineMedia.exec(composer, "insertInlineMedia", { type: "inline_media.model", id: "object.id", class: "css-class-selector" });
	  */
	 exec: function(composer, command, value) {
	     var doc = composer.doc,
	     inline  = this.state(composer),
	     textNode,
	     i,
	     parent;
	     
	     if (inline) {
		 // Inline already selected, set the caret before it and delete it
		 composer.selection.setBefore(inline);
		 parent = inline.parentNode;
		 parent.removeChild(inline);
		 
		 // and its parent <a> too it it has not got any other child node
		 wysihtml5.dom.removeEmptyTextNodes(parent);
		 
		 // firefox and ie sometimes don't remove the image handles, even though the image got removed
		 wysihtml5.quirks.redraw(composer.element);
		 return;
	     }
	     
	     inline = doc.createElement(NODE_NAME);
	     
	     for (i in value) {
		 inline.setAttribute(i, value[i]);
	     }
	     
	     composer.selection.insertNode(inline);
	     composer.selection.setAfter(inline);
	 },
	 state: function(composer) {
	     var doc = composer.doc,
	     selectedNode,
	     text,
	     inlinesInSelection;
	     
	     if(!wysihtml5.dom.hasElementWithTagName(doc, NODE_NAME)) {
		 return false;
	     }
	     
	     selectedNode = composer.selection.getSelectedNode();
	     if (!selectedNode) {
		 return false;
	     }
	     
	     if (selectedNode.nodeName === NODE_NAME) {
		 return selectedNode;
	     }

	     if (selectedNode.nodeType !== wysihtml5.ELEMENT_NODE) {
		 return false;
	     }

	     text = composer.selection.getText();
	     text = wysihtml5.lang.string(text).trim();
	     if (text) {
		 return false;
	     }

	     inlinesInSelection = composer.selection.getNodes(
		 wysihtml5.ELEMENT_NODE, function(node) {
		     return node.nodeName === "INLINE";
		 }
	     );

	     if (inlinesInSelection.length !== 1) {
		 return false;
	     }

	     return inlinesInSelection[0];
	 }
     };
})(wysihtml5);